from experiments.common.room_creator import from_experiment_config_json


def test_from_experiment_config_json():
    file_path = "tests/fixtures/sample_room_config.json"
    connected_room = from_experiment_config_json(file_path)

    assert connected_room.n_sources == 1
    assert connected_room.n_mics == 3
    assert connected_room.mic_fs == [16001, 15999, 32000]
    assert connected_room.mic_latencies == [0, 0.01, 0.02]

    connected_room.simulate_network()
