import numpy as np

# Simulation parameters
FS = 16000
ABSORPTION = 0.25
MAX_ORDER = 17

# Geometry of the room and location of sources and microphones
ROOM_DIM = np.array([20, 15, 6])
SOURCE_LOC = np.array([2.51, 3.57, 1.7])
MIC_LOC = np.c_[[7, 6.1, 1.3],[6.9, 6.1, 1.3]]

# Place a source of white noise playing for 5 s
SOURCE_SIGNAL = np.random.randn(FS * 5)