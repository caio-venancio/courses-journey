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


def _crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def _build_frame(payload: bytes, matricula: bytes) -> bytes:
    """Concatena payload + matrícula + CRC."""
    frame = payload + matricula
    crc = _crc16(frame)
    return frame + struct.pack("<H", crc)


def _validate_response(data: bytes) -> bool:
    if len(data) < 4:
        return False
    crc_calc = _crc16(data[:-2])
    crc_recv = struct.unpack("<H", data[-2:])[0]
    return crc_calc == crc_recv


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
        payload = struct.pack(">BBHH", slave, 0x03, start, count)
        frame = _build_frame(payload, self._matricula)

        for attempt in range(self.MAX_RETRIES):
            try:
                self._serial.reset_input_buffer()
                self._serial.write(frame)
                # Resposta esperada: slave(1) + fc(1) + byte_count(1) + data(2*count) + crc(2)
                expected = 3 + count * 2 + 2
                response = self._serial.read(expected)

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
                # Resposta: slave(1)+fc(1)+start(2)+count(2)+crc(2) = 8 bytes
                response = self._serial.read(8)

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
