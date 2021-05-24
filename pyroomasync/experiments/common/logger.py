from pyroomasync.experiments.common.plotter import (
    plot_room, plot_microphone_signals
)
import soundfile as sf
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")


class SimulationLogger:
    def __init__(self, output_dir):
        self.room_logger = RoomLogger(output_dir)
        self.mic_array_logger = ConnectedMicArrayLogger(output_dir)

    def log(self, room, mic_signals):
        self.room_logger.log(room.pyroomacoustics_engine)
        self.mic_array_logger.log(mic_signals, room.fs)


class BaseLogger:
    def __init__(self, output_dir, file_name=""):
        self.output_dir = output_dir

        if file_name:
            self.output_file_path = os.path.join(output_dir, file_name)

        os.makedirs(output_dir, exist_ok=True)

    def log(self):
        pass


class RoomLogger(BaseLogger):
    def __init__(self, output_dir):
        super().__init__(output_dir, "room.png")

    def log(self, room):
        plot_room(room, self.output_file_path)


class MicSignalLogger(BaseLogger):
    def __init__(self, output_dir, mic_id):
        file_name = "mic_signals_{}.wav".format(mic_id)
        super().__init__(output_dir, file_name)

    def log(self, mic_signal, sr):
        sf.write(self.output_file_path, mic_signal, sr)


class ConnectedMicArrayLogger(BaseLogger):
    def __init__(self, output_dir):
        super().__init__(output_dir, "mic_signals.png")

    def log(self, mic_signals, fs):
        for i, mic_signal in enumerate(mic_signals):
            logger = MicSignalLogger(self.output_dir, i)
            logger.log(mic_signal, fs)

        plot_microphone_signals(mic_signals, self.output_file_path)
