"""
modbus.py — MODBUS RTU sobre RS485 via pyserial.

Integrado com a rotina de CRC nativa do projeto.
Funções suportadas:
  0x03  Read Holding Registers
  0x10  Write Multiple Registers
"""

import struct
import serial
from time import sleep

### CRC-16
CRC16_TABLE = (
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
    0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
    0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
    0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
    0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
    0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
    0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
    0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
    0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
    0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
    0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
    0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
    0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
    0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
    0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
    0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
    0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
    0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
    0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
    0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
    0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
    0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
    0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
    0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
    0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
    0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
    0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
    0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
    0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040
)

# Importa as funções oficiais de CRC do seu projeto
def crc16_byte(crc, data):
    return ((crc & 0xFF00) >> 8) ^ CRC16_TABLE[(crc & 0x00FF) ^ (data & 0x00FF)]


def calcula_crc(commands):
    """
    commands pode ser:
        - bytes
        - bytearray
        - lista de inteiros
    """
    # O simulador da disciplina usa a mesma rotina de CRC da Entrega 2,
    # inicializada com 0x0000.
    crc = 0

    for b in commands:
        crc = crc16_byte(crc, b)

    return crc & 0xFFFF

def add_crc(pacote_sem_crc):
    crc = calcula_crc(pacote_sem_crc)

    crc_high = crc & 0xFF
    crc_low = (crc >> 8) & 0xFF

    return bytes(pacote_sem_crc) + bytes([crc_high, crc_low])

def check_crc(pacote_completo):
    """
    pacote_completo = mensagem inteira incluindo os 2 bytes de CRC
    """

    if len(pacote_completo) < 3:
        return False

    payload = pacote_completo[:-2]

    return list(add_crc(payload)[-2:]) == pacote_completo[-2:]


def _hex(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)


def _read_exact(ser, size: int) -> bytes:
    data = bytearray()

    while len(data) < size:
        chunk = ser.read(size - len(data))
        if not chunk:
            break
        data.extend(chunk)

    return bytes(data)


class ModbusRTU:
    MAX_RETRIES = 3

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 0.5,
        matricula: str = "000000",
        verbose: bool = True,
    ):
        self.verbose = verbose

        self._serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout,
        )

        digits = [int(c) for c in matricula.zfill(6)[-6:]]
        self._matricula = bytes(digits)

        self._log(f"[MODBUS] Porta aberta: {port} @ {baudrate} baud")

    def _log(self, msg):
        if self.verbose:
            print(msg)

    def close(self):
        if self._serial.is_open:
            self._serial.close()
            self._log("[MODBUS] Porta serial fechada")

    # ----------------------------------------------------------
    # READ HOLDING REGISTERS (0x03)
    # ----------------------------------------------------------

    def read_registers(
        self,
        slave: int,
        start: int,
        count: int,
    ) -> list[int] | None:

        payload = struct.pack(">BBHBB", slave, 0x03, start, count & 0xFF, (count >> 8) & 0xFF)
        
        # O build_frame agora utiliza a lógica correta (CRC = 0x0000 inicial)
        frame = add_crc(payload + self._matricula)

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                self._serial.reset_input_buffer()

                self._log("")
                self._log(f"[MODBUS] READ tentativa {attempt}/{self.MAX_RETRIES}")
                self._log(f"[MODBUS TX] {len(frame)} bytes: {_hex(frame)}")

                self._serial.write(frame)
                self._serial.flush()

                expected = 3 + count * 2 + 2

                response = _read_exact(self._serial, expected)

                if response:
                    self._log(f"[MODBUS RX] {len(response)} bytes: {_hex(response)}")
                else:
                    self._log("[MODBUS RX] timeout")

                if len(response) < expected:
                    self._log(f"[MODBUS] Resposta incompleta ({len(response)}/{expected} bytes)")
                    continue

                if not check_crc(list(response)):
                    self._log("[MODBUS] CRC inválido na leitura")
                    continue

                if response[1] & 0x80:
                    codigo = response[2] if len(response) > 2 else 0
                    self._log(f"[MODBUS] Exceção MODBUS 0x{codigo:02X}")
                    continue

                regs = []

                for i in range(count):
                    offset = 3 + i * 2
                    valor = struct.unpack(">H", response[offset:offset + 2])[0]
                    regs.append(valor)

                self._log("[MODBUS] Registros lidos:")
                for i, reg in enumerate(regs):
                    self._log(f"    [{start+i}] = 0x{reg:04X} ({reg})")

                return regs

            except serial.SerialException as e:
                self._log(f"[MODBUS] Erro serial: {e}")
                sleep(0.05 * attempt)

            except Exception as e:
                self._log(f"[MODBUS] Erro inesperado: {e}")
                sleep(0.05 * attempt)

        self._log("[MODBUS] Falha na leitura")
        return None

    # ----------------------------------------------------------
    # WRITE MULTIPLE REGISTERS (0x10)
    # ----------------------------------------------------------

    def write_registers(
        self,
        slave: int,
        start: int,
        values: list[int],
    ) -> bool:

        count = len(values)
        byte_count = count * 2

        header = struct.pack(">BBHHB", slave, 0x10, start, count, byte_count)
        data = struct.pack(f">{count}H", *values)

        payload = header + data
        
        frame = add_crc(payload + self._matricula)

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                self._serial.reset_input_buffer()

                self._log("")
                self._log(f"[MODBUS] WRITE tentativa {attempt}/{self.MAX_RETRIES}")
                self._log(f"[MODBUS TX] {len(frame)} bytes: {_hex(frame)}")

                self._serial.write(frame)
                self._serial.flush()

                response = _read_exact(self._serial, 8)

                if response:
                    self._log(f"[MODBUS RX] {len(response)} bytes: {_hex(response)}")
                else:
                    self._log("[MODBUS RX] timeout")

                if len(response) < 8:
                    self._log("[MODBUS] Resposta de escrita incompleta")
                    continue

                if not check_crc(list(response)):
                    self._log("[MODBUS] CRC inválido na escrita")
                    continue

                if response[1] & 0x80:
                    codigo = response[2] if len(response) > 2 else 0
                    self._log(f"[MODBUS] Exceção MODBUS 0x{codigo:02X}")
                    continue

                self._log("[MODBUS] Escrita OK")
                return True

            except serial.SerialException as e:
                self._log(f"[MODBUS] Erro serial: {e}")
                sleep(0.05 * attempt)

            except Exception as e:
                self._log(f"[MODBUS] Erro inesperado: {e}")
                sleep(0.05 * attempt)

        self._log("[MODBUS] Falha na escrita")
        return False
    
    # ----------------------------------------------------------
    # SEND RAW CUSTOM PACKET
    # ----------------------------------------------------------
    def send_custom_packet(self, payload: bytes, expected_response_size: int = 256) -> bytes | None:
        """
        Envia um pacote de bytes customizado. 
        O CRC é calculado e concatenado automaticamente ao final do pacote.
        """
        # Calcula e adiciona o CRC correto da disciplina automaticamente
        frame = add_crc(payload)

        try:
            self._serial.reset_input_buffer()

            self._log("")
            self._log("[MODBUS TX CUSTOM] Enviando pacote customizado...")
            self._log(f"[MODBUS TX] {len(frame)} bytes: {_hex(frame)}")

            self._serial.write(frame)
            self._serial.flush()

            # Lê a resposta usando o timeout configurado na serial
            # Como o tamanho da resposta customizada pode variar, lemos até o limite informado
            response = self._serial.read(expected_response_size)

            if response:
                self._log(f"[MODBUS RX] {len(response)} bytes recebidos: {_hex(response)}")
                
                # Valida se o CRC da resposta está correto
                if check_crc(list(response)):
                    self._log("[MODBUS] CRC da resposta é VÁLIDO!")
                else:
                    self._log("[MODBUS] AVISO: CRC da resposta recebida é INVÁLIDO.")
                
                return response
            else:
                self._log("[MODBUS RX] timeout - nenhuma resposta recebida")
                return None

        except Exception as e:
            self._log(f"[MODBUS] Erro ao enviar pacote customizado: {e}")
            return None