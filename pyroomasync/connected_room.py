import numpy as np
import pyroomacoustics as pra
from pyroomacoustics.beamforming import MicrophoneArray


from pyroomasync.asynchronous_microphone_network import (
    AsynchronousMicrophoneNetwork
)
from pyroomasync.settings import DEFAULT_ROOM_FS


class ConnectedShoeBox(pra.ShoeBox):
    def __init__(self, dims, **kwargs):
        super().__init__(dims, fs=DEFAULT_ROOM_FS, **kwargs)

        self.connected_mic_array = AsynchronousMicrophoneNetwork()

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

    def simulate(self, **kwargs):
        super().simulate(**kwargs)
        signals = self.mic_array.signals

        return self.connected_mic_array.simulate(signals)
