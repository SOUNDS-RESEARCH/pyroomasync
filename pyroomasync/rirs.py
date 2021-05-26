import numpy as np
from scipy.signal import fftconvolve


class Rirs:
    def __init__(self):
        self.rir_dict = {}
    
    def add(self, signal, mic_id, source_id):
        rir_key = (mic_id, source_id)
        self.rir_dict[rir_key] = signal

    def is_empty(self):
        return self.rir_dict == {}

    def __call__(self, microphone_id, source_id):
        key = (microphone_id, source_id)
        return self.rir_dict[key]


def convolve(rirs, microphones, sources):
    mic_signals = []
    for mic in microphones.mic_array:
        pre_mixed_signals = []
        for source in sources.source_array:
            pre_mixed_signal = fftconvolve(
                rirs(mic.id, source.id),
                source.signal
            )
            pre_mixed_signals.append(
                pre_mixed_signal
            )
        mic_signals.append(
            _mix_signals(pre_mixed_signals)
        )

    return _make_matrix(mic_signals)


def normalize(signals):
    """
    Normalize signals so the maximum amplitude is one.
    """

    return signals / np.abs(signals).max()


def _mix_signals(pre_mixed_signals):
    signal_max_len = max(
        [len(signal) for signal in pre_mixed_signals]
    )

    mixed_signal = np.zeros(signal_max_len)
    
    for signal in pre_mixed_signals:
        mixed_signal[0:len(signal)] += signal
        
    return mixed_signal


def _make_matrix(mic_signals):
    n_mics = len(mic_signals)
    signal_max_len = max(
        [len(signal) for signal in mic_signals]
    )

    output_matrix = np.zeros((n_mics, signal_max_len))

    for i, signal in enumerate(mic_signals):
        output_matrix[i, 0:len(signal)] = signal

    return normalize(output_matrix)
