# pyroomasync

## Introduction

Microphone arrays have been used for many audio signal processing tasks such as source localization and speech enhancement. In an ideal cenario, these microphones are fully synchronized, arriving at the same time at a processing unit which is able to gather and the signals. For some practical cenarios, the microphones may be connected using different networks (WiFi versus Ethernet, for example). Furthermore, these devices may have different sampling rates.

This project extends the functionality of the [pyroomacoustics](https://github.com/LCAV/pyroomacoustics/)
package to simulate such asynchronous microphone networks. It allows microphones to have:

* Different latencies with respect to a processing unit (10ms and 100ms, for example)
* Different sampling rates (16.000Hz vs 32.000Hz, for example)
* Imprecise sampling rates (16.000Hz vs 16.001Hz, for example)


## Installation
1. Build the package by running `python -m build`
2. (Recommended) Create a virtual environment (`virtualenv venv`) and activate it
3. Install the package pip install .\dist\pyroomasync_beta-0.0.1-py3-none-any.whl

## Speech samples 
The speech samples used were taken from the [VCTK dataset](https://datashare.ed.ac.uk/handle/10283/2950) created at the University of Edinburgh.

## Running experiments
The `experiments` module contains experiments using Pyroomasync.
You can run experiments by running the command `python -m experiments.run path_to_experiment_config_file`. For example, you can run `python -m experiments.runner pyroomasync/experiments/sample_room_config.json`. The output files for the experiment will be saved in the `logs` folder

## Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research and innovation
programme under the Marie Skłodowska-Curie grant agreement No 956369

![](docs/eu-emblem.jpg)
