import json
import librosa

from pyroomasync.connected_room import ConnectedShoeBox


def from_experiment_config_json(file_path):
    with open(file_path, "r") as f:
        experiment_config = json.load(f)

    room = ConnectedShoeBox(
        experiment_config["room"]["dims"]
    )

    for source_config in experiment_config["sources"]:
        _add_source(room, source_config)

    for mic_config in experiment_config["microphones"]:
        _add_microphone(room, mic_config)

    return room


def _add_microphone(room, mic_config):
    room.add_microphone(
        mic_config["location"],
        fs=mic_config["sr"],
        latency=mic_config["latency"]
    )

def _add_source(room, source_config):
    signal = librosa.load(source_config["signal_file_path"], sr=room.fs)[0]
    room.add_source(
        source_config["location"],
        signal
    )
