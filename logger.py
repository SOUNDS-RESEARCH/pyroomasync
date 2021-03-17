import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from pyroomacoustics.doa import circ_dist

from plotter import plot_dirac, plot_room

def _azimuth_to_degrees(azimuth_in_radians):
    return azimuth_in_radians / np.pi * 180.0

def _estimation_error(estimated, ground_truth):
    return _azimuth_to_degrees(circ_dist(ground_truth, estimated))

def create_output_dir(estimator_name):
    if not os.path.exists("results/"):
        os.mkdir("results/")
    if not os.path.exists("results/" + estimator_name):
        os.mkdir("results/" + estimator_name)


def log_estimation_results(estimator, ground_truth):
    result = estimator.estimator.azimuth_recon
    create_output_dir(estimator.estimator_name)
    
    plot_dirac(estimator,
               ground_truth,
               "results/" + estimator.estimator_name + "/dirac.png")
    
    
    df = pd.DataFrame({
        "Recovered azimuth": _azimuth_to_degrees(result),
        "Error": _estimation_error(result, ground_truth)}
    )

    df.to_csv("results/" + estimator.estimator_name + "/metrics.csv")

def log_room(room):
    if not os.path.exists("results/"):
        os.mkdir("results/")
    
    plot_room(room, "results/room.png")