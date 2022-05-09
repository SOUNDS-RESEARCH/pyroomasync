import numpy as np

from pyroomasync import ConnectedShoeBox, simulate
from algorithms.sro_estimation import naive_sro_estimator

def test_sro_estimation(): 
    ROOM_DIMS = [5,4,3]
    MIC_COORDINATES = [
        [1.5, 2, 1],
        [4.5, 1.5, 1]
    ]
    SOURCE_COORDINATES = [2.5, 2, 1]
    SR = 16000
    SIGNAL_DURATION_IN_SECS = 60
    SR_OFFSET = 0.5
    FRAME_SIZE_IN_SECS = 0.3
    HOP_PERCENT = 0.5
    EPS = 0.01

    source_signal = np.random.randn(SIGNAL_DURATION_IN_SECS*SR)

    room = ConnectedShoeBox(ROOM_DIMS, fs=SR)

    # Add microphones with their sampling frequencies and latencies
    room.add_microphone(MIC_COORDINATES[0])
    room.add_microphone(MIC_COORDINATES[1], fs_offset=SR_OFFSET)

    # Add a source
    room.add_source(SOURCE_COORDINATES, source_signal)

    # simulate and get the results recorded in the microphones
    simulation_results = simulate(room)

    estimated_sro = naive_sro_estimator(simulation_results[0], simulation_results[1],
                              SR, FRAME_SIZE_IN_SECS, HOP_PERCENT)
    
    assert estimated_sro - SR_OFFSET <= EPS