"""
math.py: Math utility functions to process raw data
"""

import numpy as np


def polar_to_cartesian(dist, pitch, yaw):
    """Returns the 3D point for the corresponding length and angle values
    Inputs:
        dist: Distance from the sensor to the object, in inches
        pitch: Pitch angle of the sensor, in radians
        yaw: Yaw angle of the sensor, in radians
    """

    return (dist * np.array([cos(pitch) * sin(yaw),
                             cos(pitch) * cos(yaw),
                             sin(pitch)]))


def sharp_ir_raw_to_distance(raw_measurement):
    distance_meters = 1
    return distance_meters

