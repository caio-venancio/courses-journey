"""
protocol.py — Mensagens JSON trocadas via TCP/IP entre
Servidor Central ↔ Servidores Distribuídos.

Cada mensagem é uma linha JSON terminada em '\\n'.

Tipos (campo "type"):
  DIST → CENTRAL
    "speed_alert"   — veículo acima de 60 km/h
    "traffic_count" — contagem periódica de veículos (2 s)

  CENTRAL → DIST
    "night_mode"      — ativar/desativar modo noturno
    "emergency_mode"  — abrir/fechar via de emergência
    "manual_signal"   — forçar código de semáforo manualmente
"""

import json


def encode(msg: dict) -> bytes:
    return (json.dumps(msg) + "\n").encode()


def decode(line: bytes) -> dict | None:
    try:
        return json.loads(line.decode().strip())
    except (ValueError, UnicodeDecodeError):
        return None


# ── helpers de construção ──────────────────────────────────────────────

def speed_alert(intersection: int, sensor_id: int,
                speed_kmh: float, timestamp: str) -> dict:
    return {
        "type": "speed_alert",
        "intersection": intersection,
        "sensor_id": sensor_id,
        "speed_kmh": round(speed_kmh, 1),
        "timestamp": timestamp,
    }


def traffic_count(intersection: int, counts: dict) -> dict:
    """counts: {sensor_id: vehicle_count, ...}"""
    return {
        "type": "traffic_count",
        "intersection": intersection,
        "counts": {str(k): v for k, v in counts.items()},
    }


def night_mode(active: bool) -> dict:
    return {"type": "night_mode", "active": active}


def emergency_mode(active: bool, signal_group: int) -> dict:
    """signal_group: 1 = principal verde, 2 = cruzamento verde"""
    return {"type": "emergency_mode", "active": active,
            "signal_group": signal_group}


def manual_signal(code: int) -> dict:
    """Força o semáforo para um código de 3 bits."""
    return {"type": "manual_signal", "code": code}
