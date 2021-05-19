import librosa
from pyroomacoustics import ShoeBox
from pyroomacoustics.beamforming import MicrophoneArray

from pyroomasync.microphones import Microphones
from pyroomasync.sources import Sources
from pyroomasync.rirs import Rirs, convolve
from pyroomasync.settings import DEFAULT_ROOM_FS


class ConnectedShoeBox:
    def __init__(self, dims, fs=DEFAULT_ROOM_FS, **kwargs):
        self.pyroomacoustics_engine = ShoeBox(
            dims, fs=DEFAULT_ROOM_FS, **kwargs
        )

        self.fs = fs
        self.microphones = Microphones()
        self.sources = Sources(base_fs=fs)
        self.rirs = Rirs()
        self.n_mics = 0
        self.n_sources = 0

    def add_microphone(self, loc, fs=None, latency=0):
        if fs is None:
            fs = self.fs
        self.microphones.add(loc, fs, latency)
        
        self.pyroomacoustics_engine.add_microphone(loc, fs=self.fs)
        self.n_mics += 1

    def add_microphone_array(self, microphone_array, latency=0):
        n_mics = len(microphone_array)

        if isinstance(microphone_array, MicrophoneArray):
            fs = microphone_array.fs
        else:
            fs = self.fs

        self.microphones.add_array(microphone_array, fs, latency)
        self.pyroomacoustics_engine.add_microphone_array(microphone_array)
        
        self.n_mics += n_mics

    def add_source(self, coordinates, signal, id=None):
        if type(signal) == str:
            signal = librosa.load(signal, sr=self.fs)[0]
        
        self.sources.add(signal, coordinates, id=id)
        self.pyroomacoustics_engine.add_source(coordinates, signal=signal)
        self.n_sources += 1
