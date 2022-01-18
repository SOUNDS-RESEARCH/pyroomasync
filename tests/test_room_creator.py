from pyroomasync.simulator import simulate
from pyroomasync.utils.room_creator import from_experiment_config_json


def test_from_experiment_config_json():
    file_path = "tests/fixtures/sample_room_config.json"
    room = from_experiment_config_json(file_path)
    
    assert room.n_sources == 1
    assert room.n_mics == 3
    assert room.microphone_network.get_fs() == [16001, 15999, 32000]
    assert room.microphone_network.get_delays() == [0, 0.01, 0.02]
    assert room.microphone_network.get_gains() == [1, 1, 1]

    simulation_results = simulate(room)
    assert simulation_results.shape == (3, 100260)


def test_from_experiment_config_json_rir():
    file_path = "tests/fixtures/sample_rir_config.json"
    room = from_experiment_config_json(file_path)

    assert room.n_sources == 1
    assert room.n_mics == 2
    assert room.microphone_network.get_fs() == [16001, 15999]
    assert room.microphone_network.get_delays() == [0.1, 0]

    simulation_results = simulate(room)
    assert simulation_results.shape == (2, 146068)
