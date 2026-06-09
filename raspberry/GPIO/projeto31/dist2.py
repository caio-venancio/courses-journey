#!/usr/bin/env python3
"""
dist2.py — Servidor Distribuído: Cruzamento 2

Idêntico ao dist1.py em estrutura — toda configuração de hardware
vem de config.json no mesmo diretório.
Após conectar ao Central, envia handshake {"type":"hello","intersection":N}.
"""

import os
import sys
import json
import socket
import threading
import time
from datetime import datetime, timezone

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
# CONFIGURAÇÃO — lida de config.json
# ======================================================================

_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config_dist2.json")

def _load_config() -> dict:
    with open(_CONFIG_FILE) as f:
        return json.load(f)

cfg = _load_config()

INTERSECTION_ID  = cfg["intersection_id"]
CENTRAL_HOST     = cfg["central_host"]
CENTRAL_PORT     = cfg["central_port"]
SIGNAL_PINS      = cfg["signal_pins"]
BTN_MAIN         = cfg["btn_main"]
BTN_CROSS        = cfg["btn_cross"]
SENSORS_CFG      = cfg["sensors"]

# Temporização dos semáforos (s) — Tabela 5 do enunciado
MAIN_GREEN_MIN   = 15
MAIN_GREEN_MAX   = 30
CROSS_GREEN_MIN  = 5
CROSS_GREEN_MAX  = 10
YELLOW_DURATION  = 3
ALL_RED_DURATION = 2

SPEED_LIMIT_KMH        = 60.0
SENSOR_DISTANCE_M      = 2.5
DEBOUNCE_S             = 0.2
TRAFFIC_REPORT_INTERVAL = 2.0

# ======================================================================
# GPIO SETUP
# ======================================================================

GPIO.setmode(GPIO.BCM)
GPIO.setup(SIGNAL_PINS, GPIO.OUT)
GPIO.setup([BTN_MAIN, BTN_CROSS], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for _s in SENSORS_CFG:
    GPIO.setup([_s["pin_a"], _s["pin_b"]], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ======================================================================
# ESTADO COMPARTILHADO
# ======================================================================

_lock = threading.Lock()

state = {
    "night_mode":              False,
    "emergency_active":        False,
    "emergency_signal_group":  0,
    "manual_override":         False,
    "manual_code":             0,
    "btn_main_pressed":        False,
    "btn_cross_pressed":       False,
    "counts":       {s["sensor_id"]: 0    for s in SENSORS_CFG},
    "sensor_a_times": {s["sensor_id"]: None for s in SENSORS_CFG},
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

            # ── Handshake ────────────────────────────────────────────
            hello = {"type": "hello", "intersection": INTERSECTION_ID}
            s.sendall(protocol.encode(hello))
            print(f"[NET] Conectado e hello enviado (cruzamento {INTERSECTION_ID})")

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
        except socket.timeout:
            continue
        except OSError:
            return


def _handle_command(msg: dict):
    mtype = msg.get("type")
    with _lock:
        if mtype == "night_mode":
            state["night_mode"] = msg.get("active", False)
            state["manual_override"] = False
            print(f"[CMD] night_mode={state['night_mode']}")

        elif mtype == "emergency_mode":
            state["emergency_active"]       = msg.get("active", False)
            state["emergency_signal_group"] = msg.get("signal_group", 0)
            print(f"[CMD] emergency_mode={state['emergency_active']} "
                  f"sg={state['emergency_signal_group']}")

        elif mtype == "manual_signal":
            code = msg.get("code", -1)
            if code < 0:
                state["manual_override"] = False
            else:
                state["manual_override"] = True
                state["manual_code"]     = code
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
    """Envia contagem acumulada por sensor a cada 2 s."""
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
        self.pin      = pin
        self.name     = name
        self.debounce = debounce
        self._last    = 0.0

    def check(self) -> bool:
        if GPIO.input(self.pin):
            now = time.monotonic()
            if now - self._last > self.debounce:
                self._last = now
                print(f"[BTN] {self.name}")
                return True
        return False


_btn_main  = DebouncedButton(BTN_MAIN,  f"C{INTERSECTION_ID}-Principal")
_btn_cross = DebouncedButton(BTN_CROSS, f"C{INTERSECTION_ID}-Travessia")


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
# SENSORES DE VELOCIDADE — callbacks de interrupção
# ======================================================================

def _make_callbacks(sensor_id: int):
    def on_a(channel):
        with _lock:
            state["sensor_a_times"][sensor_id] = time.monotonic()

    def on_b(channel):
        with _lock:
            t_a = state["sensor_a_times"][sensor_id]
        if t_a is None:
            return
        dt = time.monotonic() - t_a
        if dt <= 0:
            return
        speed = (SENSOR_DISTANCE_M / dt) * 3.6
        with _lock:
            state["counts"][sensor_id] += 1
            state["sensor_a_times"][sensor_id] = None
        ts = datetime.now(timezone.utc).isoformat()
        print(f"[SPD] Sensor {sensor_id}: {speed:.1f} km/h")
        if speed > SPEED_LIMIT_KMH:
            send_to_central(
                protocol.speed_alert(INTERSECTION_ID, sensor_id, speed, ts)
            )

    return on_a, on_b


for _s in SENSORS_CFG:
    _on_a, _on_b = _make_callbacks(_s["sensor_id"])
    GPIO.add_event_detect(_s["pin_a"], GPIO.RISING, callback=_on_a)
    GPIO.add_event_detect(_s["pin_b"], GPIO.RISING, callback=_on_b)

# ======================================================================
# FSM — SEMÁFOROS
# ======================================================================

class SignalState:
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
        self.start_time: float   = 0.0
        self._state.enter(self)
        self._night_last_toggle: float = 0.0
        self._night_phase: int         = 0

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

        if override:
            write_signal(ov_code)
            return

        if emergency:
            write_signal(1 if em_group == 1 else 5)
            return

        if night:
            now = time.monotonic()
            if now - self._night_last_toggle >= 1.0:
                self._night_last_toggle = now
                self._night_phase ^= 1
                write_signal(0 if self._night_phase == 0 else 4)
            return

        next_state = self._state.update(self)
        if next_state is not None:
            self._change(next_state)

# ======================================================================
# MAIN
# ======================================================================

def main():
    print(f"[DIST] Servidor Distribuído — Cruzamento {INTERSECTION_ID}")
    print(f"[DIST] Config: {_CONFIG_FILE}")

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