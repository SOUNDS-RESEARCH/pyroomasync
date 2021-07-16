import numpy as np
from scipy.signal import resample

from pyroomasync.rirs import convolve, normalize
from pyroomasync.room import ConnectedShoeBox
from pyroomasync.microphones import Microphones


def simulate(room: ConnectedShoeBox):
    """Simulate recordings on an asynchronous microphone network, firstly by propagating
       signals through the acoustic channel and later through the network channel.
       For more information on each channel simulation, please read the "network_simulation"
       and "acoustic_simulation" functions.

    Args:
        room (ConnectedShoeBox): Room containing asynchronous microphones and sources

    Returns:
        numpy.array: Matrix containing one matrix per 
    """
    acoustic_simulation_results = acoustic_simulation(room)
    
    network_simulation_results = network_simulation(
        room.microphones, acoustic_simulation_results)

    return network_simulation_results


def network_simulation(microphones: Microphones,
                       recorded_signals: np.array):
    """Simulate propagation through the network channel.
    The simulation consists in zero padding the beginning of each recorded signal
    according to its microphone delay.

    Args:
        microphones (Microphones): Object representing n microphones which recorded recorded_signals 
        recorded_signals (np.array): Matrix where every row is a signal recorded by one microphone in Microphones 

    Returns:
        np.array: recorded_signals with a respective added delay at the beginning.
    """

    signals = _simulate_delay(
        recorded_signals,
        microphones.get_latencies(),
        microphones.base_fs
    )

    return signals


def acoustic_simulation(room: ConnectedShoeBox, sampling_mode="downsample"):
    """Simulate propagation through acoustic channel.
       The first part of the simulation consists in convolving the signals
       from every source within a room with the room impulse responses for every (source, microphone pair), then summing
       all resulting signals at each microphone.
       A later step consists in downsampling the recorded signals with respect to its
       respective microphone sampling rate.

    Args:
        room (ConnectedShoeBox): Room containing microphones and sources
        sampling_mode (str): "downsample" or "smoothen".
                             Downsample will reduce the size of the signal,
                             Smoothen will downsample and upsample the signal,
                             resulting in a signal of the same size.

    Returns:
        np.array: Matrix containing one recording per microphone
    """

    if room.rirs.is_empty():
        # no RIRs provided: simulate using pyroomacoustics 
        room.pyroomacoustics_engine.simulate()
        signals = room.pyroomacoustics_engine.mic_array.signals
        signals = normalize(signals)
    else:
        signals = convolve(room.rirs, room.microphones, room.sources)
    
    signals = _simulate_sampling_rates(
        signals,
        room.microphones.get_fs(),
        room.microphones.base_fs,
        mode=sampling_mode
    )

    return signals


def _simulate_delay(signals, latencies, room_fs):
    """Simulate adding a certain delay to each signal

    Args:
        signals (np.array): Matrix containing one signal per row
        latencies (np.array): Array of size equal to the number of signals, where every 
                              element corresponds to the delay of that signal in seconds
        room_fs (int): Sampling frequency of the matrix

    Returns:
        (np.array): Array where every signal is delayed by its corresponding delay
    """

    n_signals, n_signal = signals.shape
    mic_delayed_samples = room_fs*np.array(latencies)
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


def _simulate_sampling_rates(signals, mic_fs, signals_fs, mode="downsample"):
    """Samples signals to microphone signals and back to the signals_fs
    """
    n_signals, n_signal = signals.shape
    resampled_signals = np.zeros_like(signals)

    for i in range(n_signals):
        resampling_rate = (mic_fs[i]/signals_fs)
        if resampling_rate == 1:
            # Do not resample
            resampled_signals[i,:] = signals[i]
        else:
            n_new_signal = int(n_signal*resampling_rate)
            downsampled_signal = resample(signals[i], n_new_signal)

            if mode == "downsample":
                # Do not upsample: add smaller signal to beginning of output matrix
                resampled_signals[i][:n_new_signal] = downsampled_signal
            elif mode == "smoothen":
                # Upsample after downsampling, making the simulation behave like a low pass
                upsampled_signal = resample(downsampled_signal, n_signal)
                resampled_signals[i] = upsampled_signal

    return resampled_signals
