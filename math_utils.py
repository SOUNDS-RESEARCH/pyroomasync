import numpy as np
from pyroomacoustics.doa import circ_dist

def azimuth_to_degrees(azimuth_in_radians):
    return azimuth_in_radians / np.pi * 180.0

def estimation_error(estimated, ground_truth):
    return azimuth_to_degrees(circ_dist(ground_truth, estimated))
