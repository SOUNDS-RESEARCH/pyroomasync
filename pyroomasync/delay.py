import numpy as np

from math import floor

from .settings import (
    DELAY_FILTER_LENGTH, DELAY_FILTER_DEFAULT_WINDOW
)


def add_delays(signals, signals_fs, delays_in_seconds,
               filter_length=DELAY_FILTER_LENGTH,
               window=DELAY_FILTER_DEFAULT_WINDOW):
    """Simulate adding a certain delay to each signal. For a complete discussion on fractional delays, see:
        * https://tomroelandts.com/articles/how-to-create-a-fractional-delay-filter
        * https://pysdr.org/content/sync.html

    Args:
        signals (np.array): Matrix containing one signal per row
        signals_fs (int): Sampling frequency of the matrix
        delays_in_seconds (np.array): Array of size equal to the number of signals, where every 
                              element corresponds to the delay of that signal in seconds
        filter_length (int): Number of filter taps to use for the sinc filter. The bigger the number of taps,
                             the lower the distortion caused to the signal
        window (str): As the sinc function is infinite, it must be windowed. 'blackman' and 'hamming' are available.

    Returns:
        (np.array): Array where every signal is delayed by its corresponding delay
    """

    delays_in_samples = signals_fs*np.array(delays_in_seconds)
    
    delayed_signals_list = [
        add_delay(signal, delay, filter_length, window)
        for signal, delay in zip(signals, delays_in_samples)
    ]
    
    # Concatenate all signals into a matrix
    max_signal = max([s.shape[0] for s in delayed_signals_list])
    delayed_signals_matrix = np.zeros((signals.shape[0], max_signal))
    
    for i, signal in enumerate(delayed_signals_list):
        delayed_signals_matrix[i,:signal.shape[0]] = signal

    return delayed_signals_matrix


def add_delay(signal, delay_in_samples,
              filter_length=DELAY_FILTER_LENGTH,
              window=DELAY_FILTER_DEFAULT_WINDOW):
    integer_delay = floor(delay_in_samples)
    fractional_delay = delay_in_samples - integer_delay

    if integer_delay > 0:
        # 1. Simulate integer delay by prepending zeros to the signal
        signal = np.hstack((np.zeros(integer_delay), signal))
    
    if fractional_delay > 0:
        # 2. Simulate fractional delay by passing it through a sinc filter
        sinc_filter = create_sinc_filter(filter_length,
                                            fractional_delay,
                                            window)
        signal = np.convolve(signal, sinc_filter, "same")
    
    return signal


def create_sinc_filter(filter_length: int,
                       delay: float, window=DELAY_FILTER_DEFAULT_WINDOW):
    # Credits to:
    # and https://pysdr.org/content/sync.html

    # 1) Create window to be multiplied to the filter
    # to make sure it decays to 0 on both sides
    if window == "hamming":
        window = np.hamming(filter_length)
    elif window == "blackman":
        window = np.blackman(filter_length)
    else:
        raise ValueError("Available windows are 'hamming' and 'blackman'")

    # 2) Create the delayed sinc filter
    n = np.arange(-filter_length//2, filter_length//2) # ...-3,-2,-1,0,1,2,3...
    h = np.sinc(n - delay) # calc filter taps
    
    # 3) Apply the window created in (1)
    h *= window
    
    # 4) Normalize to get unity gain, we don't want to change the amplitude/power
    h /= np.sum(h)

    return h
