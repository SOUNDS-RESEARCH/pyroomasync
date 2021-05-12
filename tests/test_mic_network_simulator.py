import numpy as np

from pyroomasync.mic_network_simulator import simulate_sampling_rates


def test_simulate_sampling_rates():
    
    mic_array = np.ones((2, 44100))
    mic_fs = [22050, 11025]

    resampled_mic_array = simulate_sampling_rates(mic_array, mic_fs)
    assert (resampled_mic_array.sum(axis=1) ==np.array([22050, 11025])).all()