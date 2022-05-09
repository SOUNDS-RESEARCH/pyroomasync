"This directory contains cross correlation methods, which are used to estimate delays (tdoas) between signals"

import numpy as np

from scipy.signal.signaltools import correlate, correlation_lags

EPS = 1e-4


def temporal_cross_correlation(x1, x2, abs=True):
    # Normalize signals for a normalized correlation
    # https://github.com/numpy/numpy/issues/2310
    x1 = (x1 - np.mean(x1)) / (np.std(x1) * len(x1))
    x2 = (x2 - np.mean(x2)) / (np.std(x2) * len(x2))
    
    cc = correlate(x1, x2, mode="same")

    if abs:
        cc = np.abs(cc)
    
    return cc


def gcc_phat(x1, x2, mode="cc", unwrap=True, abs=True):
    '''
    This function computes the offset between the signal sig and the reference signal x2
    using the Generalized Cross Correlation - Phase Transform (GCC-PHAT) method.
    Implementation based on http://www.xavieranguera.com/phdthesis/node92.html
    '''
    
    n = x1.shape[0] # + x2.shape[0]

    X1 = np.fft.rfft(x1, n=n)
    X2 = np.fft.rfft(x2, n=n)
    R = X1 * np.conj(X2)
    Gphat = R / (EPS + np.abs(R))
    
    if mode == "phase":
        Gphat_phase = np.angle(Gphat)
        if unwrap:
            return np.unwrap(Gphat_phase)
        return Gphat_phase
    
    cc = np.fft.irfft(Gphat, n=n)

    max_shift = n // 2

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift+1]))
    
    if abs:
        cc = np.abs(cc)

    return cc


def get_correlation_lags(n_signal_1, n_signal_2, sr):
    lag_indexes = correlation_lags(n_signal_1, n_signal_2, mode="same")
    return lag_indexes/sr

