from pyroomacoustics.beamforming import circular_microphone_array_xyplane

from .settings import DEFAULT_ROOM_FS


class MicrophoneNetwork:
    def __init__(self, base_fs=DEFAULT_ROOM_FS):
        self.mic_array = []
        self.base_fs = base_fs

    def add(self, loc, fs=None, delay=0, gain=1, id=None):
        if fs is None:
            fs = self.base_fs
        
        if id is None:
            # Create sequential id
            id = str(len(self))
        
        self.mic_array.append(
            Microphone(id, loc, fs, delay, gain)
        )

    def add_array(self, loc_array, fs=None, delay=0, gain=1, id=None):

        n_microphones = len(loc_array)
        id_array = _parse_id(id, n_microphones, len(self))
        delay_array = _parse_input_value(delay, n_microphones)
        fs_array = _parse_input_value(fs, n_microphones)
        gain_array = _parse_input_value(gain, n_microphones)

        for i in range(n_microphones):
            self.add(
                loc_array[i],
                fs_array[i],
                delay_array[i],
                gain_array[i],
                id_array[i]
            )

    def get_delays(self):
        return [m.delay for m in self.mic_array]
    
    def get_gains(self):
        return [m.gain for m in self.mic_array]
    
    def get_positions(self):
        return [m.loc for m in self.mic_array]

    def get_fs(self):
        return [m.fs for m in self.mic_array]

    def get_ids(self):
        return [m.id for m in self.mic_array]

    def __len__(self):
        return len(self.mic_array)


class Microphone:
    def __init__(self, id, loc, fs, delay, gain):
        self.id = id
        self.loc = loc
        self.fs = fs
        self.delay = delay
        self.gain = gain


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


def _parse_input_value(value, n_mics):
    if type(value) in (int, float):
        value = n_mics*[value]
    elif type(value) == list:
        n_value = len(value)
        if n_value != n_mics:
            raise ValueError(
                (
                    "The array is of size {}. Please provide an array of "
                    "the same size as the microphone positions array ({})"
                ).format(n_value, n_mics)
            )
    return value
