import numpy as np

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
    #breakpoint()
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
