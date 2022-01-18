from typing import List
import librosa
import numpy as np
from pyroomacoustics import ShoeBox

from pyroomasync.microphone_network import MicrophoneNetwork
from pyroomasync.sources import Sources
from pyroomasync.rirs import Rirs
from pyroomasync.settings import DEFAULT_ROOM_FS


class ConnectedShoeBox:
    def __init__(self, dims, fs=DEFAULT_ROOM_FS, **kwargs):
        self.pyroomacoustics_engine = ShoeBox(
            dims, fs=fs, **kwargs
        )

        self.dims = dims
        self.fs = fs
        self.microphone_network = MicrophoneNetwork(base_fs=fs)
        self.sources = Sources()
        self.rirs = Rirs()
        self.n_mics = 0
        self.n_sources = 0


    def add_microphone(self, loc: List, fs=None, delay=0, gain=1, id=None):
        if fs is None:
            fs = self.fs
        self.microphone_network.add(loc, fs, delay, gain, id)
        
        self.pyroomacoustics_engine.add_microphone(loc, fs=self.fs)
        self.n_mics += 1

    def add_microphone_array(self, microphone_array: List[List],
                             delay=0, fs=None, gain=1, id=None):
        n_mics = len(microphone_array)

        if fs is None:
            fs = self.fs

        self.microphone_network.add_array(microphone_array, fs, delay, gain, id)
        
        # Pyroomacoustics use input microphone locations as (dim, n_mics)
        microphone_array = np.array(microphone_array).T
        self.pyroomacoustics_engine.add_microphone_array(microphone_array)
        
        self.n_mics += n_mics

    def add_source(self, coordinates, signal, id=None):
        if type(signal) == str:
            signal = librosa.load(signal, sr=self.fs, mono=True)[0]
        self.sources.add(coordinates, signal, id=id)
        self.pyroomacoustics_engine.add_source(coordinates, signal=signal)
        self.n_sources += 1


    def add_rir(self, signal, mic_id, source_id):
        if type(signal) == str:
            signal = librosa.load(signal, sr=self.fs, mono=True)[0]
        self.rirs.add(signal, mic_id, source_id)