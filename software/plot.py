"""
plot.py: Thread safe 3D plotting and visualization
"""

from queue import Queue
from threading import Thread, Event
import matplotlib.pyplot as plt
import logging


class Plotter:
    """
    Creates a new thread that asynchronously plots the data coming from the data
    queue
    """
    def __init__(color='blue'):
        self.logger = logging.getLogger("main")

        self.color = color

        self.data_queue = Queue()
        self.kill_event = Event()

        self.thread = Thread(target=self._run)

        self.logger.info("Starting plotter thread")
        self.thread.start()

    def kill():
        self.logger.info("Killing plotter thread")
        self.event.set()
        self.thread.join()

    def _run():
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        while not self.kill_event.is_set():
            data = self.data_queue.get()
            if len(data) != 3:
                # Expect that data has size 3
                logger.warning(f"Datapoint {data} is not size 3, skipping")
                continue

            ax.scatter3D(data[0], data[1], data[2], marker='.', color=self.color)

