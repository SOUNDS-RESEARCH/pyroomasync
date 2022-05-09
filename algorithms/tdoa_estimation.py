"This directory contains some TDOA methods, which in turn are used for SRO estimation"

import numpy as np

from numpy.linalg import solve

from .cross_correlation import gcc_phat, temporal_cross_correlation, get_correlation_lags


def tdoa_estimator(x0, x1, sr, correlation_mode="gcc_phat", parabolic_interpolation=True):
    if correlation_mode == "gcc_phat":
        cross_correlation = gcc_phat(x0, x1)
    elif correlation_mode == "temporal_cross_correlation":
        cross_correlation = temporal_cross_correlation(x1, x2)
    else:
        raise NotImplementedError(f"Mode {correlation_mode} is not supported.")
    
    lag_indexes = get_correlation_lags(x0.shape[0], x1.shape[0], sr)

    if parabolic_interpolation:
        return find_fractional_lag(cross_correlation, lag_indexes)
    else:
        return lag_indexes[np.argmax(cross_correlation)]


def find_fractional_lag(cross_correlation_vector, lag_indexes, mode="solve_system"):
    """Find the peak location of the cross correlation between two signals.
       cross_correlation_vector corresponds to the correlation values between the signals.
       lag_indexes is a vector of the same size as cross_correlation_vector. lag_indexes[i]
       corresponds to the time lag where cross_correlation_vector[i] occurs.
       
       Selecting a peak location from lag_indexes would restrict the peak to be a multiple of the
       signals' sampling rates. To obtain a more precise location, we fit a parabola to this peak location
       as well as its left and right neighbours. We then use the peak of this parabola as a more accurate
       peak value.
       
       Two modes for computing the coefficients (a, b, c) from the parabola ax^2 + bx + c = y are provided.
       The "analytic" mode is recommended, where the coefficients a, b and c were derived analytically.
       The "solve_system" mode is included for educational purposes. This mode finds the coefficients
       by solving a linear system of equations y = Wx, where W and y are computed using the peak and its
       neighbours and x corresponds to the parabola coefficients. 

    """

    peak_idx = np.argmax(np.abs(cross_correlation_vector))
    peak_idx_left, peak_idx_right = peak_idx - 1, peak_idx + 1
    
    x = [
        lag_indexes[peak_idx_left],
        lag_indexes[peak_idx],
        lag_indexes[peak_idx_right]
    ]

    y = [
        cross_correlation_vector[peak_idx_left],
        cross_correlation_vector[peak_idx],
        cross_correlation_vector[peak_idx_right]
    ]

    if mode == "solve_system":
        W = [
            [x[0]**2, x[0], 1],
            [x[1]**2, x[1], 1],
            [x[2]**2, x[2], 1]
        ]
        (a, b, c) = solve(W, y)
        x_vertex = -b/(2*a)
    elif mode == "analytic":
        x_vertex = calc_parabola_vertex_x(x, y)
    # The x coordinate of the vertex of a parabola ax^2 + bx + c is located at -b/(2a)
    return x_vertex


def calc_parabola_vertex_x(x, y):
    """Find the horizontal coordinate of the vertex of the parabola
    defined by points (x[0], y[0]), (x[1], y[1]), (x[2], y[2])

    Credits to https://stackoverflow.com/questions/717762/how-to-calculate-the-vertex-of-a-parabola-given-three-points
    """

    denom = (x[0] - x[1]) * (x[0] - x[2]) * (x[1] - x[2])
    a = (x[2] * (y[1] - y[0]) + x[1] * (y[0] - y[2]) + x[0] * (y[2] - y[1])) / denom
    b = (x[2]*x[2] * (y[0] - y[1]) + x[1]*x[1] * (y[2] - y[0]) + x[0]*x[0] * (y[1] - y[2])) / denom
    c = (x[1] * x[2] * (x[1] - x[2]) * y[0] + x[2] * x[0] * (x[2] - x[0]) * y[1] + x[0] * x[1] * (x[0] - x[1]) * y[2]) / denom

    xv = -b / (2*a)
    #yv = c - b*b / (4*a)
    return xv #, yv
