import matplotlib.pyplot as plt
import numpy as np
import os

from pyroomasync.room import ConnectedShoeBox
from pyroomasync.simulator import (
    resample_signals, simulate
)


def test_resample_signals():
    fs = 48000
    target_fs = 32000
    input_signal = _sinusoid(10, 1, fs)[np.newaxis]

    result = resample_signals(input_signal, fs, [target_fs])
    
    assert (result[:, 32000:] == 0).all()


def test_resample_noninteger():
    fs = 48000
    target_fs = [31999.5, 32000.1]
    input_signals = np.array(2*[_sinusoid(200, 1, fs)])

    result = resample_signals(input_signals, fs, target_fs)
    assert (result[:, 32000:] == 0).all()

    fig, axs = plt.subplots(nrows=2)
    axs[0].plot(result[0][0:100], label=f"rate={target_fs[0]}")
    axs[0].plot(result[1][0:100], label=f"rate={target_fs[1]}")
    axs[0].legend()
    axs[0].set_title("Signals are synchronized at the start")

    axs[1].plot(range(31900,32000), result[0][31900:32000], label=f"rate={target_fs[0]}")
    axs[1].plot(range(31900,32000), result[1][31900:32000], label=f"rate={target_fs[1]}")
    axs[1].legend()
    axs[1].set_title("Signals are desynchronized in the end")
    os.makedirs("tests/temp/", exist_ok=True)
    plt.tight_layout()
    plt.savefig("tests/temp/noninteger_sampling_rates.png")


def test_simulate_with_snr():
    """This test does not contain any assertions.
        To manually assert this function is working, check
        the generated image at tests/temp/snr.png is noisy.
    """
    fs = 16000
    snr = 0

    input_signal = _sinusoid(10, 1, fs)
    room_dim = [4, 6]
    source_location = [1, 1]
    mic_locations = [[2,2], [3, 3]]

    room = ConnectedShoeBox(room_dim)
    room.add_source(source_location, input_signal)
    room.add_microphone_array(mic_locations)
    room_results = simulate(room, snr=snr)
    
    fig, ax = plt.subplots()
    ax.plot(room_results[0])
    
    os.makedirs("tests/temp/", exist_ok=True)
    plt.savefig("tests/temp/snr.png")


def _sinusoid(freq_in_hz, duration, sr):
    linear_samples = np.arange(duration*sr)
    return np.sin(2*np.pi*linear_samples*freq_in_hz/sr)
