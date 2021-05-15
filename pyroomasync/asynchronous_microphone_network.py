from pyroomasync.filters import simulate_latency, simulate_sampling_rates
from pyroomasync.settings import DEFAULT_ROOM_FS


class AsynchronousMicrophoneNetwork:
    def __init__(self):
        self.fs_array = []
        self.latency_array = []
        self.signals = None

    def add_microphone(self, fs, latency=0):
        self.fs_array.append(fs)
        self.latency_array.append(latency)

    def add_microphone_array(
            self, n_microphones, fs=DEFAULT_ROOM_FS, latency=0):

        self.latency_array = _parse_latency(latency, n_microphones)
        self.fs_array += n_microphones*[fs]

    def simulate(self, room_simulation_result):
        self.signals = simulate_latency(
            room_simulation_result,
            self.latency_array,
            self.room_fs
        )

        self.signals = simulate_sampling_rates(
            self.signals,
            self.fs_array,
            self.room_fs
        )

        return self.signals


def _parse_latency(latency, n_mics):
    if type(latency) in (int, float):
        latency = n_mics*[latency]
    elif type(latency) == list:
        n_latency = len(latency)
        if n_latency != n_mics:
            raise ValueError(
                (
                    "The latency array is of size {}. Please provide an array of "
                    "the same size as the microphone positions array ({})"
                ).format(n_latency, n_mics)
            )
    return latency
