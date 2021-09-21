"""
serial_process.py: Runs serial communications in seperate process
"""

from multiprocessing import Process, Event, Queue


class SerialProcess:
    def __init__(self, device):
        self.device = device

