from pyroomasync.settings import DEFAULT_ROOM_FS
from pyroomasync.simulator import simulate


class Microphones:
    def __init__(self, base_fs=DEFAULT_ROOM_FS):
        self.id_array = []
        self.fs_array = []
        self.latency_array = []
        self.loc_array = []

        self.mic_array = []
        self.base_fs = base_fs

        # variable storing simulation results
        self.signals = None

    def add(self, loc, fs=None, latency=0, id=None):
        if fs is None:
            fs = self.base_fs
        
        if id is None:
            # Create sequential id
            id = str(len(self))
        
        self.mic_array.append(
            Microphone(id, loc, fs, latency)
        )

    def add_array(self, loc_array, fs=None, latency=0, id=None):

        n_microphones = len(loc_array)
        id_array = _parse_id(id, n_microphones, len(self))
        latency_array = _parse_latency(latency, n_microphones)

        for i in range(n_microphones):
            self.add(
                loc_array[i],
                fs,
                latency_array[i],
                id_array[i]
            )

    def get_latencies(self):
        return [m.latency for m in self.mic_array]

    def get_fs(self):
        return [m.fs for m in self.mic_array]

    def __len__(self):
        return len(self.loc_array)


class Microphone:
    def __init__(self, id, loc, fs, latency):
        self.id = id
        self.loc = loc
        self.fs = fs
        self.latency = latency


def _parse_id(id, n_mics_to_add, current_n_mics_in_network):
    if id is None:
        return [
            str(current_n_mics_in_network + i)
            for i in range(n_mics_to_add)
        ]
    elif type(id) == str:
        return [
            f"{id}_{i}" for i in range(n_mics_to_add)
        ]
    elif type(id) == list:
        n_id = len(id)
        if n_id != n_mics_to_add:
            raise ValueError(
                (
                    "The id array is of size {}. Please provide an array of "
                    "the same size as the microphone positions array ({})"
                ).format(n_id, n_mics_to_add)
            )
    return id


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
