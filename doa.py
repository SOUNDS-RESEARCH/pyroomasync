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
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
import pyroomacoustics as pra

from plotter import plot_doa
from settings import (
    AZIMUTH, FREQ_BINS, NFFT, MIC_LOCATIONS, FS, C
)

def preprocess(signals):
    ################################
    # Compute the STFT frames needed
    return np.array(
        [
            pra.transform.stft.analysis(signal, NFFT, NFFT // 2).T
            for signal in signals
        ]
    )

def estimate(room):
    signals = room.mic_array.signals
    features = preprocess(signals)

    available_algos = sorted(pra.doa.algorithms.keys())

    for algo_name in available_algos:
        # Construct the new DOA object
        # the max_four parameter is necessary for FRIDA only
        algorithm = pra.doa.algorithms[algo_name](MIC_LOCATIONS, FS, NFFT, c=C, max_four=4)

        # this call here perform localization on the frames in X
        algorithm.locate_sources(features, freq_bins=FREQ_BINS)
        plot_doa(algorithm, algo_name, AZIMUTH)