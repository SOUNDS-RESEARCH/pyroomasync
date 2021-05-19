from pyroomasync.settings import DEFAULT_ROOM_FS


class Sources:
    def __init__(self):
        self.source_array = []

    def add(self, id, loc, signal, fs=DEFAULT_ROOM_FS):

        self.source_array.append(
            Source(id, loc, signal, fs)
        )

    def __len__(self):
        return len(self.id_array)


class Source:
    def __init__(self, id, loc, signal, fs):
        self.id = id
        self.loc = loc
        self.signal = signal
        self.fs = fs
