"""
math.py: Math utility functions to process raw data
"""

import numpy as np


def rotate_2d(rot):
    """Returns the rotation matrix
    Inputs:
        rot: Angle to rotate, in radians
    """
    return np.array([
        [np.cos(rot), -np.sin(rot)],
        [np.sin(rot), np.cos(rot)],
    ])


def rotate_3d_x(rot):
    """Returns the rotation matrix around the X axis
    Inputs:
        rot: Angle to rotate, in radians
    """
    return np.array([
        [1, 0, 0],
        [0, np.cos(rot), -np.sin(rot)],
        [0, np.sin(rot), np.cos(rot)],
    ])


def rotate_3d_y(rot):
    """Returns the rotation matrix around the Y axis
    Inputs:
        rot: Angle to rotate, in radians
    """
    return np.array([
        [np.cos(rot), 0, -np.sin(rot)],
        [0, 1, 0],
        [0, np.sin(rot), np.cos(rot)],
    ])


def rotate_3d_z(rot):
    """Returns the rotation matrix around the Z axis
    Inputs:
        rot: Angle to rotate, in radians
    """
    return np.array([
        [np.cos(rot), -np.sin(rot), 0],
        [np.sin(rot), np.cos(rot), 0],
        [0, 0, 1],
    ])

