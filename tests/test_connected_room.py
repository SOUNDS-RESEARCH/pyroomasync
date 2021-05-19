import numpy as np
from pyroomacoustics import ShoeBox

from pyroomasync.connected_room import ConnectedShoeBox
from experiments.common.create_signal import create_signal


def test_simulate():
    latency = 0.1 # 100 ms
    fs = 44100
    input_signal = create_signal("low")
    room_dim = [4, 6]
    source_location = [1, 1]
    mic_locations = [[2,2], [3, 3]]

    connected_room = ConnectedShoeBox(room_dim)
    connected_room.add_source(source_location, signal=input_signal)
    connected_room.add_microphone_array(mic_locations, latency=latency)
    connected_room.simulate()

    room = ShoeBox(room_dim, fs=fs)
    room.add_source(source_location, signal=input_signal)
    room.add_microphone_array(mic_locations)
    room.simulate()
    connected_room_results = connected_room.microphones.signals
    room_results = room.mic_array.signals
    
    # Assert delayed signals will start being received after a delay
    n_delayed_samples = int(latency*fs)
    assert connected_room_results.shape[1] - room_results.shape[1] == n_delayed_samples

    # Assert signals are the same
    assert np.array_equal(connected_room_results[:, n_delayed_samples:], room_results)
    assert not np.any(connected_room_results[:, :n_delayed_samples])

