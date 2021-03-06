"""
serial_process.py: Runs serial communications in seperate process
"""

from multiprocessing_logger import configure_client_logger

from multiprocessing import Process, Event, Queue

import queue
import time
import serial
import logging

from serial.tools import list_ports


arduino_ids = ((0x2341, 0x0043), (0x2341, 0x0001),
               (0x2A03, 0x0043), (0x2341, 0x0243),
               (0x0403, 0x6001), (0x1A86, 0x7523))


def find_arduino_port():
    devices = list_ports.comports()
    for device in devices:
        if (device.vid, device.pid) in arduino_ids:
            return device.device


class SerialProcess:
    def __init__(self, port=None, baudrate=115200, logger_queue=None):
        self.logger = logging.getLogger("main")
        self.logger_queue = logger_queue

        self.port = port
        self.baudrate = baudrate
        self.device = None

        self.write_queue = Queue()
        self.read_queue = Queue()
        self.kill_event = Event()
        self.process = Process(target=self._run)

        self.logger.info("Starting serial process")
        self.process.start()

    @staticmethod
    def from_cfg(cfg, logger_queue=None):
        port = None
        if "port" in cfg['Serial']:
            port = cfg['Serial']['port']

        baudrate = 115200
        if "baudrate" in cfg['Serial']:
            baudrate = int(cfg['Serial']['baudrate'])

        return SerialProcess(port=port, baudrate=baudrate,
                             logger_queue=logger_queue)

    def _run(self):
        # Setup logger
        if self.logger_queue is not None:
            configure_client_logger(self.logger_queue)

        if not self.port:
            # If port is None, autofind arduino
            self.port = find_arduino_port()

        self.device = serial.Serial(self.port, self.baudrate)
        logging.info(f"Opening serial device on {self.port}")
        # flush all serial data
        self.device.reset_input_buffer()
        self.device.reset_output_buffer()

        initialized = False
        # spam echo until serial is synced
        while not self.kill_event.is_set() and not initialized:
            echo_num = 100
            echo_msg = format_serial_output(0, echo_num, 0, 0)
            logging.info(f"Write message: {echo_msg}")
            self.device.write(echo_msg)

            time.sleep(0.1)

            while self.device.in_waiting > 0:
                read = self.device.read(1)
                logging.info(f"Read message: {read}")
                if int.from_bytes(read, "big") == echo_num:
                    # Read rest of message and reset
                    self.device.reset_input_buffer()
                    initialized = True
                    break

        self.logger.info(
            "Serial connected and initialized. Starting communications...")

        while not self.kill_event.is_set():
            try:
                message = self.write_queue.get_nowait()
                self.device.write(message)
                logging.info(f"Wrote message: {message}")
            except queue.Empty:
                pass

            if self.device.in_waiting > 0:
                message = self.device.read(8)
                logging.info(f"Read message: {list(message)}")
                self.read_queue.put(message)

        self.device.close()

    def kill(self):
        self.logger.info("Killing serial process")
        self.kill_event.set()
        self.process.join()


def uint16_to_uint8_2(uint16):
    uint8_1 = (uint16 & 0xff00) >> 8
    uint8_2 = uint16 & 0x00ff

    return (uint8_1, uint8_2)


def uint8_2_to_uint16(uint8_1, uint8_2):
    return (uint8_1 << 8) + uint8_2


def format_serial_output(cmd, echo, yaw_cmd, pitch_cmd):
    return [cmd, echo, yaw_cmd, pitch_cmd]


def parse_serial_input(serial_input):
    echo = serial_input[0]
    led_status = serial_input[1]
    distance_measurement = uint8_2_to_uint16(serial_input[2], serial_input[3])

    return echo, led_status, distance_measurement

