"""
plot.py: Thread safe 3D plotting and visualization
"""

from multiprocessing import Process, Event, Queue
import logging
import queue

import matplotlib
import matplotlib.pyplot as plt

class Plotter:
    """
    Creates a new thread that asynchronously plots the data coming from the data
    queue
    """
    def __init__(self, color='blue'):
        self.logger = logging.getLogger("main")

        self.color = color

        self.data_queue = Queue()
        self.kill_event = Event()

        self.process = Process(target=self._run)

        self.logger.info("Starting plotter thread")
        self.process.start()

    def kill(self):
        self.logger.info("Killing plotter thread")
        self.kill_event.set()
        self.process.join()

    def _run(self):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        while not self.kill_event.is_set():
            try:
                data = self.data_queue.get(timeout=1)
            except queue.Empty:
                continue
            if len(data) != 3:
                # Expect that data has size 3
                self.logger.warning(f"Datapoint {data} is not size 3, skipping")
                continue

            ax.scatter3D(data[0], data[1], data[2], marker='.', color=self.color)
        plt.show()

