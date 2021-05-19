import json

from pyroomasync.connected_room import ConnectedShoeBox


def from_experiment_config_json(file_path):
    with open(file_path, "r") as f:
        experiment_config = json.load(f)

    room = ConnectedShoeBox(
        experiment_config["room"]["dims"]
    )

    if "rirs" in experiment_config["room"].keys():
        _add_rirs(room, experiment_config["room"]["rirs"])
        

    _add_microphones(room, experiment_config["microphones"])
    _add_sources(room, experiment_config["sources"])


    return room


def _add_microphones(room, mics_config):
    for mic_config in mics_config:
        room.add_microphone(
            mic_config["location"],
            fs=mic_config["sr"],
            latency=mic_config["latency"],
            id=mic_config.get("id", None)
        )


def _add_sources(room, sources_config):
    for source_config in sources_config:   
        room.add_source(
            source_config["location"],
            source_config["signal_file_path"],
            id=source_config.get("id", None)
        )


def _add_rirs(room, rirs_config):
    for rir_config in rirs_config:
        room.add_rir(
            rir_config["signal_file_path"],
            rir_config["microphone_id"],
            rir_config["source_id"]
        )