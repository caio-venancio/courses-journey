"""
modbus.py — MODBUS RTU sobre RS485 via pyserial.

Funções suportadas:
  0x03  Read Holding Registers
  0x10  Write Multiple Registers

O enunciado exige que os 6 últimos dígitos da matrícula sejam
acrescentados como bytes crus ANTES do CRC em cada mensagem TX.
Passe `matricula` (string de 6 dígitos, ex.: "654321") ao criar
o objeto ModbusRTU.
"""

import struct
import serial
from time import sleep


# ============= CRC do projeto (inicialização 0x0000) =============
# Tabela oficial usada na disciplina (substitui o CRC padrão do Modbus)
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


def _crc16_byte(crc: int, byte: int) -> int:
    """Atualiza o CRC com um byte usando a tabela do projeto."""
    return ((crc & 0xFF00) >> 8) ^ CRC16_TABLE[(crc & 0x00FF) ^ (byte & 0x00FF)]


def _calcula_crc(data: bytes) -> int:
    """CRC conforme especificação da disciplina: inicialização 0x0000."""
    crc = 0
    for b in data:
        crc = _crc16_byte(crc, b)
    return crc & 0xFFFF


def _build_frame(payload: bytes, matricula: bytes) -> bytes:
    """Concatena payload + matrícula + CRC."""
    frame = payload + matricula
    crc = _calcula_crc(frame)
    # CRC em little-endian (byte baixo primeiro), mesmo que Modbus padrão
    return frame + struct.pack("<H", crc)


def _validate_response(data: bytes) -> bool:
    """Verifica o CRC da resposta usando a rotina do projeto."""
    if len(data) < 4:
        return False
    crc_calc = _calcula_crc(data[:-2])
    crc_recv = struct.unpack("<H", data[-2:])[0]
    return crc_calc == crc_recv


def _read_exact(ser, size: int) -> bytes:
    """Lê exatamente 'size' bytes da porta serial."""
    buf = bytearray()
    while len(buf) < size:
        chunk = ser.read(size - len(buf))
        if not chunk:
            break
        buf.extend(chunk)
    return bytes(buf)


class ModbusRTU:
    MAX_RETRIES = 3

    def __init__(self, port: str, baudrate: int = 115200,
                 timeout: float = 0.3, matricula: str = "000000"):
        self._serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout,
        )
        # Matrícula: 6 bytes crus (não ASCII)
        digits = [int(c) for c in matricula.zfill(6)[-6:]]
        self._matricula = bytes(digits)

    def close(self):
        if self._serial.is_open:
            self._serial.close()

    # ------------------------------------------------------------------
    # Função 0x03 — Read Holding Registers
    # ------------------------------------------------------------------

    def read_registers(self, slave: int, start: int, count: int) -> list[int] | None:
        # Empacotamento conforme esperado pelo simulador da disciplina:
        # count é enviado como dois bytes separados (low, high).
        payload = struct.pack(">BBHBB", slave, 0x03, start, count & 0xFF, (count >> 8) & 0xFF)
        frame = _build_frame(payload, self._matricula)

        for attempt in range(self.MAX_RETRIES):
            try:
                self._serial.reset_input_buffer()
                self._serial.write(frame)
                self._serial.flush()
                # Resposta esperada: slave(1) + fc(1) + byte_count(1) + data(2*count) + crc(2)
                expected = 3 + count * 2 + 2
                response = _read_exact(self._serial, expected)

                if len(response) < expected:
                    continue
                if not _validate_response(response):
                    continue
                if response[1] & 0x80:  # exceção MODBUS
                    continue

                # Desempacotar registradores
                regs = []
                for i in range(count):
                    offset = 3 + i * 2
                    regs.append(struct.unpack(">H", response[offset:offset + 2])[0])
                return regs

            except serial.SerialException:
                sleep(0.05 * (attempt + 1))

        return None

    # ------------------------------------------------------------------
    # Função 0x10 — Write Multiple Registers
    # ------------------------------------------------------------------

    def write_registers(self, slave: int, start: int, values: list[int]) -> bool:
        count = len(values)
        byte_count = count * 2
        header = struct.pack(">BBHHB", slave, 0x10, start, count, byte_count)
        data = struct.pack(f">{count}H", *values)
        payload = header + data
        frame = _build_frame(payload, self._matricula)

        for attempt in range(self.MAX_RETRIES):
            try:
                self._serial.reset_input_buffer()
                self._serial.write(frame)
                self._serial.flush()
                # Resposta: slave(1)+fc(1)+start(2)+count(2)+crc(2) = 8 bytes
                response = _read_exact(self._serial, 8)

                if len(response) < 8:
                    continue
                if not _validate_response(response):
                    continue
                if response[1] & 0x80:
                    continue
                return True

            except serial.SerialException:
                sleep(0.05 * (attempt + 1))

        return False