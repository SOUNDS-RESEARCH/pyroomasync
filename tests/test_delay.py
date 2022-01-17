import matplotlib.pyplot as plt
import numpy as np
import os

from pyroomasync.delay import add_delays, create_sinc_filter


def test_add_delays():
    fs = 48000
    input_signals = np.array(2*[_sinusoid(200, 1, fs)])
    delays_in_samples = [0.1, 0.5]
    delays_in_seconds = [d/fs for d in delays_in_samples]
   
    result = add_delays(input_signals, fs, delays_in_seconds)
    
    fig, axs = plt.subplots(nrows=2)
    axs[0].plot(result[0][0:20], label=f"delay={delays_in_samples[0]}")
    axs[0].plot(result[1][0:20], label=f"delay={delays_in_samples[1]}")
    axs[0].legend()
    axs[0].set_title("Fractional delay filter introduces artifacts in the beginning")

    axs[1].plot(range(100, 120), result[0][100:120], label=f"delay={delays_in_samples[0]}")
    axs[1].plot(range(100, 120), result[1][100:120], label=f"delay={delays_in_samples[1]}")
    axs[1].legend()
    axs[1].set_title("...But stabilizes soon afterwards")
    os.makedirs("tests/temp/", exist_ok=True)
    plt.tight_layout()
    plt.savefig("tests/temp/fractional_delays.png")


def test_add_integer_delay():
    fs = 48000
    input_signals = np.array(2*[_sinusoid(200, 1, fs)])
    delays_in_samples = [100, 50]
    delays_in_seconds = [d/fs for d in delays_in_samples]
   
    result = add_delays(input_signals, fs, delays_in_seconds)
    
    fig, ax = plt.subplots()
    ax.plot(result[0][0:150], label=f"delay={delays_in_samples[0]}")
    ax.plot(result[1][0:150], label=f"delay={delays_in_samples[1]}")
    ax.legend()
    ax.set_title("Integer delays")

    os.makedirs("tests/temp/", exist_ok=True)
    plt.tight_layout()
    plt.savefig("tests/temp/integer_delays.png")

    assert result.shape[1] == 48100


def test_add_fractional_delay():
    fs = 48000
    input_signals = np.array(2*[_sinusoid(200, 1, fs)])
    delays_in_samples = [100.9, 100.0]
    delays_in_seconds = [d/fs for d in delays_in_samples]
   
    result = add_delays(input_signals, fs, delays_in_seconds)
    
    fig, ax = plt.subplots()
    ax.plot(result[0][0:150], label=f"delay={delays_in_samples[0]}")
    ax.plot(result[1][0:150], label=f"delay={delays_in_samples[1]}")
    ax.legend()
    ax.set_title("Integer delays")

    os.makedirs("tests/temp/", exist_ok=True)
    plt.tight_layout()
    plt.savefig("tests/temp/fractional_delays.png")

    assert result.shape[1] == 48100


def test_create_sinc_filter():
    filter_length = 21
    idxs = range(-filter_length//2, filter_length//2)
    
    sinc_hamming = create_sinc_filter(filter_length, 0.5, "hamming")
    sinc_blackman = create_sinc_filter(filter_length, 0.5, "blackman")

    fig, ax = plt.subplots()
    ax.plot(idxs, sinc_hamming, label=f"window=hamming")
    ax.plot(idxs, sinc_blackman, label=f"window=blackman")
    ax.legend()
    ax.set_title("Delayed sinc filter windowed by different functions")

    os.makedirs("tests/temp/", exist_ok=True)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("tests/temp/sinc.png")


def _sinusoid(freq_in_hz, duration, sr):
    linear_samples = np.arange(duration*sr)
    return np.cos(2*np.pi*linear_samples*freq_in_hz/sr)