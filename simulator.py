import numpy as np
import pyroomacoustics as pra

from settings import (
    DISTANCE, SR, MIC_LOCATIONS,
    ROOM_DIM, SOURCE_LOCATION, SOURCE_SIGNAL,
    ROOM_NOISE_VARIANCE
)
from logger import log_room


def simulate():
    room = pra.ShoeBox(ROOM_DIM, fs=SR, max_order=0, sigma2_awgn=ROOM_NOISE_VARIANCE)
    room.add_source(SOURCE_LOCATION, signal=SOURCE_SIGNAL)
    room.add_microphone_array(MIC_LOCATIONS)
    room.simulate()

    log_room(room)

    return room
