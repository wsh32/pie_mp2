"""
serial_process.py: Runs serial communications in seperate process
"""

from multiprocessing import Process, Event, Queue
import queue
import time
import serial


class SerialProcess:
    def __init__(self, port, baudrate, logger_queue=None):
        self.logger = logging.getLogger("main")
        self.logger_queue = logger_queue

        self.port = port
        self.baudrate = baudrate

        self.write_queue = Queue()
        self.read_queue = Queue()
        self.kill_event = Event()
        self.process = Process(target=self._run)

        self.logger.info("Starting serial process")
        self.process.start()

    def _run(self):
        # Setup logger
        if self.logger_queue is not None:
            configure_client_logger(self.logger_queue)

        self.device = serial.Serial(self.port, self.baudrate)
        # flush all serial data
        self.device.reset_input_buffer()
        self.device.reset_output_buffer()

        initialized = False
        # spam echo until serial is synced
        while not self.kill_event.is_set() and not initialized:
            echo_num = 100
            echo_msg = format_serial_output(0, echo_num, 0, 0)
            self.device.write(echo_msg)

            time.sleep(0.1)

            while self.device.in_waiting > 0:
                read = self.device.read(1)
                if int.from_bytes(read, "big") == echo_num + 1:
                    # Read rest of message and reset
                    self.device.reset_input_buffer()
                    initialized = True
                    break

        while not self.kill_event.is_set():
            try:
                self.device.write(self.write_queue.get_nowait())
            except queue.Empty:
                pass

            if self.device.in_waiting > 0:
                self.read_queue.put(self.device.read(8))

    def kill(self):
        self.event.set()
        self.process.join()
        self.device.close()


def uint16_to_uint8_2(uint16):
    uint8_1 = uint16 & 0xff00 >> 8
    uint8_2 = uint16 & 0x00ff

    return (uint8_1, uint8_2)


def uint8_2_to_uint16(uint8_1, uint8_2):
    return uint8_1 << 8 + uint8_2


def format_serial_output(cmd, echo, yaw_cmd, pitch_cmd):
    yaw_cmd_1, yaw_cmd_2 = uint16_to_uint8_2(yaw_cmd)
    pitch_cmd_1, pitch_cmd_2 = uint16_to_uint8_2(pitch_cmd)
    return [cmd, echo, yaw_cmd_1, yaw_cmd_2, pitch_cmd_1, pitch_cmd_2]

