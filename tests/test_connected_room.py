import numpy as np
from pyroomacoustics import ShoeBox

from pyroomasync.connected_room import ConnectedShoeBox
from pyroomasync.simulator import simulate


def test_simulate():
    latency = 0.1 # 100 ms
    fs = 48000
    input_signal = _sinusoid(10, 1, fs)
    room_dim = [4, 6]
    source_location = [1, 1]
    mic_locations = [[2,2], [3, 3]]

    connected_room = ConnectedShoeBox(room_dim)
    connected_room.add_source(source_location, input_signal)
    connected_room.add_microphone_array(mic_locations, latency=latency)
    connected_room_results = simulate(connected_room)

    room = ShoeBox(room_dim, fs=fs)
    room.add_source(source_location, signal=input_signal)
    room.add_microphone_array(mic_locations)
    room.simulate()
    room_results = room.mic_array.signals
    
    # Assert delayed signals will start being received after a delay
    n_delayed_samples = int(latency*fs)
    assert connected_room_results.shape[1] - room_results.shape[1] == n_delayed_samples

    # Assert signals are the same
    assert np.array_equal(connected_room_results[:, n_delayed_samples:], room_results)
    assert not np.any(connected_room_results[:, :n_delayed_samples])


def _sinusoid(freq_in_hz, duration, sr):
    linear_samples = np.arange(duration*sr)
    return np.sin(linear_samples*freq_in_hz)
