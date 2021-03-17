import numpy as np
import pyroomacoustics as pra

SR = 16000
C = 343.0  # speed of sound
NFFT = 256  # FFT size
FREQ_BINS = np.arange(5, 60)  # FFT bins to use for estimation

# Room parameters
ROOM_DIM = np.r_[10.0, 10.0]


# Microphone location
MIC_LOCATIONS = pra.circular_2D_array(ROOM_DIM / 2, 6, 0.0, 0.15)
MIC_LOCATIONS = np.c_[
    [4.0, 4.0],  # mic 1
    [6.0, 4.0],  # mic 2
]

# Source parameters
SOURCE_AZIMUTH = 61.0 / 180.0 * np.pi  # 60 degrees
DISTANCE = 3.0  # 3 meters
SOURCE_LOCATION = ROOM_DIM / 2 + DISTANCE * np.r_[np.cos(SOURCE_AZIMUTH), np.sin(SOURCE_AZIMUTH)]
SIGNAL_DURATION_IN_SECONDS = 2
#SOURCE_SIGNAL = np.random.randn(SIGNAL_DURATION_IN_SECONDS*SR)
F0 = 2500
SOURCE_SIGNAL = np.sin(np.arange(SIGNAL_DURATION_IN_SECONDS*SR)*F0)

# Room noise parameters
SNR = 0.0  # signal-to-noise ratio
ROOM_NOISE_VARIANCE = 10 ** (-SNR / 10) / (4.0 * np.pi * DISTANCE) ** 2