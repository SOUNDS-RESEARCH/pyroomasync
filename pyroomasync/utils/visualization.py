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




def plot_room_2d(room, ax=None):

    if ax is None:
        ax = plt.gca()
        
    ax.set_xlim(0, room.dims[0])
    ax.set_ylim(0, room.dims[1])
    
    mics = room.microphones.mic_array
    sources = room.sources.source_array
    
    mics_x = [mic.loc[0] for mic in mics]
    mics_y = [mic.loc[1] for mic in mics]
    sources_x = [source.loc[0] for source in sources]
    sources_y = [source.loc[1] for source in sources]
    
    ax.scatter(mics_x, mics_y, marker="^", label="microphones")
    ax.scatter(sources_x, sources_y, marker="o", label="sources")
    ax.legend()
    ax.grid()
    
    return ax


def _plot_spectogram(signal):
    D = librosa.stft(signal)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    librosa.display.specshow(S_db, x_axis='time', y_axis='linear')
