import os
import pandas as pd

from estimators import create_estimators, extract_features
from settings import BASE_OUTPUT_DIR
from input_signals import signal_types
from simulator import Simulation


def compare_doa_estimators(room, output_dir):
    input_signals = room.mic_array.signals
    features = extract_features(input_signals)

    estimators = create_estimators(output_dir)
    
    return {
        estimator.estimator_name:estimator.locate_sources(features)[0]
        for estimator in estimators
    }

def compare_results_for_input_signals():
    if not os.path.exists(BASE_OUTPUT_DIR):
        os.mkdir(BASE_OUTPUT_DIR)

    available_signal_types = signal_types()
    
    estimation_results = []
    for signal_type in available_signal_types:
        output_dir = os.path.join(BASE_OUTPUT_DIR, signal_type)
        simulator = Simulation(signal_type, output_dir)
        simulation_result = simulator.run()
        
        estimation_result = compare_doa_estimators(
            simulation_result, output_dir)
        estimation_results.append(estimation_result)

    df = pd.DataFrame(estimation_results)
    df.to_csv(os.path.join(BASE_OUTPUT_DIR, "results.csv"))