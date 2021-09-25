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

    return (dist * np.array([np.cos(pitch - np.pi / 2) * np.sin(yaw),
                             np.cos(pitch - np.pi / 2) * np.cos(yaw),
                             np.sin(pitch - np.pi / 2)]))


def sharp_ir_raw_to_distance(reading):
    dist = ((((96525*reading)/1088 - 9008)**2 + 654710)**(1/2) - (96525*reading)/1088 + 9008)**(1/3) - 16287/(187*((((96525*reading)/1088 - 9008)**2 + 654710)**(1/2) - (96525*reading)/1088 + 9008)**(1/3)) + 20779/448
    return dist

