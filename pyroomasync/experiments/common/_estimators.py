import numpy as np
import matplotlib.pyplot as plt
import pyroomacoustics as pra
from scipy.signal import fftconvolve
import os

from pyroomasync.experiments.logger import EstimatorLogger
from pyroomasync.experiments.settings import (
    SOURCE_AZIMUTH_IN_RADIANS, FREQ_BINS, NFFT, MIC_LOCATIONS, SR, C
)


class DoaEstimator:
    def __init__(self, estimator_name, estimator_func, log_dir):
        self.log_dir = os.path.join(log_dir, estimator_name)
        self.logger = EstimatorLogger(log_dir)

        self.estimator_name = estimator_name
        self.estimator = estimator_func(
            MIC_LOCATIONS, SR, NFFT, c=C, max_four=4)

    def locate_sources(self, features):
        self.estimator.locate_sources(features, freq_bins=FREQ_BINS)
        self.logger.log(self, SOURCE_AZIMUTH_IN_RADIANS)
        
        return self.estimator.azimuth_recon


def extract_features(signals):
    return np.array(
        [
            pra.transform.stft.analysis(signal, NFFT, NFFT // 2).T
            for signal in signals
        ]
    )


def create_estimators(output_dir):
    "Load estimators included in Pyroomacoustics"
    return [
        DoaEstimator(estimator_name, estimator_func, output_dir)
        for estimator_name, estimator_func in pra.doa.algorithms.items()
        if estimator_name not in ["FRIDA"]
    ]
