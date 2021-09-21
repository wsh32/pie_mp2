"""
device.py: Serial communications driver
"""

from serial import Serial, SerialException
from serial.tools import list_ports
from threading import Lock
import struct


class Device:
    def __init__(self, autodetect, baudrate, port=None):
        self.read_lock = Lock()
        self.write_lock = Lock()
        self._ser = Serial()
        self._ser.baudrate = baudrate
        if not port:
            ports = list(list_ports.grep(r'.*{}.*'.format(autodetect)))
            if len(ports) == 0:
                raise SerialException(f"Could not locate USB device with name \
                                      {autodetect}. Devices connected: \
                                      {list_ports.comports()}")
            self._ser.port = list(ports[0])[0]
        else:
            self._ser.port = port

        self._ser.open()

    def write(self, data):
        with self.write_lock:
            self._ser.write(data)

    def read(self, buffer_len=1, timeout=None):
        with self.read_lock:
            self._ser.timeout = timeout
            response = self._ser.read(buffer_len)
            return response

    def read_line(self, timeout=None):
        with self.read_lock:
            self._ser.timeout = timeout
            response = self._ser.readline()
            return response

    def close(self):
        self._ser.close()

    def open(self):
        self._ser.open()

    def flush_input(self):
        self._ser.flushInput()

    def flush_output(self):
        self._ser.flushOutput()

    def flush_all(self):
        self._ser.flush()

    def in_waiting(self):
        return self._ser.in_waiting()

