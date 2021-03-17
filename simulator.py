import numpy as np
import pyroomacoustics as pra

from settings import (
    DISTANCE, SR, MIC_LOCATIONS,
    ROOM_DIM, SOURCE_LOCATION,
    ROOM_NOISE_VARIANCE
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
        self.room.add_source(SOURCE_LOCATION, signal=input_signal)
        self.room.add_microphone_array(MIC_LOCATIONS)
    
    def run(self):
        print("Running simulation with '{}' signal type".format(
            self.input_signal_type))

        self.room.simulate()

        log_simulation_results(self.room, self.output_folder)

        return self.room
