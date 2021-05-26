import argparse
import os
from pathlib import Path

from pyroomasync.utils.room_creator import from_experiment_config_json
from pyroomasync.utils.logger import SimulationLogger
from pyroomasync.simulator import simulate

def parse_args():
    parser = argparse.ArgumentParser(description="Run an experiment from a config file")  # noqa
    parser.add_argument(
        "config_file_path", type=str,
        help="Configuration file for the experiment"
    )
    parser.add_argument(
        "output_dir", type=str, default="logs/",
        help="Configuration file for the experiment"
    )
    
    return parser.parse_args()


def run_experiment(config_file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_dir = Path(output_dir)

    experiment_name = Path(config_file_path).name.replace(".json", "")
    experiment_dir = output_dir / experiment_name
    logger = SimulationLogger(experiment_dir)
    
    room = from_experiment_config_json(config_file_path)
    simulation_results = simulate(room)

    logger.log(room, simulation_results)


if __name__ == "__main__":
    parser = parse_args()
    run_experiment(parser.config_file_path, parser.output_dir)
