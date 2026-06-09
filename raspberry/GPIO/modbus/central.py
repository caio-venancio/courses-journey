import os
import sys
import time

# Insere a pasta raiz ou shared no path para conseguir importar dependências
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))
import modbus

# Importa as configurações nativas de projeto como fallback
try:
    import config
except ImportError:
    config = None

# ======================================================================
# CONFIGURAÇÃO
# ======================================================================

CENTRAL_HOST = os.environ.get("CENTRAL_HOST", "0.0.0.0")
# Ajustado com base no config.py (CENTRAL_PORT = 5000)
CENTRAL_PORT = int(os.environ.get("CENTRAL_PORT", getattr(config, 'CENTRAL_PORT', "5000")))

SERIAL_PORT = os.environ.get("SERIAL_PORT", getattr(config, 'PORT', "/dev/serial0"))
MODBUS_BAUD = getattr(config, 'BAUDRATE', 115200)
MATRICULA   = os.environ.get("MATRICULA", "027195")  # 6 dígitos

# Ajustado para utilizar as constantes do config se existirem
MODBUS_POLL_INTERVAL = getattr(config, 'REPORT_INTERVAL', 2.0)
SISTEMA_ADDR = getattr(config, 'ENDERECO_SISTEMA', 0x20)

LOG_FILE   = os.environ.get("LOG_FILE",   "multas.log")
STATE_FILE = os.environ.get("STATE_FILE", "central_state.json")

# Mapa de câmeras conforme enunciado §4.1: sensor → endereço MODBUS
CAMERA_ADDRESSES = {1: 0x11, 2: 0x12, 3: 0x13, 4: 0x14}

# Limites de multa conforme faixas de excesso (km/h)
FINE_MILD     = 195.23  # excesso ≤ 20 km/h
FINE_MODERATE = 293.47  # excesso ≤ 50 km/h
FINE_SEVERE   = 880.41  # excesso > 50 km/h

_modbus = None

def _init_modbus():
    global _modbus
    try:
        _modbus = modbus.ModbusRTU(
            port=SERIAL_PORT,
            baudrate=MODBUS_BAUD,
            matricula=MATRICULA,
        )
        print(f"[MODBUS] Porta {SERIAL_PORT} aberta. Módulo Central Ativo.")
    except Exception as e:
        print(f"[MODBUS] Falha crítica ao abrir porta: {e}")
        _modbus = None


def main():
    print("[CENTRAL] Iniciando Servidor Central...")
    _init_modbus()

    # Proteção: Impede que o laco dispare sem a porta serial aberta
    if _modbus is None:
        print("[CENTRAL] O programa será encerrado pois o nó serial não está operante.")
        return

    try:
        mb = _modbus
        while True:
            time.sleep(MODBUS_POLL_INTERVAL)

            # Uso direto da constante do Sistema Endereço
            regs = mb.read_registers(SISTEMA_ADDR, 0, 11)
            
            if regs is None or len(regs) < 11:
                print("[CENTRAL] DEBUG: Falha de comunicação. Não deu certo ler os registradores.")
            else:
                # Opcional: Mostre os dados lidos caso tenha dado certo.
                print(f"[CENTRAL] Sucesso na leitura do Módulo Emergencial: {regs}")
                
    except KeyboardInterrupt:
        print("\n[CENTRAL] Interrupção de teclado (Ctrl+C).")
    finally:
        if _modbus:
            _modbus.close()
        print("[CENTRAL] Encerrado.")

if __name__ == "__main__":
    main()