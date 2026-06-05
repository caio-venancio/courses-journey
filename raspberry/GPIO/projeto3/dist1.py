#!/usr/bin/env python3
"""
dist1.py — Servidor Distribuído: Cruzamento 1

Responsabilidades:
  • Controla semáforos via GPIO (código 3 bits)
  • Lê botões de pedestre com debounce
  • Mede velocidade dos veículos via sensores A/B
  • Envia speed_alert ao Central quando v > 60 km/h
  • Envia traffic_count ao Central a cada 2 s
  • Obedece comandos night_mode, emergency_mode e manual_signal

Configuração: veja as constantes abaixo ou passe variáveis de ambiente.
"""

import os
import sys
import socket
import threading
import json
import time
from datetime import datetime, timezone

# ── caminho do módulo compartilhado ───────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))
import protocol  # noqa: E402

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("[WARN] RPi.GPIO indisponível — usando stub.")
    from unittest.mock import MagicMock
    GPIO = MagicMock()
    GPIO.BCM = 11
    GPIO.IN = 1
    GPIO.OUT = 0
    GPIO.HIGH = 1
    GPIO.LOW = 0
    GPIO.PUD_DOWN = 21
    GPIO.RISING = 31

# ======================================================================
# CONFIGURAÇÃO — Cruzamento 1
# ======================================================================

INTERSECTION_ID = 1

# Semáforo (saída RPi → ESP32)
SIGNAL_BIT0 = 17
SIGNAL_BIT1 = 18
SIGNAL_BIT2 = 23
SIGNAL_PINS  = [SIGNAL_BIT0, SIGNAL_BIT1, SIGNAL_BIT2]

# Botões de pedestre (entrada ESP32 → RPi)
BTN_MAIN  = 1
BTN_CROSS = 12

# Sensores de velocidade
SENSOR1_A = 16
SENSOR1_B = 20
SENSOR2_A = 21
SENSOR2_B = 27

# TCP — Servidor Central
CENTRAL_HOST = os.environ.get("CENTRAL_HOST", "127.0.0.1")
CENTRAL_PORT  = int(os.environ.get("CENTRAL_PORT", "9000"))

# Temporização dos semáforos (segundos)
MAIN_GREEN_MIN  = 15
MAIN_GREEN_MAX  = 30
CROSS_GREEN_MIN = 5
CROSS_GREEN_MAX = 10
YELLOW_DURATION = 3
ALL_RED_DURATION = 2

SPEED_LIMIT_KMH = 60.0
SENSOR_DISTANCE_M = 2.0
DEBOUNCE_S = 0.2
TRAFFIC_REPORT_INTERVAL = 2.0   # s

# ======================================================================
# GPIO SETUP
# ======================================================================

GPIO.setmode(GPIO.BCM)
GPIO.setup(SIGNAL_PINS, GPIO.OUT)
GPIO.setup([BTN_MAIN, BTN_CROSS], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup([SENSOR1_A, SENSOR1_B, SENSOR2_A, SENSOR2_B],
           GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ======================================================================
# ESTADO COMPARTILHADO
# ======================================================================

_lock = threading.Lock()

state = {
    # semáforo
    "signal_code": 1,         # código 3-bits atual
    "night_mode": False,
    "emergency_active": False,
    "emergency_signal_group": 0,
    "manual_override": False,
    "manual_code": 0,
    # pedestre
    "btn_main_pressed": False,
    "btn_cross_pressed": False,
    # velocidade / contagem
    "counts": {1: 0, 2: 0},   # sensor_id → contagem total
    "sensor1_a_time": None,
    "sensor2_a_time": None,
}

_central_socket: socket.socket | None = None
_central_lock = threading.Lock()

# ======================================================================
# GPIO — SEMÁFORO
# ======================================================================

def write_signal(code: int):
    b0 = (code >> 0) & 1
    b1 = (code >> 1) & 1
    b2 = (code >> 2) & 1
    GPIO.output(SIGNAL_PINS, (b0, b1, b2))


# ======================================================================
# COMUNICAÇÃO COM O CENTRAL
# ======================================================================

def _connect_to_central():
    global _central_socket
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((CENTRAL_HOST, CENTRAL_PORT))
            s.settimeout(5.0)
            print(f"[NET] Conectado ao Central em {CENTRAL_HOST}:{CENTRAL_PORT}")
            with _central_lock:
                _central_socket = s
            _receive_loop(s)
        except (ConnectionRefusedError, OSError) as e:
            print(f"[NET] Falha ao conectar: {e} — tentando novamente em 3 s")
            time.sleep(3)
        finally:
            with _central_lock:
                _central_socket = None


def _receive_loop(sock: socket.socket):
    buf = b""
    while True:
        try:
            chunk = sock.recv(1024)
            if not chunk:
                print("[NET] Central fechou a conexão.")
                return
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                msg = protocol.decode(line)
                if msg:
                    _handle_command(msg)
        except (socket.timeout, OSError):
            return


def _handle_command(msg: dict):
    mtype = msg.get("type")
    with _lock:
        if mtype == "night_mode":
            state["night_mode"] = msg.get("active", False)
            state["manual_override"] = False
            print(f"[CMD] night_mode={state['night_mode']}")

        elif mtype == "emergency_mode":
            state["emergency_active"] = msg.get("active", False)
            state["emergency_signal_group"] = msg.get("signal_group", 0)
            print(f"[CMD] emergency_mode={state['emergency_active']} sg={state['emergency_signal_group']}")

        elif mtype == "manual_signal":
            code = msg.get("code", 0)
            state["manual_override"] = True
            state["manual_code"] = code
            print(f"[CMD] manual_signal code={code}")


def send_to_central(msg: dict):
    with _central_lock:
        sock = _central_socket
    if sock is None:
        return
    try:
        sock.sendall(protocol.encode(msg))
    except OSError:
        pass


def _traffic_reporter():
    while True:
        time.sleep(TRAFFIC_REPORT_INTERVAL)
        with _lock:
            counts_snapshot = dict(state["counts"])
        msg = protocol.traffic_count(INTERSECTION_ID, counts_snapshot)
        send_to_central(msg)


# ======================================================================
# DEBOUNCE — BOTÕES
# ======================================================================

class DebouncedButton:
    def __init__(self, pin: int, name: str, debounce: float = DEBOUNCE_S):
        self.pin = pin
        self.name = name
        self.debounce = debounce
        self._last = 0.0

    def check(self) -> bool:
        if GPIO.input(self.pin):
            now = time.monotonic()
            if now - self._last > self.debounce:
                self._last = now
                print(f"[BTN] {self.name}")
                return True
        return False


_btn_main  = DebouncedButton(BTN_MAIN,  "Cruzamento1-Principal")
_btn_cross = DebouncedButton(BTN_CROSS, "Cruzamento1-Travessia")


def _button_poll():
    while True:
        if _btn_main.check():
            with _lock:
                state["btn_main_pressed"] = True
        if _btn_cross.check():
            with _lock:
                state["btn_cross_pressed"] = True
        time.sleep(0.01)


# ======================================================================
# SENSORES DE VELOCIDADE — interrupção em borda de subida
# ======================================================================

def _on_sensor1_a(channel):
    with _lock:
        state["sensor1_a_time"] = time.monotonic()


def _on_sensor1_b(channel):
    with _lock:
        t_a = state["sensor1_a_time"]
    if t_a is None:
        return
    dt = time.monotonic() - t_a
    if dt <= 0:
        return
    speed = (SENSOR_DISTANCE_M / dt) * 3.6
    with _lock:
        state["counts"][1] += 1
        state["sensor1_a_time"] = None
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[SPD] Sensor1: {speed:.1f} km/h")
    if speed > SPEED_LIMIT_KMH:
        send_to_central(protocol.speed_alert(INTERSECTION_ID, 1, speed, ts))


def _on_sensor2_a(channel):
    with _lock:
        state["sensor2_a_time"] = time.monotonic()


def _on_sensor2_b(channel):
    with _lock:
        t_a = state["sensor2_a_time"]
    if t_a is None:
        return
    dt = time.monotonic() - t_a
    if dt <= 0:
        return
    speed = (SENSOR_DISTANCE_M / dt) * 3.6
    with _lock:
        state["counts"][2] += 1
        state["sensor2_a_time"] = None
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[SPD] Sensor2: {speed:.1f} km/h")
    if speed > SPEED_LIMIT_KMH:
        send_to_central(protocol.speed_alert(INTERSECTION_ID, 2, speed, ts))


GPIO.add_event_detect(SENSOR1_A, GPIO.RISING, callback=_on_sensor1_a)
GPIO.add_event_detect(SENSOR1_B, GPIO.RISING, callback=_on_sensor1_b)
GPIO.add_event_detect(SENSOR2_A, GPIO.RISING, callback=_on_sensor2_a)
GPIO.add_event_detect(SENSOR2_B, GPIO.RISING, callback=_on_sensor2_b)


# ======================================================================
# FSM — SEMÁFOROS
# ======================================================================

class SignalState:
    """Estado base da FSM de semáforos."""
    CODE:     int   = 0
    DURATION: float = 0.0
    MINIMUM:  float = 0.0

    def enter(self, fsm):
        print(f"[FSM] → código {self.CODE}")
        write_signal(self.CODE)
        fsm.start_time = time.monotonic()

    def update(self, fsm) -> "SignalState | None":
        raise NotImplementedError


class MainGreen(SignalState):
    CODE     = 1
    DURATION = MAIN_GREEN_MAX
    MINIMUM  = MAIN_GREEN_MIN

    def update(self, fsm):
        elapsed = time.monotonic() - fsm.start_time
        with _lock:
            btn = state["btn_main_pressed"] or state["btn_cross_pressed"]
        if elapsed >= self.DURATION:
            return MainYellow()
        if btn and elapsed >= self.MINIMUM:
            return MainYellow()
        return None


class MainYellow(SignalState):
    CODE     = 2
    DURATION = YELLOW_DURATION

    def update(self, fsm):
        if time.monotonic() - fsm.start_time >= self.DURATION:
            return AllRedToCross()
        return None


class AllRedToCross(SignalState):
    CODE     = 4
    DURATION = ALL_RED_DURATION

    def update(self, fsm):
        if time.monotonic() - fsm.start_time >= self.DURATION:
            return CrossGreen()
        return None


class CrossGreen(SignalState):
    CODE     = 5
    DURATION = CROSS_GREEN_MAX
    MINIMUM  = CROSS_GREEN_MIN

    def enter(self, fsm):
        super().enter(fsm)
        with _lock:
            state["btn_main_pressed"]  = False
            state["btn_cross_pressed"] = False

    def update(self, fsm):
        elapsed = time.monotonic() - fsm.start_time
        with _lock:
            btn = state["btn_main_pressed"] or state["btn_cross_pressed"]
        if elapsed >= self.DURATION:
            return CrossYellow()
        if btn and elapsed >= self.MINIMUM:
            return CrossYellow()
        return None


class CrossYellow(SignalState):
    CODE     = 6
    DURATION = YELLOW_DURATION

    def update(self, fsm):
        if time.monotonic() - fsm.start_time >= self.DURATION:
            return AllRedToMain()
        return None


class AllRedToMain(SignalState):
    CODE     = 4
    DURATION = ALL_RED_DURATION

    def update(self, fsm):
        if time.monotonic() - fsm.start_time >= self.DURATION:
            return MainGreen()
        return None


class SignalFSM:
    def __init__(self):
        self._state: SignalState = MainGreen()
        self.start_time: float = 0.0
        self._state.enter(self)
        self._night_last_toggle: float = 0.0
        self._night_phase: int = 0    # 0 → código 0, 1 → código 4

    def _change(self, new_state: SignalState):
        self._state = new_state
        self._state.enter(self)

    def run_once(self):
        with _lock:
            night     = state["night_mode"]
            emergency = state["emergency_active"]
            em_group  = state["emergency_signal_group"]
            override  = state["manual_override"]
            ov_code   = state["manual_code"]

        # Prioridade 1: override manual
        if override:
            write_signal(ov_code)
            return

        # Prioridade 2: emergência
        if emergency:
            code = 1 if em_group == 1 else 5
            write_signal(code)
            return

        # Prioridade 3: modo noturno (pisca-pisca)
        if night:
            now = time.monotonic()
            if now - self._night_last_toggle >= 1.0:
                self._night_last_toggle = now
                self._night_phase ^= 1
                write_signal(0 if self._night_phase == 0 else 4)
            return

        # Prioridade 4: ciclo normal
        next_state = self._state.update(self)
        if next_state is not None:
            self._change(next_state)


# ======================================================================
# MAIN
# ======================================================================

def main():
    print(f"[DIST] Servidor Distribuído — Cruzamento {INTERSECTION_ID}")

    # Threads de fundo
    threading.Thread(target=_connect_to_central, daemon=True).start()
    threading.Thread(target=_button_poll,         daemon=True).start()
    threading.Thread(target=_traffic_reporter,    daemon=True).start()

    fsm = SignalFSM()

    try:
        while True:
            fsm.run_once()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n[DIST] Encerrando...")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()