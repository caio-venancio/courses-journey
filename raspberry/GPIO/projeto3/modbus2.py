"""
modbus.py — MODBUS RTU sobre RS485 via pyserial.

Funções suportadas:
  0x03  Read Holding Registers
  0x10  Write Multiple Registers

Versão com logs de debug.
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
    frame = payload + matricula
    crc = _crc16(frame)

    return frame + struct.pack("<H", crc)


def _validate_response(data: bytes) -> bool:
    if len(data) < 4:
        return False

    crc_calc = _crc16(data[:-2])
    crc_recv = struct.unpack("<H", data[-2:])[0]

    return crc_calc == crc_recv


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
        timeout: float = 0.3,
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

        self._log(
            f"[MODBUS] Porta aberta: {port} @ {baudrate} baud"
        )

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

        payload = struct.pack(">BBHH", slave, 0x03, start, count)

        frame = _build_frame(
            payload,
            self._matricula
        )

        for attempt in range(1, self.MAX_RETRIES + 1):

            try:
                self._serial.reset_input_buffer()

                self._log("")
                self._log(
                    f"[MODBUS] READ tentativa "
                    f"{attempt}/{self.MAX_RETRIES}"
                )

                self._log(
                    f"[MODBUS TX] {len(frame)} bytes: "
                    f"{_hex(frame)}"
                )

                self._serial.write(frame)
                self._serial.flush()

                expected = 3 + count * 2 + 2

                response = _read_exact(
                    self._serial,
                    expected
                )

                if response:
                    self._log(
                        f"[MODBUS RX] {len(response)} bytes: "
                        f"{_hex(response)}"
                    )
                else:
                    self._log(
                        "[MODBUS RX] timeout"
                    )

                if len(response) < expected:
                    self._log(
                        f"[MODBUS] Resposta incompleta "
                        f"({len(response)}/{expected} bytes)"
                    )
                    continue

                if not _validate_response(response):
                    crc_calc = _crc16(response[:-2])
                    crc_recv = struct.unpack(
                        "<H",
                        response[-2:]
                    )[0]

                    self._log(
                        f"[MODBUS] CRC inválido "
                        f"(calc=0x{crc_calc:04X}, "
                        f"recv=0x{crc_recv:04X})"
                    )

                    continue

                if response[1] & 0x80:
                    codigo = (
                        response[2]
                        if len(response) > 2
                        else 0
                    )

                    self._log(
                        f"[MODBUS] Exceção MODBUS "
                        f"0x{codigo:02X}"
                    )

                    continue

                regs = []

                for i in range(count):
                    offset = 3 + i * 2

                    valor = struct.unpack(
                        ">H",
                        response[offset:offset + 2]
                    )[0]

                    regs.append(valor)

                self._log(
                    "[MODBUS] Registros lidos:"
                )

                for i, reg in enumerate(regs):
                    self._log(
                        f"    [{start+i}] = "
                        f"0x{reg:04X} ({reg})"
                    )

                return regs

            except serial.SerialException as e:

                self._log(
                    f"[MODBUS] Erro serial: {e}"
                )

                sleep(0.05 * attempt)

            except Exception as e:

                self._log(
                    f"[MODBUS] Erro inesperado: {e}"
                )

                sleep(0.05 * attempt)

        self._log(
            "[MODBUS] Falha na leitura"
        )

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

        header = struct.pack(
            ">BBHHB",
            slave,
            0x10,
            start,
            count,
            byte_count,
        )

        data = struct.pack(
            f">{count}H",
            *values
        )

        payload = header + data

        frame = _build_frame(
            payload,
            self._matricula
        )

        for attempt in range(1, self.MAX_RETRIES + 1):

            try:
                self._serial.reset_input_buffer()

                self._log("")
                self._log(
                    f"[MODBUS] WRITE tentativa "
                    f"{attempt}/{self.MAX_RETRIES}"
                )

                self._log(
                    f"[MODBUS TX] {len(frame)} bytes: "
                    f"{_hex(frame)}"
                )

                self._serial.write(frame)
                self._serial.flush()

                response = _read_exact(
                    self._serial,
                    8
                )

                if response:
                    self._log(
                        f"[MODBUS RX] {len(response)} bytes: "
                        f"{_hex(response)}"
                    )
                else:
                    self._log(
                        "[MODBUS RX] timeout"
                    )

                if len(response) < 8:
                    self._log(
                        "[MODBUS] Resposta "
                        "de escrita incompleta"
                    )

                    continue

                if not _validate_response(response):
                    crc_calc = _crc16(response[:-2])
                    crc_recv = struct.unpack(
                        "<H",
                        response[-2:]
                    )[0]

                    self._log(
                        f"[MODBUS] CRC inválido "
                        f"(calc=0x{crc_calc:04X}, "
                        f"recv=0x{crc_recv:04X})"
                    )

                    continue

                if response[1] & 0x80:
                    codigo = (
                        response[2]
                        if len(response) > 2
                        else 0
                    )

                    self._log(
                        f"[MODBUS] Exceção MODBUS "
                        f"0x{codigo:02X}"
                    )

                    continue

                self._log(
                    "[MODBUS] Escrita OK"
                )

                return True

            except serial.SerialException as e:

                self._log(
                    f"[MODBUS] Erro serial: {e}"
                )

                sleep(0.05 * attempt)

            except Exception as e:

                self._log(
                    f"[MODBUS] Erro inesperado: {e}"
                )

                sleep(0.05 * attempt)

        self._log(
            "[MODBUS] Falha na escrita"
        )

        return False