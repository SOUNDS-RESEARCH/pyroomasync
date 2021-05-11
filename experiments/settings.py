import numpy as np
import pyroomacoustics as pra

SR = 16000
C = 343.0  # speed of sound
NFFT = 256  # FFT size
FREQ_BINS = np.arange(5, 60)  # FFT bins to use for estimation

# Room parameters
ROOM_DIM = np.r_[10.0, 10.0]

# Microphone location
MIC_LOCATIONS = np.c_[
    [4.0, 4.0],  # mic 1
    [6.0, 4.0],  # mic 2
]

# Source parameters
SOURCE_AZIMUTH_IN_DEGREES = 60.0
SOURCE_AZIMUTH_IN_RADIANS = (SOURCE_AZIMUTH_IN_DEGREES - 1)/ 180.0 * np.pi
DISTANCE = 3.0  # 3 meters
LOW_FREQ_IN_HZ = 50
HIGH_FREQ_IN_HZ = 2500

SIGNAL_DURATION_IN_SECONDS = 2
SIGNAL_TYPE = "noise"

# Room noise parameters
SNR = 0.0  # signal-to-noise ratio
ROOM_NOISE_VARIANCE = 10 ** (-SNR / 10) / (4.0 * np.pi * DISTANCE) ** 2


# Logging
BASE_OUTPUT_DIR = "results/"