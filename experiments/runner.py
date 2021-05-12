import argparse
from pathlib import Path

from experiments.common.room_creator import from_experiment_config_json
from experiments.common.logger import SimulationLogger

BASE_LOG_DIR = Path("logs/")


def parse_args():
    parser = argparse.ArgumentParser(description="Run an experiment from a config file")  # noqa
    parser.add_argument(
        "config_file_path", type=str,
        help="Configuration file for the experiment"
    )
    return parser.parse_args()


def run_experiment(config_file_path):
    room = from_experiment_config_json(config_file_path)
    room.simulate_network()

    experiment_name = Path(config_file_path).name.replace(".json", "")
    experiment_dir = BASE_LOG_DIR / experiment_name
    logger = SimulationLogger(experiment_dir)
    logger.log(room)


if __name__ == "__main__":
    parser = parse_args()
    run_experiment(parser.config_file_path)
    

