import matplotlib.pyplot as plt
import matplotlib.patches as patches
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


def plot_room_2d(room, output_path=None, axs=None, mode="row"):
    if axs is None:
        if mode == "row":
            n_rows, n_cols = (1, 2)
            figsize = (5, 7)
        elif mode == "col":
            n_rows, n_cols = (2, 1)
            figsize = (7, 5)
        fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=figsize)

    _plot_room_2d(room, axs[0])
    _plot_room_2d(room, axs[1], mode="xz")

    plt.tight_layout()
    if output_path is not None:
        plt.savefig(output_path)

def _plot_room_2d(room, ax=None, output_path=None, mode="xy"):
    margin = 0.25 # Add a 0.25m margin to plot the room rectangle

    if ax is None:
        _, ax = plt.subplots()

    if mode == "xy":
        idxs = [0, 1]
        labels = ["width", "length"]
        title = "Aerial view"
    elif mode == "xz":
        idxs = [0, 2]
        labels = ["width", "height"]
        title = "Lateral view"

    ax.set_xlim(-margin, room.dims[idxs[0]] + margin)
    ax.set_ylim(-margin, room.dims[idxs[1]] + margin)
    
    mics = room.microphone_network.mic_array
    sources = room.sources.source_array
    
    mics_x = [mic.loc[idxs[0]] for mic in mics]
    mics_y = [mic.loc[idxs[1]] for mic in mics]
    sources_x = [source.loc[idxs[0]] for source in sources]
    sources_y = [source.loc[idxs[1]] for source in sources]
    
    # Draw room boundaries as a rectangle
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            room.dims[0],
            room.dims[1],
            color="g",
            fill=False,
            linewidth=3
    ))
    ax.scatter(mics_x, mics_y, marker="o", label="microphones")
    ax.scatter(sources_x, sources_y, marker="x", label="sources")

    ax.set_aspect("equal")
    ax.set_xlabel(f"Room {labels[0]} (m)")
    ax.set_ylabel(f"Room {labels[1]} (m)")
    ax.set_title(title)

    ax.legend()
    ax.grid()
    
    if output_path is not None:
        plt.savefig(output_path)

    return ax


def _plot_spectogram(signal):
    D = librosa.stft(signal)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    librosa.display.specshow(S_db, x_axis='time', y_axis='linear')
