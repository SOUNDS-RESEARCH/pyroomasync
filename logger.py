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


def log_error(result, ground_truth, output_dir):
    
    df = pd.DataFrame.from_records([{
        "Recovered azimuth": _azimuth_to_degrees(result)[0],
        "Error": _estimation_error(result, ground_truth)[0]}]
    )

    df.to_csv(os.path.join(output_dir, "metrics.csv"))


def log_estimation_results(output_dir, estimator, ground_truth):

    result = estimator.estimator.azimuth_recon

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


    plot_dirac(
        estimator.estimator,
        os.path.join(output_dir, "dirac.png"),
        ground_truth)

    log_error(result, ground_truth, output_dir)

def log_simulation_results(room, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    plot_room(room, os.path.join(output_dir, "room.png"))

    room.plot_rir()
    plt.savefig(os.path.join(output_dir, "mic_rir.png"))

    mic_signals = room.mic_array.signals
    plot_microphone_signals(mic_signals, os.path.join(output_dir, "mic_signals.png"))
    for i, mic_signal in enumerate(mic_signals):
        sf.write(
            os.path.join(output_dir, "mic_signals_{}.wav".format(i)), mic_signal, SR)