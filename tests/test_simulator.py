import numpy as np

from pyroomasync.room import ConnectedShoeBox
from pyroomasync.simulator import _simulate_sampling_rates, simulate


def test_delay():
    fs = 48000
    def sinusoid(freq_in_hz, duration, sr):
        linear_samples = np.arange(duration*sr)
        return np.sin(linear_samples*freq_in_hz)
    input_signal = sinusoid(10, 1, fs)
    room_dim = [4, 6]
    source_location = [1, 1]
    mic_locations = [[2,2], [3, 3]]

    delay_1 = 0.1
    delay_2 = 0.0

    def simulate_delay(delay):
        room = ConnectedShoeBox(room_dim)
        room.add_source(source_location, input_signal)
        room.add_microphone_array(mic_locations, delay=delay)
        room_results = simulate(room)
        return room_results
    
    room_1_results = simulate_delay(delay_1)
    room_2_results = simulate_delay(delay_2)
    
    # Assert delayed signals will start being received after a delay
    n_delayed_samples = int(delay_1*fs)
    assert room_1_results.shape[1] - room_2_results.shape[1] == n_delayed_samples

    # Assert signals are the same after the delay
    assert np.array_equal(room_1_results[:, n_delayed_samples:], room_2_results)
    
    # Assert signals are 0 until the delay ends
    assert not np.any(room_1_results[:, :n_delayed_samples])


def test_simulate_sampling_rates_downsample_mode():
    fs = 48000
    mic_fs = 32000
    def sinusoid(freq_in_hz, duration, sr):
        linear_samples = np.arange(duration*sr)
        return np.sin(linear_samples*freq_in_hz)
    input_signal = sinusoid(10, 1, fs)[np.newaxis]

    result = _simulate_sampling_rates(input_signal, [mic_fs], fs, mode="downsample")
    
    assert (result[0, 32000:] == 0).all()
