import numpy as np
from pyroomacoustics import ShoeBox

from pyroomasync.room import ConnectedShoeBox
from pyroomasync.simulator import simulate


def test_latency():
    fs = 48000
    def sinusoid(freq_in_hz, duration, sr):
        linear_samples = np.arange(duration*sr)
        return np.sin(linear_samples*freq_in_hz)
    input_signal = sinusoid(10, 1, fs)
    room_dim = [4, 6]
    source_location = [1, 1]
    mic_locations = [[2,2], [3, 3]]

    latency_1 = 0.1
    latency_2 = 0.0

    def simulate_latency(latency):
        room = ConnectedShoeBox(room_dim)
        room.add_source(source_location, input_signal)
        room.add_microphone_array(mic_locations, latency=latency)
        room_results = simulate(room)
        return room_results
    
    room_1_results = simulate_latency(latency_1)
    room_2_results = simulate_latency(latency_2)
    
    # Assert delayed signals will start being received after a delay
    n_delayed_samples = int(latency_1*fs)
    assert room_1_results.shape[1] - room_2_results.shape[1] == n_delayed_samples

    # Assert signals are the same after the delay
    assert np.array_equal(room_1_results[:, n_delayed_samples:], room_2_results)
    
    # Assert signals are 0 until the delay ends
    assert not np.any(room_1_results[:, :n_delayed_samples])
