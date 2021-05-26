import matplotlib.pyplot as plt
import numpy as np
import librosa, librosa.display


def plot_microphone_signals(mic_signals, output_path=None):
    plt.figure()

    n_mics = mic_signals.shape[0]
    for i, mic_signal in enumerate(mic_signals):
        plt.subplot(n_mics, 1, i + 1)
        _plot_spectogram(mic_signal)
        plt.title('Microphone {} signal'.format(i))
        plt.xlabel('Time [s]')
    #plt.colorbar(format="%+2.f dB")
    plt.tight_layout()

    if output_path is not None:
        plt.savefig(output_path)
    else:
        plt.show()


def plot_room(room, output_path=None):
    room.pyroomacoustics_engine.plot()

    if output_path is not None:
        plt.savefig(output_path)
    else:
        plt.show()


def _plot_spectogram(signal):
    D = librosa.stft(signal)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    librosa.display.specshow(S_db, x_axis='time', y_axis='linear')

    
def plot_dirac(estimator, output_path, ground_truth):
    estimator.polar_plt_dirac(azimuth_ref=np.array([ground_truth]))
    plt.savefig(output_path)
