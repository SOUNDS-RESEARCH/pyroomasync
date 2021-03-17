from estimators import extract_features, locate_sources
from logger import log_room


def compare_doa_estimators(room):
    input_signals = room.mic_array.signals
    features = extract_features(input_signals)
    return locate_sources(features)
