"""
run_scan.py: Runs the scanning action and generates a visualization
"""

import plot
import multiprocessing_logger

import logging
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
    configurator = multiprocessing_logger.LoggerFromCfg(cfg)
    logger_process = multiprocessing_logger.ProcessLogger(configurator)
    multiprocessing_logger.configure_client_logger(logger_process.logger_queue)

    logger = logging.getLogger("main")

    # Start main loop
    logger.info("Starting main loop")

    # Start plotter
    plotter_process = plot.Plotter(logger_queue=logger_process.logger_queue)

    for i in range(100):
        plotter_process.data_queue.put(np.random.rand(3) * 100)
        time.sleep(0.1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Kill everything
        plotter_process.kill()
        logger_process.kill()

