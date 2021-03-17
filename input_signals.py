import numpy as np
import librosa

from settings import (
    SR, SIGNAL_DURATION_IN_SECONDS, LOW_FREQ_IN_HZ,
    HIGH_FREQ_IN_HZ
)

def _noise():
    return np.random.randn(SIGNAL_DURATION_IN_SECONDS*SR)

def _sinusoid(freq_in_hz):
    linear_samples = np.arange(SIGNAL_DURATION_IN_SECONDS*SR)
    return np.sin(linear_samples*freq_in_hz)

def _speech():
    return librosa.load("speech_samples/p225_001.wav", sr=SR)[0]


def create_signal(signal_type):
    if signal_type == "low":
        return _sinusoid(LOW_FREQ_IN_HZ)
    elif signal_type == "high":
        return _sinusoid(HIGH_FREQ_IN_HZ)
    elif signal_type == "noise":
        return _noise()
    elif signal_type == "speech":
        return _speech()

def signal_types():
    return ["speech", "low", "high", "noise"]