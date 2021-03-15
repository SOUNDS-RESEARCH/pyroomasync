import numpy as np
import pyroomacoustics as pra

from settings import (
    ABSORPTION, FS, MAX_ORDER,
    MIC_LOC, ROOM_DIM, SOURCE_LOC,
    SOURCE_SIGNAL
)

def simulate():
    # Create the room itself
    room = pra.ShoeBox(ROOM_DIM, fs=FS, absorption=ABSORPTION, max_order=MAX_ORDER)
    room.add_source(SOURCE_LOC, signal=SOURCE_SIGNAL)

    # Place the microphone array
    microphone_array = pra.MicrophoneArray(MIC_LOC, fs=FS)
    room.add_microphone_array(microphone_array)

    # Now the setup is finished, run the simulation
    room.simulate()

    return room
