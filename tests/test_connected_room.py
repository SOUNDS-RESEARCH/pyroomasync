import numpy as np
from pyroomacoustics import ShoeBox

from pyroomasync.connected_room import ConnectedShoeBox
from experiments.common.create_signal import create_signal
from experiments.common.math_utils import compute_source_location
from experiments.settings import (
    ROOM_DIM, SR, SOURCE_AZIMUTH_IN_RADIANS, DISTANCE, MIC_LOCATIONS
)


def test_simulate():
    latency = 0.1 # 100 ms
    n_delayed_samples = int(latency*SR)

    input_signal = create_signal("low")
    source_location = compute_source_location(
        SOURCE_AZIMUTH_IN_RADIANS,
        DISTANCE,
        ROOM_DIM
    )

    connected_room = ConnectedShoeBox(ROOM_DIM, fs=SR)
    connected_room.add_source(source_location, signal=input_signal)
    connected_room.add_microphone_array(MIC_LOCATIONS, latency=latency)

    room = ShoeBox(ROOM_DIM, fs=SR)
    room.add_source(source_location, signal=input_signal)
    room.add_microphone_array(MIC_LOCATIONS)

    connected_room_results = connected_room.simulate()
    room.simulate()
    room_results = room.mic_array.signals

    # Assert delayed signals will start being received after a delay
    assert connected_room_results.shape[1] - room_results.shape[1] == n_delayed_samples

    # Assert signals are the same
    assert np.array_equal(connected_room_results[:, n_delayed_samples:], room_results)
    assert not np.any(connected_room_results[:, :n_delayed_samples])