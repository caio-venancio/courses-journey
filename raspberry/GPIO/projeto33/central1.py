#!/usr/bin/env python3
"""
central1.py — Servidor Central

Responsabilidades:
  • Aceita conexões TCP dos dois Servidores Distribuídos
  • Polling MODBUS RS485 (dispositivo 0x20) → night_mode + emergência
  • Aciona câmeras LPR via MODBUS (0x11-0x14) ao receber speed_alert
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
import modbus    # noqa: E402

# ======================================================================
# CONFIGURAÇÃO
# ======================================================================
_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
with open(_CONFIG_FILE) as f:
    full_cfg = json.load(f)

cfg_central = full_cfg["central"]
cfg_rules   = full_cfg["traffic_rules"]

CENTRAL_HOST = os.environ.get("CENTRAL_HOST", cfg_central["host"])
CENTRAL_PORT = int(os.environ.get("CENTRAL_PORT", cfg_central["port"]))

SERIAL_PORT = os.environ.get("SERIAL_PORT", cfg_central["serial_port"])
MODBUS_BAUD = cfg_central["modbus_baud"]
MATRICULA   = os.environ.get("MATRICULA", cfg_central["matricula"])

LOG_FILE   = cfg_central["log_file"]
STATE_FILE = cfg_central["state_file"]

MODBUS_POLL_INTERVAL = 0.3
CAMERA_ADDRESSES = {1: 0x11, 2: 0x12, 3: 0x13, 4: 0x14}

FINE_MILD     = cfg_rules["fine_mild"]
FINE_MODERATE = cfg_rules["fine_moderate"]
FINE_SEVERE   = cfg_rules["fine_severe"]
# [FIX] Mapa de câmeras conforme enunciado §4.1: sensor → endereço MODBUS
CAMERA_ADDRESSES = {1: 0x11, 2: 0x12, 3: 0x13, 4: 0x14}

# Limites de multa conforme faixas de excesso (km/h)
FINE_MILD    = 195.23   # excesso ≤ 20 km/h
FINE_MODERATE = 293.47  # excesso ≤ 50 km/h
FINE_SEVERE  = 880.41   # excesso > 50 km/h

# ======================================================================
# ESTADO GLOBAL
# ======================================================================

_lock = threading.Lock()

FLOW_WINDOW_S = 60.0   # janela deslizante para cálculo de carros/min

traffic: dict[int, dict] = {
    i: {
        "count":      0,
        "speeds":     deque(maxlen=20),
        "timestamps": deque(),   # sem maxlen — purgamos por tempo
    }
    for i in range(1, 5)
}

fines: list[dict] = []
event_log: deque  = deque(maxlen=200)

_dist_sockets: dict[int, socket.socket | None] = {1: None, 2: None}
_dist_lock = threading.Lock()

# Estado MODBUS — lido pelo polling e pela UI
modbus_state = {
    "night_mode":               False,
    "emergency_active":         False,
    "emergency_signal_group":   0,
    "emergency_intersection_id": 0,
    "emergency_road":           0,
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
            for sid_str, info in data.get("traffic", {}).items():
                sid = int(sid_str)
                if sid in traffic:
                    traffic[sid]["count"] = info.get("count", 0)
        _log_event("[STATE] Estado restaurado do disco.")
    except Exception as e:
        _log_event(f"[STATE] Falha ao carregar estado: {e}")


def _save_state():
    with _lock:
        data = {
            "fines":   list(fines),
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
    """Grava uma multa no arquivo de log persistente."""
    try:
        # [FIX] Garante que o diretório existe antes de abrir o arquivo
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        # [FIX] Escreve cabeçalho se o arquivo for novo/vazio
        is_new = not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0
        with open(LOG_FILE, "a") as f:
            if is_new:
                f.write(
                    "# timestamp | cruzamento | sensor | velocidade (km/h) | "
                    "camera_modbus | placa | confianca (%) | valor_multa\n"
                )
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

# [FIX] Um único objeto ModbusRTU — o lock interno da classe serializa os acessos.
# Não use _modbus_lock externo para envolver chamadas individuais; isso causava
# deadlock quando _trigger_camera (em thread filha) tentava adquirir um lock
# já mantido por _modbus_poll_loop (thread independente).
_modbus: modbus.ModbusRTU | None = None


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


def _calculate_fine(speed_kmh: float) -> float:
    excess = speed_kmh - 60.0
    if excess <= 20:
        return FINE_MILD
    elif excess <= 50:
        return FINE_MODERATE
    else:
        return FINE_SEVERE


def _trigger_camera(sensor_id: int, speed_kmh: float,
                    intersection: int, timestamp: str):
    """
    Aciona a câmera LPR correspondente ao sensor via MODBUS e registra
    a multa. Executado em thread filha para não bloquear o loop TCP.

    Fluxo (§4.2 do enunciado):
      1. Escreve trigger=1 no offset 1
      2. Polling do status (offset 0) até 2=OK ou 3=Erro (timeout 2 s)
      3. Se OK: lê placa (offsets 2-5) e confiança (offset 6)
      4. Reseta trigger para 0
      5. Registra multa
    """
    cam_addr = CAMERA_ADDRESSES.get(sensor_id)
    if cam_addr is None:
        return

    mb = _modbus
    if mb is None:
        _log_event(f"[LPR] MODBUS não disponível para sensor {sensor_id}")
        return

    _log_event(f"[LPR] Disparando câmera 0x{cam_addr:02X} — sensor {sensor_id}")

    # 1. Disparar trigger (offset 1, valor 1)
    # [FIX] O lock está dentro do ModbusRTU — não precisa de lock externo aqui.
    ok = mb.write_registers(cam_addr, 1, [1])
    if not ok:
        _log_event(f"[LPR] Falha ao disparar câmera 0x{cam_addr:02X}")
        return

    # 2. Polling de status (offset 0) até OK=2 ou Erro=3 (timeout 2 s)
    deadline = time.monotonic() + 2.0
    status = None
    while time.monotonic() < deadline:
        regs = mb.read_registers(cam_addr, 0, 1)
        if regs:
            status = regs[0]
            if status in (2, 3):
                break
        time.sleep(0.05)

    if status != 2:
        _log_event(f"[LPR] Câmera 0x{cam_addr:02X} retornou status={status}")
        mb.write_registers(cam_addr, 1, [0])
        return

    # 3. Ler placa (offsets 2-5, 4 registradores) e confiança (offset 6)
    # [FIX] Lê 5 registradores de uma vez (4 placa + 1 confiança) em vez de
    # duas leituras separadas, reduzindo tráfego no barramento.
    plate_regs = mb.read_registers(cam_addr, 2, 5)
    if not plate_regs or len(plate_regs) < 5:
        _log_event(f"[LPR] Falha ao ler placa da câmera 0x{cam_addr:02X}")
        mb.write_registers(cam_addr, 1, [0])
        return

    # Decodificar 4 registradores de 16 bits → 8 chars ASCII (big-endian)
    plate = ""
    for reg in plate_regs[:4]:
        plate += chr((reg >> 8) & 0xFF)
        plate += chr(reg & 0xFF)
    plate = plate.strip("\x00").strip()
    confidence = plate_regs[4]

    # 4. Resetar câmera
    mb.write_registers(cam_addr, 1, [0])

    # 5. Registrar multa
    fine_value = _calculate_fine(speed_kmh)
    entry = {
        "timestamp":    timestamp,
        "intersection": intersection,
        "sensor_id":    sensor_id,
        "speed_kmh":    speed_kmh,
        "camera_addr":  cam_addr,
        "plate":        plate,
        "confidence":   confidence,
        "fine_value":   fine_value,
    }
    with _lock:
        fines.append(entry)
    _append_fine_log(entry)
    _save_state()
    _log_event(
        f"[MULTA] Placa={plate} vel={speed_kmh} km/h "
        f"sensor={sensor_id} multa=R${fine_value:.2f}"
    )


# ======================================================================
# MODBUS — POLLING DO ESTADO 0x20
# ======================================================================

def _modbus_poll_loop():
    prev_night     = False
    prev_emergency = False

    while True:
        time.sleep(MODBUS_POLL_INTERVAL)

        mb = _modbus
        if mb is None:
            continue

        # [FIX] Sem lock externo — ModbusRTU já é thread-safe internamente.
        regs = mb.read_registers(0x20, 0, 11)
        if regs is None or len(regs) < 11:
            _log_event("[DEBUG]: regs não chegou corretamente")
            continue

        active          = regs[0]
        road            = regs[1]
        direction       = regs[2]
        intersection_id = regs[3]
        # vehicle_type  = regs[4]
        signal_group    = regs[5]
        # timed_out     = regs[6]
        # unattended    = regs[7]
        # elapsed       = regs[8]
        # max_time      = regs[9]
        night_mode      = bool(regs[10])

        with _lock:
            modbus_state["night_mode"]                = night_mode
            modbus_state["emergency_active"]           = bool(active)
            modbus_state["emergency_signal_group"]     = signal_group
            modbus_state["emergency_intersection_id"]  = intersection_id
            modbus_state["emergency_road"]             = road

        # ── Modo Noturno ──────────────────────────────────────────────
        if night_mode != prev_night:
            prev_night = night_mode
            _broadcast_all(protocol.night_mode(night_mode))
            _log_event(f"[MODBUS] night_mode={'ON' if night_mode else 'OFF'}")

        # ── Emergência ────────────────────────────────────────────────
        if bool(active) != prev_emergency:
            prev_emergency = bool(active)

            if active:
                # [FIX] Garante que signal_group nunca é 0 ao abrir emergência
                sg = signal_group if signal_group in (1, 2) else 1
                _log_event(
                    f"[EMERG] Ativa: road={road} dir={direction} "
                    f"iid={intersection_id} sg={sg}"
                )
                affected = _emergency_affected(road, intersection_id)
                for iid in affected:
                    _send_to_dist(iid, protocol.emergency_mode(True, sg))
            else:
                _log_event("[EMERG] Encerrada — retomando ciclo normal")
                _broadcast_all(protocol.emergency_mode(False, 0))


def _emergency_affected(road: int, intersection_id: int) -> list[int]:
    """
    Retorna lista de IDs de cruzamento afetados pela emergência.

    Regras (§6.3 do enunciado):
      - via principal (road=1) com intersection_id=0 → ambos os cruzamentos
      - intersection_id=1 ou 2 → apenas aquele cruzamento
      - qualquer outro caso → ambos (fallback seguro)
    """
    if intersection_id in (1, 2):
        return [intersection_id]
    # road=1 e intersection_id=0, ou qualquer caso não mapeado
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
        try:
            conn, addr = srv.accept()
            _log_event(f"[TCP] Conexão de {addr}")
            threading.Thread(
                target=_handle_dist_connection,
                args=(conn,),
                daemon=True,
            ).start()
        except OSError as e:
            _log_event(f"[TCP] Erro no accept: {e}")
            time.sleep(1)


def _handle_dist_connection(conn: socket.socket):
    """
    Protocolo de handshake:
      1. Aguarda {"type":"hello","intersection":N}
      2. Registra o socket em _dist_sockets[N]
      3. Loop de recebimento de mensagens
    """
    # [FIX] Timeout mais curto para o handshake inicial; depois aumenta
    # para o loop de recebimento (que pode ficar silencioso por vários segundos).
    conn.settimeout(5.0)
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
            # [FIX] Fecha o socket antigo se o cruzamento reconectar
            old = _dist_sockets.get(intersection_id)
            if old is not None:
                try:
                    old.close()
                except OSError:
                    pass
            _dist_sockets[intersection_id] = conn

        # Loop de recebimento — timeout mais longo para mensagens periódicas
        conn.settimeout(10.0)
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
                # [FIX] Só limpa o slot se ainda aponta para ESTE socket,
                # evitando apagar uma reconexão que chegou ao mesmo tempo.
                if _dist_sockets.get(intersection_id) is conn:
                    _dist_sockets[intersection_id] = None
            _log_event(f"[TCP] Cruzamento {intersection_id} desconectado.")
        conn.close()


def _handle_dist_message(msg: dict):
    mtype = msg.get("type")

    if mtype == "speed_alert":
        # [FIX] Validação defensiva dos campos obrigatórios
        sensor_id    = msg.get("sensor_id")
        speed_kmh    = msg.get("speed_kmh")
        intersection = msg.get("intersection")
        if None in (sensor_id, speed_kmh, intersection):
            _log_event(f"[ALERTA] Mensagem speed_alert incompleta: {msg}")
            return
        timestamp = msg.get("timestamp", datetime.now(timezone.utc).isoformat())

        with _lock:
            if sensor_id in traffic:
                traffic[sensor_id]["speeds"].append(speed_kmh)
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
                try:
                    sid = int(sid_str)
                except ValueError:
                    continue
                if sid not in traffic:
                    continue
                prev      = traffic[sid]["count"]
                new_total = int(cnt)
                new_vehicles = max(0, new_total - prev)
                traffic[sid]["count"] = new_total
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
        # [FIX] Remove o socket inválido para que a próxima reconexão funcione
        with _dist_lock:
            if _dist_sockets.get(intersection_id) is sock:
                _dist_sockets[intersection_id] = None
        _log_event(f"[TCP] Cruzamento {intersection_id} desconectou durante envio.")


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
ROAD_NAMES    = {0: "—", 1: "Principal",  2: "Cruzamento"}
DIRECTIONS    = {0: "—", 1: "Leste",      2: "Oeste",  3: "Norte", 4: "Sul"}


def _avg_speed(sensor_id: int) -> str:
    with _lock:
        speeds = list(traffic[sensor_id]["speeds"])
    if not speeds:
        return "—"
    return f"{sum(speeds)/len(speeds):.1f}"


def _flow(sensor_id: int) -> str:
    """Taxa de tráfego em carros/min usando janela deslizante de 60 s."""
    now    = time.monotonic()
    cutoff = now - FLOW_WINDOW_S
    with _lock:
        ts_deque = traffic[sensor_id]["timestamps"]
        while ts_deque and ts_deque[0] < cutoff:
            ts_deque.popleft()
        count_in_window = len(ts_deque)
    rate = count_in_window * (60.0 / FLOW_WINDOW_S)
    return f"{rate:.1f}"


def _run_ui(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(200)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN,  -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_RED,    -1)
    curses.init_pair(4, curses.COLOR_CYAN,   -1)

    HELP = (
        "Q=sair | N=night toggle | E=forçar fim emergência | "
        "1/2=semáforo cruzamento | P=limpar override manual"
    )

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        row  = 0

        def wprint(r, c, text, attr=0):
            try:
                stdscr.addstr(r, c, text[:w - c - 1], attr)
            except curses.error:
                pass

        wprint(row, 0,
               "═══ SERVIDOR CENTRAL — CONTROLE DE CRUZAMENTOS ═══",
               curses.A_BOLD)
        row += 1

        with _lock:
            ms       = dict(modbus_state)
            fn_count = len(fines)

        night_str = "NOITE ●" if ms["night_mode"] else "DIA   ○"
        emerg_str = "EMERGÊNCIA ●" if ms["emergency_active"] else "Normal     ○"
        wprint(row, 0, f"  Modo: {night_str}   Estado: {emerg_str}", curses.A_BOLD)
        row += 1

        if ms["emergency_active"]:
            wprint(row, 0,
                   f"  Via: {ROAD_NAMES.get(ms['emergency_road'], '?')} | "
                   f"SG: {ms['emergency_signal_group']} | "
                   f"iid: {ms['emergency_intersection_id']}",
                   curses.color_pair(3) | curses.A_BOLD)
            row += 1

        wprint(row, 0, "─" * min(w - 1, 60))
        row += 1

        # Cabeçalho da tabela de sensores
        wprint(row, 0,
               f"  {'Sensor':<8} {'Cruzamento':<12} {'Fluxo(c/min)':<14} "
               f"{'Total':<8} {'Vel. Média':<12} {'Online':<6}")
        row += 1
        wprint(row, 0, "  " + "─" * 56)
        row += 1

        with _dist_lock:
            online = {k: v is not None for k, v in _dist_sockets.items()}

        for sid in range(1, 5):
            iid   = 1 if sid <= 2 else 2
            flow  = _flow(sid)
            with _lock:
                total = traffic[sid]["count"]
            avg  = _avg_speed(sid)
            conn = "✓" if online.get(iid) else "✗"
            attr = curses.color_pair(1) if online.get(iid) else curses.color_pair(3)
            wprint(row, 0,
                   f"  {sid:<8} {iid:<12} {flow:<14} {total:<8} "
                   f"{avg + ' km/h':<12} {conn:<6}",
                   attr)
            row += 1

        wprint(row, 0, "─" * min(w - 1, 60))
        row += 1

        wprint(row, 0, f"  Multas registradas: {fn_count}", curses.color_pair(2))
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
            wprint(row, 0, line, curses.color_pair(3))
            row += 1

        wprint(row, 0, "─" * min(w - 1, 60))
        row += 1

        wprint(row, 0, "  Log de eventos:", curses.A_BOLD)
        row += 1
        with _lock:
            events = list(event_log)
        max_events = max(0, h - row - 3)
        for evt in events[-max_events:]:
            wprint(row, 0, "  " + evt)
            row += 1

        wprint(h - 1, 0, HELP, curses.A_DIM)
        stdscr.refresh()

        # ── Teclas ────────────────────────────────────────────────────
        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            break

        elif key in (ord("n"), ord("N")):
            # [FIX] Toggle correto: atualiza modbus_state e transmite
            with _lock:
                new_night = not modbus_state["night_mode"]
                modbus_state["night_mode"] = new_night
            _broadcast_all(protocol.night_mode(new_night))
            _log_event(f"[UI] night_mode forçado para {'ON' if new_night else 'OFF'}")

        elif key in (ord("e"), ord("E")):
            # [FIX] Permite forçar fim de emergência manualmente pela UI
            with _lock:
                modbus_state["emergency_active"] = False
            _broadcast_all(protocol.emergency_mode(False, 0))
            _log_event("[UI] Emergência encerrada manualmente")

        elif key in (ord("1"), ord("2")):
            iid = int(chr(key))
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
            # Desativar override manual em todos (code=-1 → dist limpa flag)
            _broadcast_all(protocol.manual_signal(-1))
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

    threading.Thread(target=_tcp_server,       daemon=True).start()
    threading.Thread(target=_modbus_poll_loop, daemon=True).start()
    threading.Thread(target=_auto_save,        daemon=True).start()

    try:
        _start_ui()
    except KeyboardInterrupt:
        pass
    finally:
        _save_state()
        mb = _modbus
        if mb:
            mb.close()
        print("\n[CENTRAL] Encerrado.")


if __name__ == "__main__":
    main()
