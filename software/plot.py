"""
plot.py: Multiprocessing compatible 3D plotting and visualization
"""

from multiprocessing_logger import configure_client_logger

from multiprocessing import Process, Event, Queue
import logging
import queue

import matplotlib
import matplotlib.pyplot as plt

class Plotter3D:
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
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        min_z = None
        max_z = None
        # ax.set_aspect('equal')
        x = []
        y = []
        z = []
        while not self.kill_event.is_set():
            try:
                data = self.data_queue.get_nowait()
            except queue.Empty:
                plt.pause(0.01)
                continue

            color = self.color
            if len(data) == 4:
                # If length of 4, use 4th point as color
                color = data[3]
            elif len(data) != 3:
                # Expect that data has size 3
                self.logger.warning(f"Datapoint {data} has invalid size, skipping")
                continue

            if min_x is not None:
                min_x = min(min_x, data[0])
                max_x = max(max_x, data[0])
                min_y = min(min_y, data[1])
                max_y = max(max_y, data[1])
                min_z = min(min_z, data[2])
                max_z = max(max_z, data[2])
            else:
                min_x = data[0]
                max_x = data[0]
                min_y = data[1]
                max_y = data[1]
                min_z = data[2]
                max_z = data[2]

            aspect_ratio = (max(max_x - min_x, 1),
                            max(max_y - min_y, 1),
                            max(max_z - min_z, 1))
            self.logger.warning(f"New aspect ratio: {aspect_ratio}")
            ax.set_box_aspect(aspect_ratio)

            self.logger.debug(f"Plotting data:\t{data}")

            x.append(data[0])
            y.append(data[1])
            z.append(data[2])

            ax.scatter3D(data[0], data[1], data[2], marker='.', color=color)
            """
            if len(x) < 3:
                continue
            ax.plot_trisurf(x, y, z, linewidth=0.2)
            """
            plt.show(block=False)


class Plotter2D:
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

        while not self.kill_event.is_set():
            try:
                data = self.data_queue.get_nowait()
            except queue.Empty:
                plt.pause(0.01)
                continue

            color = self.color

            self.logger.warning(f"New aspect ratio: {aspect_ratio}")

            self.logger.debug(f"Plotting data:\t{data}")
            plt.scatter(data[0], data[1], marker='.', color=color)
            plt.show(block=False)

