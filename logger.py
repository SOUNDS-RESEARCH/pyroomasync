import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from pyroomacoustics.doa import circ_dist

from plotter import (
    plot_dirac, plot_room, plot_microphone_signals
)
from settings import SR

def _azimuth_to_degrees(azimuth_in_radians):
    return azimuth_in_radians / np.pi * 180.0

def _estimation_error(estimated, ground_truth):
    return _azimuth_to_degrees(circ_dist(ground_truth, estimated))

def _create_output_dir(estimator_name):
    if not os.path.exists("results/"):
        os.mkdir("results/")
    if not os.path.exists("results/" + estimator_name):
        os.mkdir("results/" + estimator_name)


def log_estimation_results(estimator, ground_truth):
    result = estimator.estimator.azimuth_recon
    _create_output_dir(estimator.estimator_name)
    
    plot_dirac(
        estimator.estimator,
        "results/" + estimator.estimator_name + "/dirac.png")

    df = pd.DataFrame.from_records([{
        "Recovered azimuth": _azimuth_to_degrees(result)[0],
        "Error": _estimation_error(result, ground_truth)[0]}]
    )

    df.to_csv("results/" + estimator.estimator_name + "/metrics.csv")

def log_room(room):
    if not os.path.exists("results/"):
        os.mkdir("results/")
    
    plot_room(room, "results/room.png")

    room.plot_rir()
    plt.savefig("results/mic_rir.png")

    mic_signals = room.mic_array.signals
    plot_microphone_signals(mic_signals, "results/mic_signals.png")
    for i, mic_signal in enumerate(mic_signals):
        sf.write(
            "results/mic_signals_{}.wav".format(i), mic_signal, SR)