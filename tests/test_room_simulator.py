import numpy as np
from pyroomasync.room_simulator import simulate_room


def test_room_simulator():

    # Initialize random signals
    source_array = [
        np.random.randn(1000),
        np.random.randn(1500)
    ]

    # Initialize random rirs
    rir_matrix = [
        [
            np.random.randn(500),
            np.random.randn(1000)
        ],
        [
            np.random.randn(1500),
            np.random.randn(2000)
        ]
    ]

    result = simulate_room(source_array, rir_matrix)

    assert result.shape == (2, 3500)