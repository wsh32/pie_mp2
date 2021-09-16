"""
run_scan.py: Runs the scanning action and generates a visualization
"""

import logging
import sys
import configparser
import argparse

LOG = logging.getLogger("main")

def setup_logger(logger, log_filename=None):
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(levelname)s %(asctime)s:\t%(message)s",
                                  datefmt='%I:%M:%S %p')

    cout_handler = logging.StreamHandler(sys.stdout)
    cout_handler.setLevel(logging.DEBUG)
    cout_handler.setFormatter(formatter)
    logger.addHandler(cout_handler)

    if log_filename:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Runs the scanning action")
    parser.add_argument('config_file', type=str)

    args = parser.parse_args()

    cfg = configparser.ConfigParser()
    cfg.read(args.config_file)

    setup_logger(LOG, cfg['logger'])
    LOG.info("Starting main loop")


