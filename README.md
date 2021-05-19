# pyroomasync

## Introduction

Microphone arrays have been used for many audio signal processing tasks such as source localization and speech enhancement. In an ideal cenario, these microphones are fully synchronized, arriving at the same time at a processing unit which is able to gather and the signals. For some practical cenarios, the microphones may be connected using different networks (WiFi versus Ethernet, for example). Furthermore, these devices may have different sampling rates.

This project extends the functionality of the [pyroomacoustics](https://github.com/LCAV/pyroomacoustics/)
package to simulate such asynchronous microphone networks. It allows microphones to have:

* Different latencies with respect to a processing unit (10ms and 100ms, for example)
* Different sampling rates (16.000Hz vs 32.000Hz, for example)
* Imprecise sampling rates (16.000Hz vs 16.001Hz, for example)


## Installation
Install the required Python packages using `pip install -r requirements.txt`

## Speech samples 
The speech samples used were taken from the [VCTK dataset](https://datashare.ed.ac.uk/handle/10283/2950) created at the University of Edinburgh.

## Running experiments
The `experiments` module contains experiments using Pyroomasync.
You can run experiments by running the command `python -m experiments.runner path_to_experiment_config_file`. For example, you can run `python -m experiments.runner experiments/sample_room_config.json`. The output files for the experiment will be saved in the `logs` folder