from pyroomasync.simulator import simulate
from experiments.room_creator import from_experiment_config_json


def test_from_experiment_config_json():
    file_path = "tests/fixtures/sample_room_config.json"
    connected_room = from_experiment_config_json(file_path)

    assert connected_room.n_sources == 1
    assert connected_room.n_mics == 3
    assert connected_room.microphones.get_fs() == [16001, 15999, 32000]
    assert connected_room.microphones.get_latencies() == [0, 0.01, 0.02]

    simulation_results = simulate(connected_room)
    assert simulation_results.shape == (3, 92416)


def test_from_experiment_config_json_rir():
    file_path = "tests/fixtures/sample_rir_config.json"
    connected_room = from_experiment_config_json(file_path)

    assert connected_room.n_sources == 1
    assert connected_room.n_mics == 2
    assert connected_room.microphones.get_fs() == [16001, 15999]
    assert connected_room.microphones.get_latencies() == [0.1, 0]

    simulation_results = simulate(connected_room)
    assert simulation_results.shape == (2, 137141)
