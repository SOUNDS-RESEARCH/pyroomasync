import numpy as np

from scipy.stats import linregress

from tqdm import tqdm
from.tdoa_estimation import tdoa_estimator


def naive_sro_estimator(x0, x1,
                        sr,
                        frame_size_in_secs=0.3,
                        hop_percent=0.5,
                        correlation_mode="gcc_phat",
                        parabolic_interpolation=True,
                        output_type="samples_per_second"):
    """Estimate the sampling rate offset between two microphones by assuming their relative delay,
    equivalent to their Time Difference of Arrival (TDOA) increases linearly due to the Sampling Rate Offset (SRO)
    between them. Note that this assumes that there is a single stationary source. The steps of the algorithm are:

    1. Dividing the signals into multiple frames and computing the TDOA between them.
    2. Fitting these points to a line y = ax + b. The slope 'a' of this line is the estimated SRO.

    Args:
        x0, x1 (np.ndarray): microphone signals of same size
        sr (float): Base sampling rate of the microphones
        frame_size_in_secs (float): Size of the frames used to compute a TDOA
        hop_percent (float): Dictates the interval between two frames. Default is 0.5, meaning that frames will overlap by 50%. 
        correlation_mode (str, optional): Correlation method to use for TDOA estimation.
                                          Available ones are 'temporal_cross_correlation' and 'gcc_phat' (default).
        parabolic_interpolation (bool, optional): If 'False' the TDOAs will be multiples of the sampling period.
        output_type (str, optional): SRO output type. Available options are Parts Per Million ('ppm') and 'samples_per_second'.
                                     Note that 'samples_per_second' is relative to the base sampling rate sr.
    """

    if x0.shape != x1.shape:
        raise ValueError("Microphone signals must have the same size")
    
    frame_size_in_samples = int(frame_size_in_secs*sr)
    hop_size_in_samples = int(hop_percent*frame_size_in_samples)


    # 1. Compute a TDOA for each frame
    n_frames = np.floor((x0.shape[0] -  frame_size_in_samples)/hop_size_in_samples)
    frame_start_idxs = np.arange(0, n_frames*hop_size_in_samples, hop_size_in_samples, dtype=int)
    tdoas = []
    for frame_start_idx in tqdm(frame_start_idxs):
        frame_end_idx = frame_start_idx + frame_size_in_samples
        x0_frame = x0[frame_start_idx:frame_end_idx]
        x1_frame = x1[frame_start_idx:frame_end_idx]

        tdoa = tdoa_estimator(x0_frame, x1_frame, sr, correlation_mode, parabolic_interpolation)
        tdoas.append(tdoa)
    tdoas = np.stack(tdoas)

    # 2. Fit a slope to the computed TDOAs
    regression_result = linregress(frame_start_idxs/sr, tdoas)
    
    print(f"Sampling rate offset (ppm)={regression_result.slope*1e6}")
    print(f"Sampling rate offset (samples/second @{sr}Hz)={regression_result.slope*sr}")

    if output_type == "ppm":
        return regression_result.slope*1e6
    elif output_type == "samples_per_second":
        return regression_result.slope*sr

