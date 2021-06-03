from scipy.signal import correlate


def from_simulation_results(simulation_results, simulation_fs):
    n_microphones = simulation_results.shape[0]

    tdoas = {}
    for n_microphone_1 in range(n_microphones):

        for n_microphone_2 in range(n_microphone_1, n_microphones):
            key = (n_microphone_1, n_microphone_2)
            tdoas[key] = compute_tdoa(
                simulation_results[n_microphone_1],
                simulation_results[n_microphone_2],
                simulation_fs
            )


def compute_tdoa(signal_1, signal_2, simulation_fs):
    correlation = correlate(signal_1, signal_2, mode="same")

    max_lag_in_samples = correlation.argmax()
    max_lag_in_time = max_lag_in_samples/simulation_fs
    max_lag_in_meters = max_lag_in_time
