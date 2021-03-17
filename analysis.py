from estimators import extract_features, locate_sources

def compare_doa_estimators(room):
    input_signals = room.mic_array.signals
    features = extract_features(input_signals)
    locate_sources(features)
