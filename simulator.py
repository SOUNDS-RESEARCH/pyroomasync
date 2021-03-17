import numpy as np
import pyroomacoustics as pra

from settings import (
    DISTANCE, SR, MIC_LOCATIONS,
    SOURCE_AZIMUTH_IN_RADIANS,
    ROOM_DIM, ROOM_NOISE_VARIANCE
)
from logger import log_simulation_results
from input_signals import create_signal

class Simulation:
    def __init__(self, input_signal_type, output_folder):
        self.input_signal_type = input_signal_type
        self.output_folder = output_folder
        input_signal = create_signal(input_signal_type)
        
        self.room = pra.ShoeBox(
            ROOM_DIM, fs=SR, max_order=0, sigma2_awgn=ROOM_NOISE_VARIANCE)

        source_location = self._compute_source_location()

        self.room.add_source(source_location, signal=input_signal)
        self.room.add_microphone_array(MIC_LOCATIONS)
    
    def _compute_source_location(self):
        return ROOM_DIM / 2 + DISTANCE * np.r_[np.cos(SOURCE_AZIMUTH_IN_RADIANS), np.sin(SOURCE_AZIMUTH_IN_RADIANS)]

    def run(self):
        print("Running simulation with '{}' signal type".format(
            self.input_signal_type))

        self.room.simulate()

        log_simulation_results(self.room, self.output_folder)

        return self.room
