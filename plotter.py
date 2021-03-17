import matplotlib.pyplot as plt
import numpy as np
import librosa, librosa.display

from settings import SR

def _plot_spectogram(signal):
    D = librosa.stft(signal)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    librosa.display.specshow(S_db, x_axis='time', y_axis='linear')

def plot_microphone_signals(mic_signals, output_path):
    plt.figure()

    n_mics = mic_signals.shape[0]
    for i, mic_signal in enumerate(mic_signals):
        plt.subplot(n_mics, 1, i + 1)
        _plot_spectogram(mic_signal)
        plt.title('Microphone {} signal'.format(i))
        plt.xlabel('Time [s]')
    #plt.colorbar(format="%+2.f dB")
    plt.tight_layout()
    plt.savefig(output_path)
    

def plot_dirac(estimator, output_path):
    estimator.polar_plt_dirac()
    plt.savefig(output_path)


def plot_room(room, output_path):
    room.plot()
    plt.savefig(output_path)



