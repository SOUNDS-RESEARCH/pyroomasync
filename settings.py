import numpy as np
import pyroomacoustics as pra

FS = 16000
SNR = 0.0  # signal-to-noise ratio
C = 343.0  # speed of sound
NFFT = 256  # FFT size
FREQ_BINS = np.arange(5, 60)  # FFT bins to use for estimation

# Room parameters
ROOM_DIM = np.r_[10.0, 10.0]

# Source parameters
AZIMUTH = 61.0 / 180.0 * np.pi  # 60 degrees
DISTANCE = 3.0  # 3 meters
SOURCE_LOCATION = ROOM_DIM / 2 + DISTANCE * np.r_[np.cos(AZIMUTH), np.sin(AZIMUTH)]
SOURCE_SIGNAL = np.random.randn((NFFT // 2 + 1) * NFFT)

# Microphone location
MIC_LOCATIONS = pra.circular_2D_array(ROOM_DIM / 2, 12, 0.0, 0.15)


