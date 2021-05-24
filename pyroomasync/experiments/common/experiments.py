import os

from pyroomasync.experiments.common.estimators import create_estimators, extract_features
from pyroomasync.experiments.common.settings import BASE_OUTPUT_DIR
from pyroomasync.experiments.common.create_signal import signal_types
from pyroomasync.experiments.common.simulator import Simulation
from pyroomasync.experiments.common.logger import ExperimentLogger


def compare_doa_estimators(input_signals, output_dir):
    features = extract_features(input_signals)

    estimators = create_estimators(output_dir)

    return {
        estimator.estimator_name: estimator.locate_sources(features)[0]
        for estimator in estimators
    }


def compare_results_for_input_signals():
    logger = ExperimentLogger(BASE_OUTPUT_DIR)

    available_signal_types = signal_types()

    estimation_results = []
    for signal_type in available_signal_types:
        output_dir = os.path.join(BASE_OUTPUT_DIR, signal_type)
        simulator = Simulation(signal_type, output_dir)
        simulation_result = simulator.run()

        estimation_result = compare_doa_estimators(
            simulation_result, output_dir)
        estimation_result["SIGNAL_TYPE"] = signal_type
        estimation_results.append(estimation_result)

    logger.log(estimation_results)