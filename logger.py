import soundfile as sf
import matplotlib.pyplot as plt
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from plotter import (
    plot_dirac, plot_room, plot_microphone_signals
)
from math_utils import azimuth_to_degrees, estimation_error
from settings import SR


class Logger:
    def __init__(self, output_dir, file_name=""):
        self.output_dir = output_dir

        if file_name:
            self.output_file_path = os.path.join(output_dir, file_name)

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
    
    def log(self):
        pass

class ErrorLogger(Logger):
    def __init__(self, output_dir):
        super().__init__(output_dir, "metrics.csv")
        
    def log(self, result, ground_truth):
        df = pd.DataFrame.from_records([{
            "Recovered azimuth": azimuth_to_degrees(result)[0],
            "Error": estimation_error(result, ground_truth)[0]}]
        )
        df.to_csv(self.output_file_path)
    
class EstimatorLogger(Logger):
    def __init__(self, output_dir):
        super().__init__(output_dir, "dirac.png")
        self.error_logger = ErrorLogger(output_dir)

    def log(self, estimator, ground_truth):
        result = estimator.estimator.azimuth_recon

        plot_dirac(
            estimator.estimator,
            self.output_file_path,
            ground_truth)

        self.error_logger.log(result, ground_truth)


class RirLogger(Logger):
    def __init__(self, output_dir):
        super().__init__(output_dir, "mic_rir.png")

    def log(self, room):
        room.plot_rir()
        plt.savefig(self.output_file_path)


class SceneLogger(Logger):
    def __init__(self, output_dir):
        super().__init__(output_dir, "room.png")

    def log(self, room):  
        plot_room(room, self.output_file_path)


class SimulationLogger:
    def __init__(self, output_dir):
        self.room_logger = SceneLogger(output_dir)
        self.rir_logger = RirLogger(output_dir)
    
    def log(self, room):
        self.room_logger.log(room)
        self.rir_logger.log(room)

class MicSignalLogger(Logger):
    def __init__(self, output_dir, mic_id):
        file_name = os.path.join(output_dir, "mic_signals_{}.wav".format(i))
        super().__init__(output_dir, file_name)

    def log(self, mic_signal):
        sf.write(self.output_file_path, mic_signal, SR)

class MicArrayLogger(Logger):
    def __init__(self, output_dir):
        super.__init__(output_dir, "mic_signals.png")

    def log(self, room):    
        mic_signals = room.mic_array.signals
        for i, mic_signal in enumerate(mic_signals):
            logger = MicSignalLogger(self.output_dir, i)
            logger.log(mic_signal)

        plot_microphone_signals(self.output_file_path)
