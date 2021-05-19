from pyroomasync.settings import DEFAULT_ROOM_FS


class Sources:
    def __init__(self):
        self.source_array = []

    def add(self, loc, signal, fs=DEFAULT_ROOM_FS, id=None):
        if id is None:
            # Create sequential id
            id = str(len(self))

        self.source_array.append(
            Source(id, loc, signal, fs)
        )
    
    def add_array(self, loc_array, fs=DEFAULT_ROOM_FS, base_id=None):

        n_sources = len(loc_array)
        id_array = _parse_id(base_id, n_sources, len(self))

        for i in range(n_sources):
            self.add(id_array[i], loc_array[i], fs)

    def __len__(self):
        return len(self.source_array)


class Source:
    def __init__(self, id, loc, signal, fs):
        self.id = id
        self.loc = loc
        self.signal = signal
        self.fs = fs


def _parse_id(id, n_sources_to_add, n_current_sources):
    if id is None:
        return [
            str(n_current_sources + i)
            for i in range(n_sources_to_add)
        ]
    elif type(id) == str:
        return [
            f"{id}_{i}" for i in range(n_sources_to_add)
        ]
    elif type(id) == list:
        n_id = len(id)
        if n_id != n_sources_to_add:
            raise ValueError(
                (
                    "The id array is of size {}. Please provide an array of "
                    "the same size as the microphone positions array ({})"
                ).format(n_id, n_sources_to_add)
            )
    return id