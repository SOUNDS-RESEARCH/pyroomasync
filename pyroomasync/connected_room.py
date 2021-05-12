import numpy as np
import pyroomacoustics as pra
from pyroomacoustics.beamforming import MicrophoneArray

from pyroomasync.mic_network_simulator import (
    simulate_latency
)
from pyroomasync.settings import DEFAULT_ROOM_FS


class ConnectedShoeBox(pra.ShoeBox):
    def __init__(self, dims, **kwargs):
        super().__init__(dims, fs=DEFAULT_ROOM_FS, **kwargs)

        self.connected_mic_array = ConnectedMicrophoneArray()

    def add_microphone(self, loc, fs=None, latency=0):
        if fs is None:
            fs = self.fs
        super().add_microphone(loc, fs=self.fs)
        self.connected_mic_array.add_microphone(fs, latency)

    def add_microphone_array(self, microphone_array, latency=0):
        super().add_microphone_array(microphone_array)
        n_mics = len(microphone_array)

        if isinstance(microphone_array, MicrophoneArray):
            fs = microphone_array.fs
        else:
            fs = self.fs

        self.connected_mic_array.add_microphone_array(n_mics, fs, latency)

    def simulate_network(self, **kwargs):
        self.simulate(**kwargs)

        signals = self.mic_array.signals

        return self.connected_mic_array.simulate_latency(signals)


class ConnectedMicrophoneArray:
    def __init__(self):
        self.fs_array = []
        self.latency_array = []
        self.signals = None

    def add_microphone(self, fs, latency=0):
        self.fs_array.append(fs)
        self.latency_array.append(latency)

    def add_microphone_array(
            self, n_microphones, fs=DEFAULT_ROOM_FS, latency=0):

        self.latency_array = _parse_latency(latency, n_microphones)
        self.fs_array += n_microphones*[fs]

    def simulate_latency(self, room_simulation_result):
        self.signals = simulate_latency(
            room_simulation_result,
            self.latency_array,
            self.fs_array
        )

        return self.signals


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
