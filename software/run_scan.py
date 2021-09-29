"""
run_scan.py: Runs the scanning action and generates a visualization
"""

import plot
import multiprocessing_logger
import serial_process
import math_utils

import logging
import configparser
import argparse
import time
import numpy as np


def run_path_sweep(horizontal_samples, horizontal_left_bound,
                   horizontal_right_bound, vertical_samples,
                   vertical_top_bound, vertical_bottom_bound,
                   serial_write_queue, serial_read_queue, plot_data_queue,
                   min_distance_plot=11, max_distance_plot=15,
                   yaw_calibration=None, pitch_calibration=None):
    x = np.linspace(horizontal_left_bound, horizontal_right_bound,
                    horizontal_samples)
    y = np.linspace(vertical_top_bound, vertical_bottom_bound,
                    vertical_samples)

    direction = False  # False = left to right, True = right to left
    for y_index, y_pos in enumerate(y):
        pitch_cmd = int(y_pos)
        for x_index, x_pos in enumerate(x):
            x_index_corrected = x_index
            if direction:
                # Right to left: Invert index
                x_index_corrected = horizontal_samples - x_index - 1
            yaw_cmd = int(x[x_index_corrected])

            logger.info(f"Current command: {pitch_cmd}\t{yaw_cmd}")

            yaw_cmd_calibrated = yaw_cmd
            pitch_cmd_calibrated = pitch_cmd
            if yaw_calibration:
                yaw_cmd_calibrated = int(math_utils.apply_motor_calibration(
                    yaw_cmd, *yaw_calibration))
            if pitch_calibration:
                pitch_cmd_calibrated = int(math_utils.apply_motor_calibration(
                    pitch_cmd, *pitch_calibration))

            serial_write_queue.put(
                serial_process.format_serial_output(
                    1, 0, yaw_cmd_calibrated, pitch_cmd_calibrated))

            read_echo, read_led, read_dist = serial_process.parse_serial_input(
                serial_read_queue.get())

            logger.info(
                f"Read serial data: {read_echo}\t{read_led}\t{read_dist}")

            pitch_cmd_rad = np.deg2rad(pitch_cmd)
            yaw_cmd_rad = np.deg2rad(yaw_cmd)

            dist_in = math_utils.sharp_ir_raw_to_distance(read_dist)

            x_read, y_read, z_read = math_utils.polar_to_cartesian(
                dist_in, pitch_cmd_rad, yaw_cmd_rad)

            logger.info(f"Position: {x_read}\t{y_read}\t{z_read}")
            if y_read > min_distance_plot and y_read < max_distance_plot:
                plot_data_queue.put((x_read, y_read, z_read))

        direction = not direction


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

    # Start serial
    if 'Serial' in cfg:
        arduino_process = serial_process.SerialProcess.from_cfg(
            cfg, logger_queue=logger_process.logger_queue)

    # Start plotter
    plotter_process = plot.Plotter3D(logger_queue=logger_process.logger_queue)

    # Zhu Li! Do the thing!
    if 'Path' in cfg:
        if cfg['Path']['type'] == 'sweep':
            horizontal_samples = int(cfg['Path']['horizontal_samples'])
            horizontal_left_bound = int(cfg['Path']['horizontal_left_bound'])
            horizontal_right_bound = int(cfg['Path']['horizontal_right_bound'])

            vertical_samples = int(cfg['Path']['vertical_samples'])
            vertical_top_bound = int(cfg['Path']['vertical_top_bound'])
            vertical_bottom_bound = int(cfg['Path']['vertical_bottom_bound'])

            if 'YawCalibration' in cfg:
                yaw_calibration = (int(cfg['YawCalibration']['left']),
                                   int(cfg['YawCalibration']['middle']),
                                   bool(cfg['YawCalibration']['invert']))
            else:
                yaw_calibration = None

            if 'PitchCalibration' in cfg:
                pitch_calibration = (int(cfg['PitchCalibration']['up']),
                                     int(cfg['PitchCalibration']['middle']),
                                     bool(cfg['PitchCalibration']['invert']))
            else:
                pitch_calibration = None

            if 'Plot' in cfg:
                min_distance_plot = float(cfg['Plot']['min_distance'])
                max_distance_plot = float(cfg['Plot']['max_distance'])

                run_path_sweep(horizontal_samples, horizontal_left_bound,
                               horizontal_right_bound, vertical_samples,
                               vertical_top_bound, vertical_bottom_bound,
                               arduino_process.write_queue,
                               arduino_process.read_queue,
                               plotter_process.data_queue,
                               min_distance_plot=min_distance_plot,
                               max_distance_plot=max_distance_plot,
                               yaw_calibration=yaw_calibration,
                               pitch_calibration=pitch_calibration)
            else:
                run_path_sweep(horizontal_samples, horizontal_left_bound,
                               horizontal_right_bound, vertical_samples,
                               vertical_top_bound, vertical_bottom_bound,
                               arduino_process.write_queue,
                               arduino_process.read_queue,
                               plotter_process.data_queue,
                               yaw_calibration=yaw_calibration,
                               pitch_calibration=pitch_calibration)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Kill everything
        plotter_process.kill()
        arduino_process.kill()
        logger_process.kill()

