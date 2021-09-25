"""
multiprocessing_logger.py: Enables multiprocessing support with the python
logging module using a QueueLogger
"""

import logging
import logging.handlers
from multiprocessing import Process, Event, Queue
import queue
import time
import sys


class ProcessLogger:
    def __init__(self, logger_configurator):
        self.configurator = logger_configurator

        self.logger_queue = Queue()
        self.kill_event = Event()
        self.process = Process(target=self._run)
        self.process.start()

    def _run(self):
        # Setup logger
        self.logger = logging.getLogger("logger_out")
        self.configurator.configure(self.logger)

        self.logger.info("Starting logger process")

        while not self.kill_event.is_set():
            try:
                record = self.logger_queue.get_nowait()
            except queue.Empty:
                time.sleep(0.1)
                continue
            if record is None:
                break
            self.logger.handle(record)

    def kill(self):
        self.kill_event.set()
        self.process.join()


def configure_client_logger(logger_queue, level=logging.DEBUG):
    handler = logging.handlers.QueueHandler(logger_queue)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


class LoggerFromCfg:
    def __init__(self, cfg):
        self.cfg = cfg

    def configure(self, logger):
        formatter = logging.Formatter(self.cfg['Logger']['format'],
                                      datefmt=self.cfg['Logger']['datefmt'])

        if 'ConsoleLogger' in self.cfg:
            cout_handler = logging.StreamHandler(sys.stdout)
            cout_handler.setLevel(self.cfg['ConsoleLogger']['level'])
            cout_handler.setFormatter(formatter)
            logger.addHandler(cout_handler)

        if 'FileLogger' in self.cfg:
            file_handler = logging.FileHandler(self.cfg['FileLogger']['filename'])
            file_handler.setLevel(self.cfg['FileLogger']['level'])
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.setLevel(self.cfg['Logger']['level'])

