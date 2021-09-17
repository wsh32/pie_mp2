"""
run_scan.py: Runs the scanning action and generates a visualization
"""

import plot

import logging
import sys
import configparser
import argparse
import time
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Runs the scanning action")
    parser.add_argument('config_file', type=str, nargs="+")

    args = parser.parse_args()

    cfg = configparser.ConfigParser()
    cfg.read(args.config_file)

    # Setup logger
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("<%(levelname)s>\t%(asctime)s:\t%(message)s",
                                  datefmt='%I:%M:%S %p')

    if 'ConsoleLogger' in cfg:
        cout_handler = logging.StreamHandler(sys.stdout)
        cout_handler.setLevel(cfg['ConsoleLogger']['level'])
        cout_handler.setFormatter(formatter)
        logger.addHandler(cout_handler)

    if 'FileLogger' in cfg:
        file_handler = logging.FileHandler(cfg['FileLogger']['filename'])
        file_handler.setLevel(cfg['FileLogger']['level'])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Start main loop
    logger.info("Starting main loop")

    # Start plotter
    plotter = plot.Plotter()

    for i in range(100):
        plotter.data_queue.put(np.random.rand(3))
        time.sleep(0.1)

