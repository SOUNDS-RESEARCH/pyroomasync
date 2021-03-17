import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from pyroomacoustics.doa import circ_dist


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
    estimator.polar_plt_dirac()

    create_output_dir(estimator.estimator_name)
    plt.savefig("results/" + estimator.estimator_name + "/dirac.png")
    # estimator.azimuth_recon contains the reconstructed location of the source
    print(_azimuth_to_degrees(result), type(_azimuth_to_degrees(result)))
    
    df = pd.DataFrame({
        "Recovered azimuth": _azimuth_to_degrees(result),
        "Error": _estimation_error(result, ground_truth)}
    )

    df.to_csv("results/" + estimator.estimator_name + "/metrics.csv",)