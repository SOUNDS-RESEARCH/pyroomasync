import numpy as np

from scipy.signal import resample

from pyroomasync.settings import DEFAULT_ROOM_FS


def simulate_latency(signals, latencies, fs):
    """Simulate adding a certain latency to each signal

    Args:
        signals (np.array): Matrix containing one signal per row
        latencies (np.array): Array of size equal to the number of signals, where every 
                              element corresponds to the latency of that signal in seconds
        fs (int): Sampling frequency of the matrix

    Returns:
        (np.array): Array where every signal is delayed by its corresponding latency
    """

    n_signals, n_signal = signals.shape
    mic_delayed_samples = fs*np.array(latencies)
    max_delayed_samples = int(mic_delayed_samples.max()) 
    n_output_signal = n_signal + max_delayed_samples
    output_signals = np.zeros(
        (n_signals, n_output_signal)
    )

    for i in range(n_signals):
        n_delayed_samples = int(mic_delayed_samples[i])
        n_end_signal = n_output_signal - (max_delayed_samples - n_delayed_samples)
        output_signals[i, n_delayed_samples:n_end_signal] = signals[i]

    return output_signals


def simulate_sampling_rates(signals, mic_fs, room_fs=DEFAULT_ROOM_FS):
    n_signals, n_signal = signals.shape
    resampled_signals = np.zeros_like(signals)

    for i in range(n_signals):
        resampling_rate = (mic_fs[i]/room_fs)
        if resampling_rate == 1:
            # Do not resample
            resampled_signals[i,:] = signals[i]
        else:
            n_new_signal = int(n_signal*resampling_rate)
            resampled_signals[i,:n_new_signal] = resample(
                                                    signals[i], n_new_signal)

    return resampled_signals