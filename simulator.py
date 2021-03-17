import numpy as np
import pyroomacoustics as pra

from settings import (
    DISTANCE, FS, MIC_LOCATIONS,
    ROOM_DIM, SNR, SOURCE_LOCATION, SOURCE_SIGNAL
)
from logger import log_room

def simulate():
    # compute the noise variance
    sigma2 = 10 ** (-SNR / 10) / (4.0 * np.pi * DISTANCE) ** 2

    room = pra.ShoeBox(ROOM_DIM, fs=FS, max_order=0, sigma2_awgn=sigma2)
    room.add_source(SOURCE_LOCATION, signal=SOURCE_SIGNAL)

    # We use a circular array with radius 15 cm # and 12 microphones

    microphones = pra.MicrophoneArray(MIC_LOCATIONS, fs=FS)
    room.add_microphone_array(microphones)

    log_room(room)
    # run the simulation
    room.simulate()

    return room
