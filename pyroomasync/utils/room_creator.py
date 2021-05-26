import json
import librosa

from pyroomasync.connected_room import ConnectedShoeBox


def from_experiment_config_json(file_path_or_json):

    if type(file_path_or_json) == dict:
        experiment_config = file_path_or_json
    else:
        with open(file_path_or_json, "r") as f:
            experiment_config = json.load(f)

    # Infer sampling rates from files, set the room's SR as the lowest
    experiment_config = _add_sampling_rates(experiment_config)
    
    room = ConnectedShoeBox(
        experiment_config["room"]["dims"],
        fs=experiment_config["room"]["fs"]
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


def _add_sampling_rates(experiment_config):
    """Get sampling rates from sources and rirs'
       wav files and add them to experiment config"
       Also, add the minimum value of those as the room's fs,
       which will be used as a reference during the simulation.
    
    Args:
        experiment_config (dict of dicts): json-like dict
                                           with the experiment's config
    """
    fs_array = []

    def _add_fs(config_nodes):
        "A config node may be a 'rirs config' or a 'sources config'"
        for node in config_nodes:
            fs = librosa.get_samplerate(node["signal_file_path"])
            node["fs"] = fs
            fs_array.append(fs)
    
    if "rirs" in experiment_config["room"].keys():
        _add_fs(experiment_config["room"]["rirs"])
    
    _add_fs(experiment_config["sources"])
   

    experiment_config["room"]["fs"] = min(fs_array)

    return experiment_config
