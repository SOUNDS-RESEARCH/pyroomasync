import numpy as np

from pyroomasync.room import ConnectedShoeBox


def test_add_microphone_array():
    fs = 48000
    room_dim = [4, 6, 2]
    mic_locations = [[2, 2, 2], [3, 3, 2]]

    delays = [0.1, 0.0]
    sampling_rates = [48000, 48010] 

    room = ConnectedShoeBox(room_dim)
    room.add_microphone_array(mic_locations, delays, sampling_rates)

    assert len(room.microphone_network) == 2
    assert len(room.pyroomacoustics_engine.mic_array) == 2
