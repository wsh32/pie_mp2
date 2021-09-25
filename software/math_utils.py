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
    dist = ((pow((96525*reading)/1088 - 889849181450345845042039/98863019020037128192, 2) + 4320918025146633092526075044890718306748939018668359539455369/6599702224362321183928599545720790629314745847412424704)**(1./2.) - (96525*reading)/1088 + 889849181450345845042039/98863019020037128192)**(1./3.) - 162876592769475220889/(1875749244799811584*((((96525*reading)/1088 - 889849181450345845042039/98863019020037128192)**(2.) + 4320918025146633092526075044890718306748939018668359539455369/6599702224362321183928599545720790629314745847412424704)**(1./2.) - (96525*reading)/1088 + 889849181450345845042039/98863019020037128192)**(1./3.)) + 20779/448
    return dist

