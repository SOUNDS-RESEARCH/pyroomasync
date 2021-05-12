import numpy as np
import pyroomacoustics as pra
from pyroomacoustics.beamforming import MicrophoneArray

from pyroomasync.mic_network_simulator import simulate_latency

DEFAULT_FS = 44100

class ConnectedShoeBox(pra.ShoeBox):
    def __init__(self, dims, **kwargs):
        super().__init__(dims, fs=DEFAULT_FS, **kwargs)

        self.mic_latencies = []
        self.mic_fs = []

    def add_microphone(self, loc, fs=None, latency=0):
        if fs is None:
            fs = self.fs
        super().add_microphone(loc, fs=self.fs)
        self.mic_latencies.append(latency)
        self.mic_fs.append(fs)

    def add_microphone_array(self, microphone_array, latency=0):
        super().add_microphone_array(microphone_array)
        n_mics = len(microphone_array)
        self.mic_latencies += _parse_latency(latency, n_mics)

        if isinstance(microphone_array, MicrophoneArray):
            self.mic_fs += n_mics*[microphone_array.fs]
        else:
            self.mic_fs += n_mics*[self.fs]

    def simulate_network(self, **kwargs):
        self.simulate(**kwargs)

        signals = self.mic_array.signals

        self.mic_array.connected_signals = simulate_latency(
            signals, np.array(self.mic_latencies), self.fs
        )

        return self.mic_array.connected_signals


def _parse_latency(latency, n_mics):
    if type(latency) in (int, float):
        latency = n_mics*[latency]
    elif type(latency) == list:
        n_latency = len(latency)
        if n_latency != n_mics:
            raise ValueError(
                (
                    "The latency array is of size {}. Please provide an array of "
                    "the same size as the microphone positions array ({})"
                ).format(n_latency, n_mics)
            )
    return latency
