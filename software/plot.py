"""
plot.py: Multiprocessing compatible 3D plotting and visualization
"""

from multiprocessing_logger import configure_client_logger

from multiprocessing import Process, Event, Queue
import logging
import queue

import matplotlib
import matplotlib.pyplot as plt

class Plotter:
    """
    Creates a new process that asynchronously plots the data coming from the data
    queue
    """
    def __init__(self, logger_queue=None, color='blue'):
        self.logger = logging.getLogger("main")
        self.logger_queue = logger_queue

        self.color = color

        self.data_queue = Queue()
        self.kill_event = Event()

        self.process = Process(target=self._run)

        self.logger.info("Starting plotter process")
        self.process.start()

    def kill(self):
        self.logger.info("Killing plotter process")
        self.kill_event.set()
        self.process.join()

    def _run(self):
        # Setup logger
        if self.logger_queue is not None:
            configure_client_logger(self.logger_queue)

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        while not self.kill_event.is_set():
            try:
                data = self.data_queue.get_nowait()
            except queue.Empty:
                plt.pause(0.1)
                continue

            color = self.color
            if len(data) == 4:
                # If length of 4, use 4th point as color
                color = data[3]
            elif len(data) != 3:
                # Expect that data has size 3
                self.logger.warning(f"Datapoint {data} has invalid size, skipping")
                continue

            self.logger.debug(f"Plotting data:\t{data}")
            ax.scatter3D(data[0], data[1], data[2], marker='.', color=color)
            plt.show(block=False)

