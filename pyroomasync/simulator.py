import numpy as np

from librosa import resample

from pyroomasync.rirs import convolve, normalize
from pyroomasync.room import ConnectedShoeBox
from pyroomasync.delay import add_delays


def simulate(room: ConnectedShoeBox, **kwargs):
    """Simulate recordings of an asynchronous microphone network embedded within a room.
       

       Input signals are put through an acoustic channel, where they are convolved with 
       room impulse responses pertaining to every microphone.
       The signals at every microphone are then summed together to generate the 
       simulated recorded signal at each microphone.
       1. To simulate sampling rate offsets between microphones, sinc interpolation
       is applied to every recording.
       2. To simulate delays between the microphones,
       which may be caused by clock offsets or network latency, a sinc filter is applied to
       every resampled signal.
       3. To simulate level differences,
       the resulting signals are multipliedby their respective gain values.

    Args:
        room (ConnectedShoeBox): Room containing asynchronous microphones and sources

    Returns:
        numpy.array: Matrix containing one row per microphone signal
    """

    if room.rirs.is_empty():
        # no RIRs provided: simulate using pyroomacoustics 
        room.pyroomacoustics_engine.simulate(**kwargs)
        signals = room.pyroomacoustics_engine.mic_array.signals
        acoustic_signals = normalize(signals)
    else:
        acoustic_signals = convolve(room.rirs, room.microphone_network, room.sources)
    

    resampled_signals = resample_signals(
                            acoustic_signals,
                            room.microphone_network.base_fs,
                            room.microphone_network.get_fs(),
                        )

    deleveled_signals = simulate_microphone_gains(
                            resampled_signals,
                            room.microphone_network.get_gains()
                        )

    delayed_signals = add_delays(
                        deleveled_signals,
                        room.microphone_network.get_fs(),
                        room.microphone_network.get_delays()
                      )

    return delayed_signals


def resample_signals(signals: np.array, original_fs: int, target_fs: np.array):
    """Resample a matrix of signals to their own target signals

    Args:
        signals (np.array): Matrix with one row per signal
        original_fs (int): Original sampling rate of signals
        target_fs (list or np.array): Target sampling rate for every row

    Returns:
        np.array: Matrix where every signal is resampled to a specific rate
    """
    n_signals = signals.shape[0]
    resampled_signals = np.zeros_like(signals)

    target_fs = np.array(target_fs)
    if (target_fs > original_fs).any():
        raise ValueError("Resampling only supported for smaller rates than the original")

    for i in range(n_signals):
        if target_fs[i] == original_fs:
            resampled_signals[i,:] = signals[i]
        else:
            
            downsampled_signal = resample(signals[i],
                                          original_fs, target_fs[i])
            n_new_signal = downsampled_signal.shape[0]
            resampled_signals[i][:n_new_signal] = downsampled_signal

    return resampled_signals


def simulate_microphone_gains(signals, mic_gains):
    if type(mic_gains) == list:
        mic_gains = np.array(mic_gains)
    
    mic_gains = mic_gains.reshape(mic_gains.shape[0], 1)
    return signals*mic_gains
