import matplotlib.pyplot as plt
import numpy as np

from settings import FS

def _plot_microphone_signals(mic_signals):
    plt.figure()
    plt.subplot(1,2,1)
    plt.plot(np.arange(mic_signals.shape[1]) / FS, mic_signals[0])
    plt.title('Microphone 0 signal')
    plt.xlabel('Time [s]')
    plt.subplot(1,2,2)
    plt.plot(np.arange(mic_signals.shape[1]) / FS, mic_signals[1])
    plt.title('Microphone 1 signal')
    plt.xlabel('Time [s]')
    plt.tight_layout()


def plot_simulation_results(room):
    mic_signals = room.mic_array.signals
    _plot_microphone_signals(mic_signals)
    
    # Plot the room and the image sources
    room.plot(img_order=4)
    plt.title('The room with 4 generations of image sources')

    # Plot the impulse responses
    plt.figure()
    room.plot_rir()

    plt.show()