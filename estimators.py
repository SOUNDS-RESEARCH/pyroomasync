# -*- coding: utf-8 -*-
"""
DOA Algorithms
==============
This example demonstrates how to use the DOA object to perform direction of arrival
finding in 2D using one of several algorithms
- MUSIC [1]_
- SRP-PHAT [2]_
- CSSM [3]_
- WAVES [4]_
- TOPS [5]_
- FRIDA [6]_
.. [1] R. Schmidt, *Multiple emitter location and signal parameter estimation*, 
    IEEE Trans. Antennas Propag., Vol. 34, Num. 3, pp 276--280, 1986
.. [2] J. H. DiBiase, J H, *A high-accuracy, low-latency technique for talker localization 
    in reverberant environments using microphone arrays*, PHD Thesis, Brown University, 2000
.. [3] H. Wang, M. Kaveh, *Coherent signal-subspace processing for the detection and 
    estimation of angles of arrival of multiple wide-band sources*, IEEE Trans. Acoust., 
    Speech, Signal Process., Vol. 33, Num. 4, pp 823--831, 1985
.. [4] E. D. di Claudio, R. Parisi, *WAVES: Weighted average of signal subspaces for 
    robust wideband direction finding*, IEEE Trans. Signal Process., Vol. 49, Num. 10, 
    2179--2191, 2001
.. [5] Y. Yeo-Sun, L. M. Kaplan, J. H. McClellan, *TOPS: New DOA estimator for wideband 
    signals*, IEEE Trans. Signal Process., Vol. 54, Num 6., pp 1977--1989, 2006
.. [6] H. Pan, R. Scheibler, E. Bezzam, I. Dokmanić, and M. Vetterli, *FRIDA:
    FRI-based DOA estimation for arbitrary array layouts*, Proc. ICASSP,
    pp 3186-3190, 2017
In this example, we generate some random signal for a source in the far field
and then simulate propagation using a fractional delay filter bank
corresponding to the relative microphone delays.
Then we perform DOA estimation and compare the errors for different algorithms
"""

import numpy as np
import matplotlib.pyplot as plt
import pyroomacoustics as pra
from scipy.signal import fftconvolve

from logger import log_estimation_results
from settings import (
    SOURCE_AZIMUTH, FREQ_BINS, NFFT, MIC_LOCATIONS, FS, C
)

def create_estimators():
    return [
        DoaEstimator(estimator_name, estimator_func)
        for estimator_name, estimator_func in pra.doa.algorithms.items()
    ]

class DoaEstimator:
    def __init__(self, estimator_name, estimator_func):
        self.estimator_name = estimator_name
        self.estimator = estimator_func(
            MIC_LOCATIONS, FS, NFFT, c=C, max_four=4)

    def locate_sources(self, features):
        self.estimator.locate_sources(features, freq_bins=FREQ_BINS)
        log_estimation_results(self, SOURCE_AZIMUTH)
        return self.estimator.azimuth_recon

    def polar_plt_dirac(self):
        return self.estimator.polar_plt_dirac()

def extract_features(signals):
    ################################
    # Compute the STFT frames needed
    return np.array(
        [
            pra.transform.stft.analysis(signal, NFFT, NFFT // 2).T
            for signal in signals
        ]
    )


def locate_sources(features):
    estimators = create_estimators()
    
    return {
        estimator.estimator_name:estimator.locate_sources(features)
        for estimator in estimators
    }
