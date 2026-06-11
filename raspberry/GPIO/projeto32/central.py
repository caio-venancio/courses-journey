#!/usr/bin/env python3
"""
central.py — Servidor Central

Responsabilidades:
  • Aceita conexões TCP dos dois Servidores Distribuídos
  • Polling MODBUS RS485 (dispositivo 0x20) → night_mode + emergência
  • Aciona câmeras LPR via MODBUS (0x11–0x14) ao receber speed_alert
  • Registra multas em arquivo de log persistente
  • Interface de terminal: monitoramento em tempo real + comandos manuais
  • Reconexão automática e inicialização independente
"""

import os
import sys
import socket
import threading
import time
import json
import curses
from datetime import datetime, timezone
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))
import protocol  # noqa: E402
import modbus   # noqa: E402

# ======================================================================
# CONFIGURAÇÃO
# ======================================================================

CENTRAL_HOST = os.environ.get("CENTRAL_HOST", "0.0.0.0")
CENTRAL_PORT  = int(os.environ.get("CENTRAL_PORT", "9000"))

SERIAL_PORT   = os.environ.get("SERIAL_PORT", "/dev/serial0")
MODBUS_BAUD   = 115200
MATRICULA     = os.environ.get("MATRICULA", "027195")   # 6 dígitos

MODBUS_POLL_INTERVAL = 0.3   # s — polling do 0x20

LOG_FILE   = os.environ.get("LOG_FILE",   "multas.log")
STATE_FILE = os.environ.get("STATE_FILE", "central_state.json")

CAMERA_ADDRESSES = {1: 0x11, 2: 0x12, 3: 0x13, 4: 0x14}

# ======================================================================
# ESTADO GLOBAL
# ======================================================================

_lock = threading.Lock()

# Por sensor_id (1–4):
#   "count"      → total acumulado de veículos (persistido)
#   "speeds"     → últimas velocidades para cálculo da média (km/h)
#   "timestamps" → instantes (monotonic) das últimas passagens, janela de 60 s
FLOW_WINDOW_S = 60.0   # janela deslizante para cálculo de carros/min

traffic: dict[int, dict] = {
    i: {
        "count":      0,
        "speeds":     deque(maxlen=20),
        "timestamps": deque(),          # sem maxlen — purgamos por tempo
    }
    for i in range(1, 5)
}

fines: list[dict] = []           # lista de multas (persistente)
event_log: deque  = deque(maxlen=200)   # log de eventos para a UI

# Sockets dos distribuídos: {intersection_id: socket | None}
_dist_sockets: dict[int, socket.socket | None] = {1: None, 2: None}
_dist_lock = threading.Lock()

# Estado MODBUS atual
modbus_state = {
    "night_mode": False,
    "emergency_active": False,
    "emergency_signal_group": 0,
    "emergency_intersection_id": 0,
    "emergency_road": 0,
}

# ======================================================================
# PERSISTÊNCIA
# ======================================================================

def _load_state():
    if not os.path.exists(STATE_FILE):
        return
    try:
        with open(STATE_FILE) as f:
            data = json.load(f)
        with _lock:
            for entry in data.get("fines", []):
                fines.append(entry)
            for sid, info in data.get("traffic", {}).items():
                sid = int(sid)
                if sid in traffic:
                    traffic[sid]["count"] = info.get("count", 0)
        _log_event("[STATE] Estado restaurado do disco.")
    except Exception as e:
        _log_event(f"[STATE] Falha ao carregar estado: {e}")


def _save_state():
    with _lock:
        data = {
            "fines": list(fines),
            "traffic": {str(k): {"count": v["count"]} for k, v in traffic.items()},
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        _log_event(f"[STATE] Falha ao salvar estado: {e}")


def _auto_save():
    while True:
        time.sleep(30)
        _save_state()


# ======================================================================
# LOG
# ======================================================================

def _log_event(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    with _lock:
        event_log.append(f"[{ts}] {msg}")


def _append_fine_log(entry: dict):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(
                f"{entry['timestamp']} | cruzamento={entry['intersection']} | "
                f"sensor={entry['sensor_id']} | vel={entry['speed_kmh']} km/h | "
                f"cam=0x{entry['camera_addr']:02X} | placa={entry['plate']} | "
                f"confianca={entry['confidence']}% | "
                f"multa=R${entry['fine_value']:.2f}\n"
            )
    except Exception as e:
        _log_event(f"[LOG] Erro ao gravar multa: {e}")


# ======================================================================
# MODBUS — CÂMERA LPR
# ======================================================================

_modbus: modbus.ModbusRTU | None = None
_modbus_lock = threading.Lock()


def _init_modbus():
    global _modbus
    try:
        _modbus = modbus.ModbusRTU(
            port=SERIAL_PORT,
            baudrate=MODBUS_BAUD,
            matricula=MATRICULA,
        )
        _log_event(f"[MODBUS] Porta {SERIAL_PORT} aberta.")
    except Exception as e:
        _log_event(f"[MODBUS] Falha ao abrir porta: {e}")


def _trigger_camera(sensor_id: int, speed_kmh: float,
                    intersection: int, timestamp: str):
    cam_addr = CAMERA_ADDRESSES.get(sensor_id)
    if cam_addr is None:
        return

    with _modbus_lock:
        mb = _modbus
    if mb is None:
        _log_event(f"[LPR] MODBUS não disponível para sensor {sensor_id}")
        return

    _log_event(f"[LPR] Disparando câmera 0x{cam_addr:02X} — sensor {sensor_id}")

    with _modbus_lock:
        # 1. Escrever trigger = 1
        ok = mb.write_registers(cam_addr, 1, [1])
        if not ok:
            _log_event(f"[LPR] Falha ao disparar câmera 0x{cam_addr:02X}")
            return

        # 2. Polling de status até OK ou Erro (timeout 2 s)
        deadline = time.monotonic() + 2.0
        status = None
        while time.monotonic() < deadline:
            regs = mb.read_registers(cam_addr, 0, 1)
            if regs and regs[0] in (2, 3):
                status = regs[0]
                break
            time.sleep(0.05)

        if status != 2:
            _log_event(f"[LPR] Câmera 0x{cam_addr:02X} retornou status={status}")
            mb.write_registers(cam_addr, 1, [0])
            return

        # 3. Ler placa (offsets 2–5) e confiança (offset 6)
        plate_regs = mb.read_registers(cam_addr, 2, 5)
        if not plate_regs:
            _log_event(f"[LPR] Falha ao ler placa da câmera 0x{cam_addr:02X}")
            mb.write_registers(cam_addr, 1, [0])
            return

        # Decodificar 4 registradores de 16 bits → 8 chars ASCII
        plate = ""
        for reg in plate_regs[:4]:
            plate += chr((reg >> 8) & 0xFF)
            plate += chr(reg & 0xFF)
        plate = plate.strip("\x00").strip()
        confidence = plate_regs[4]

        # 4. Resetar câmera
        mb.write_registers(cam_addr, 1, [0])

    fine_value = _calculate_fine(speed_kmh)
    entry = {
        "timestamp":   timestamp,
        "intersection": intersection,
        "sensor_id":   sensor_id,
        "speed_kmh":   speed_kmh,
        "camera_addr": cam_addr,
        "plate":       plate,
        "confidence":  confidence,
        "fine_value":  fine_value,
    }
    with _lock:
        fines.append(entry)
    _append_fine_log(entry)
    _log_event(
        f"[MULTA] Placa={plate} vel={speed_kmh} km/h "
        f"sensor={sensor_id} multa=R${fine_value:.2f}"
    )


def _calculate_fine(speed_kmh: float) -> float:
    excess = speed_kmh - 60.0
    if excess <= 20:
        return 195.23
    elif excess <= 50:
        return 293.47
    else:
        return 880.41


# ======================================================================
# MODBUS — POLLING DO ESTADO 0x20
# ======================================================================

def _modbus_poll_loop():
    prev_night     = False
    prev_emergency = False

    while True:
        time.sleep(MODBUS_POLL_INTERVAL)
        with _modbus_lock:
            mb = _modbus
        if mb is None:
            continue

        with _modbus_lock:
            regs = mb.read_registers(0x20, 0, 11)
            print("[MODBUS] regs =", regs)
        if regs is None or len(regs) < 11:
            continue

        active          = regs[0]
        road            = regs[1]
        direction       = regs[2]
        intersection_id = regs[3]
        # vehicle_type  = regs[4]  (não usado aqui)
        signal_group    = regs[5]
        # timed_out     = regs[6]
        # unattended    = regs[7]
        # elapsed       = regs[8]
        # max_time      = regs[9]
        night_mode      = bool(regs[10])

        with _lock:
            modbus_state["night_mode"]               = night_mode
            modbus_state["emergency_active"]          = bool(active)
            modbus_state["emergency_signal_group"]    = signal_group
            modbus_state["emergency_intersection_id"] = intersection_id
            modbus_state["emergency_road"]            = road

        # ── Modo Noturno ──────────────────────────────────────────────
        if night_mode != prev_night:
            prev_night = night_mode
            _broadcast_all(protocol.night_mode(night_mode))
            _log_event(f"[MODBUS] night_mode={'ON' if night_mode else 'OFF'}")

        # ── Emergência ────────────────────────────────────────────────
        if bool(active) != prev_emergency:
            prev_emergency = bool(active)

            if active:
                _log_event(
                    f"[EMERG] Ativa: road={road} dir={direction} "
                    f"iid={intersection_id} sg={signal_group}"
                )
                # Determinar quais cruzamentos afetados
                affected = _emergency_affected(road, intersection_id)
                for iid in affected:
                    _send_to_dist(iid, protocol.emergency_mode(True, signal_group))
            else:
                _log_event("[EMERG] Encerrada — retomando ciclo normal")
                _broadcast_all(protocol.emergency_mode(False, 0))


def _emergency_affected(road: int, intersection_id: int) -> list[int]:
    """Retorna lista de IDs de cruzamento afetados pela emergência."""
    if road == 1 and intersection_id == 0:
        return [1, 2]   # via principal atravessa os dois
    elif intersection_id in (1, 2):
        return [intersection_id]
    return [1, 2]


# ======================================================================
# TCP — SERVIDOR
# ======================================================================

def _tcp_server():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((CENTRAL_HOST, CENTRAL_PORT))
    srv.listen(5)
    _log_event(f"[TCP] Escutando em {CENTRAL_HOST}:{CENTRAL_PORT}")

    while True:
        conn, addr = srv.accept()
        _log_event(f"[TCP] Conexão de {addr}")
        threading.Thread(
            target=_handle_dist_connection,
            args=(conn,),
            daemon=True
        ).start()


def _handle_dist_connection(conn: socket.socket):
    """
    O primeiro pacote recebido deve conter {"type":"hello","intersection":N}.
    Em seguida processa todos os pacotes subsequentes.
    """
    conn.settimeout(10.0)
    intersection_id: int | None = None
    buf = b""

    try:
        # Aguarda o handshake inicial
        while b"\n" not in buf:
            chunk = conn.recv(256)
            if not chunk:
                return
            buf += chunk

        line, buf = buf.split(b"\n", 1)
        hello = protocol.decode(line)
        if hello and hello.get("type") == "hello":
            intersection_id = hello.get("intersection")
            _log_event(f"[TCP] Cruzamento {intersection_id} identificado.")

        if intersection_id not in (1, 2):
            _log_event(f"[TCP] Handshake inválido: {hello}")
            return

        with _dist_lock:
            _dist_sockets[intersection_id] = conn

        # Loop de recebimento
        while True:
            try:
                chunk = conn.recv(1024)
            except socket.timeout:
                continue
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                msg = protocol.decode(line)
                if msg:
                    _handle_dist_message(msg)

    except OSError:
        pass
    finally:
        if intersection_id is not None:
            with _dist_lock:
                _dist_sockets[intersection_id] = None
            _log_event(f"[TCP] Cruzamento {intersection_id} desconectado.")
        conn.close()


def _handle_dist_message(msg: dict):
    mtype = msg.get("type")

    if mtype == "speed_alert":
        sensor_id    = msg["sensor_id"]
        speed_kmh    = msg["speed_kmh"]
        intersection = msg["intersection"]
        timestamp    = msg.get("timestamp", datetime.now(timezone.utc).isoformat())
        with _lock:
            traffic[sensor_id]["speeds"].append(speed_kmh)
            # speed_alert equivale a uma passagem — registra instante
            traffic[sensor_id]["timestamps"].append(time.monotonic())
        _log_event(
            f"[ALERTA] Cruzamento {intersection} sensor {sensor_id} "
            f"— {speed_kmh} km/h"
        )
        threading.Thread(
            target=_trigger_camera,
            args=(sensor_id, speed_kmh, intersection, timestamp),
            daemon=True,
        ).start()

    elif mtype == "traffic_count":
        counts = msg.get("counts", {})
        now = time.monotonic()
        with _lock:
            for sid_str, cnt in counts.items():
                sid = int(sid_str)
                if sid not in traffic:
                    continue
                prev      = traffic[sid]["count"]
                new_total = int(cnt)
                # Quantos veículos novos desde o último relatório?
                new_vehicles = max(0, new_total - prev)
                traffic[sid]["count"] = new_total
                # Injeta um timestamp por veículo novo na janela deslizante
                for _ in range(new_vehicles):
                    traffic[sid]["timestamps"].append(now)


def _send_to_dist(intersection_id: int, msg: dict):
    with _dist_lock:
        sock = _dist_sockets.get(intersection_id)
    if sock is None:
        return
    try:
        sock.sendall(protocol.encode(msg))
    except OSError:
        pass


def _broadcast_all(msg: dict):
    for iid in (1, 2):
        _send_to_dist(iid, msg)


# ======================================================================
# INTERFACE DE TERMINAL (curses)
# ======================================================================

SIGNAL_NAMES = {
    0: "Amarelo/Amarelo",
    1: "Verde/Vermelho",
    2: "Amarelo/Vermelho",
    4: "Vermelho Total",
    5: "Vermelho/Verde",
    6: "Vermelho/Amarelo",
}

VEHICLE_TYPES = {0: "—", 1: "Ambulância", 2: "Bombeiros", 3: "Polícia"}
ROAD_NAMES    = {0: "—", 1: "Principal", 2: "Cruzamento"}
DIRECTIONS    = {0: "—", 1: "Leste", 2: "Oeste", 3: "Norte", 4: "Sul"}


def _avg_speed(sensor_id: int) -> str:
    with _lock:
        speeds = list(traffic[sensor_id]["speeds"])
    if not speeds:
        return "—"
    return f"{sum(speeds)/len(speeds):.1f}"


def _flow(sensor_id: int) -> str:
    """Retorna a taxa de tráfego em carros/min usando janela deslizante de 60 s."""
    now = time.monotonic()
    cutoff = now - FLOW_WINDOW_S
    with _lock:
        ts_deque = traffic[sensor_id]["timestamps"]
        # Purgar entradas fora da janela (deque é ordenado por inserção)
        while ts_deque and ts_deque[0] < cutoff:
            ts_deque.popleft()
        count_in_window = len(ts_deque)
    # Escala para carros/min (a janela tem FLOW_WINDOW_S segundos)
    rate = count_in_window * (60.0 / FLOW_WINDOW_S)
    return f"{rate:.1f}"


def _run_ui(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(200)

    # Cores
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN,  -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_RED,    -1)
    curses.init_pair(4, curses.COLOR_CYAN,   -1)

    HELP = (
        "Q=sair | N=night toggle | "
        "1/2=semáforo cruzamento 1/2 | "
        "P=forçar código manual"
    )

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        row = 0

        def write(r, c, text, attr=0):
            try:
                stdscr.addstr(r, c, text[:w - c - 1], attr)
            except curses.error:
                pass

        write(row, 0,
              "═══ SERVIDOR CENTRAL — CONTROLE DE CRUZAMENTOS ═══",
              curses.A_BOLD)
        row += 1

        # Estado MODBUS
        with _lock:
            ms = dict(modbus_state)
            fn_count = len(fines)

        night_str = "NOITE ●" if ms["night_mode"] else "DIA   ○"
        emerg_str = "EMERGÊNCIA ●" if ms["emergency_active"] else "Normal     ○"
        write(row, 0, f"  Modo: {night_str}   Estado: {emerg_str}", curses.A_BOLD)
        row += 1

        if ms["emergency_active"]:
            write(row, 0,
                  f"  Via: {ROAD_NAMES.get(ms['emergency_road'])} | "
                  f"SG: {ms['emergency_signal_group']} | "
                  f"iid: {ms['emergency_intersection_id']}",
                  curses.color_pair(3) | curses.A_BOLD)
            row += 1

        write(row, 0, "─" * min(w - 1, 60))
        row += 1

        # Tabela de sensores
        write(row, 0, f"  {'Sensor':<8} {'Cruzamento':<12} {'Fluxo(c/min)':<14} "
                      f"{'Total':<8} {'Vel. Média':<12} {'Online':<6}")
        row += 1
        write(row, 0, "  " + "─" * 56)
        row += 1

        with _dist_lock:
            online = {k: v is not None for k, v in _dist_sockets.items()}

        for sid in range(1, 5):
            iid   = 1 if sid <= 2 else 2
            flow  = _flow(sid)
            with _lock:
                total = traffic[sid]["count"]
            avg   = _avg_speed(sid)
            conn  = "✓" if online.get(iid) else "✗"
            attr  = curses.color_pair(1) if online.get(iid) else curses.color_pair(3)
            write(row, 0,
                  f"  {sid:<8} {iid:<12} {flow:<14} {total:<8} {avg + ' km/h':<12} {conn:<6}",
                  attr)
            row += 1

        write(row, 0, "─" * min(w - 1, 60))
        row += 1

        # Multas
        write(row, 0, f"  Multas registradas: {fn_count}", curses.color_pair(2))
        row += 1
        with _lock:
            recent_fines = list(fines[-3:])
        for fine in reversed(recent_fines):
            line = (
                f"  {fine['timestamp'][:19]} | "
                f"placa={fine['plate']} | "
                f"vel={fine['speed_kmh']} | "
                f"R${fine['fine_value']:.2f}"
            )
            write(row, 0, line, curses.color_pair(3))
            row += 1

        write(row, 0, "─" * min(w - 1, 60))
        row += 1

        # Log de eventos
        write(row, 0, "  Log de eventos:", curses.A_BOLD)
        row += 1
        with _lock:
            events = list(event_log)
        max_events = max(0, h - row - 3)
        for evt in events[-max_events:]:
            write(row, 0, "  " + evt)
            row += 1

        # Rodapé
        write(h - 1, 0, HELP, curses.A_DIM)

        stdscr.refresh()

        # Teclas
        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            break

        elif key in (ord("n"), ord("N")):
            with _lock:
                new_night = not modbus_state["night_mode"]
                modbus_state["night_mode"] = new_night
            _broadcast_all(protocol.night_mode(new_night))
            _log_event(f"[UI] night_mode forçado para {'ON' if new_night else 'OFF'}")

        elif key in (ord("1"), ord("2")):
            iid = int(chr(key))
            # Pede o código via input simples (abandona curses brevemente)
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            stdscr.addstr(h - 2, 0, f"Código (0-7) para cruzamento {iid}: ")
            stdscr.refresh()
            try:
                code = int(stdscr.getstr(1).decode())
                code = max(0, min(7, code))
                _send_to_dist(iid, protocol.manual_signal(code))
                _log_event(f"[UI] Manual: cruzamento {iid} → código {code}")
            except (ValueError, curses.error):
                pass
            curses.noecho()
            stdscr.keypad(True)
            curses.cbreak()

        elif key in (ord("p"), ord("P")):
            # Desativar override manual em todos
            _broadcast_all({"type": "manual_signal", "code": -1})
            _log_event("[UI] Override manual removido de todos")


def _start_ui():
    try:
        curses.wrapper(_run_ui)
    except Exception as e:
        print(f"[UI] Erro: {e}")


# ======================================================================
# MAIN
# ======================================================================

def main():
    print("[CENTRAL] Iniciando Servidor Central...")
    _load_state()
    _init_modbus()
    print("MATRICULA =", MATRICULA)

    threading.Thread(target=_tcp_server,         daemon=True).start()
    threading.Thread(target=_modbus_poll_loop,   daemon=True).start()
    threading.Thread(target=_auto_save,           daemon=True).start()

    try:
        _start_ui()
    except KeyboardInterrupt:
        pass
    finally:
        _save_state()
        with _modbus_lock:
            if _modbus:
                _modbus.close()
        print("\n[CENTRAL] Encerrado.")


if __name__ == "__main__":
    main()
