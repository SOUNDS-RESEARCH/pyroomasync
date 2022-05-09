# pyroomasync

## Introduction

Microphone arrays have been used for many audio signal processing tasks such as source localization and speech enhancement. In an ideal cenario, these microphones are fully synchronized, arriving at the same time at a processing unit which is able to gather and the signals. In practical cenarios, the microphones may be connected using different networks (WiFi versus Ethernet, for example). Furthermore, these devices may have different sampling rates.

This project extends the functionality of the [pyroomacoustics](https://github.com/LCAV/pyroomacoustics/)
package to simulate such asynchronous microphone networks. It allows microphones to have:

* Different latencies with respect to the fusion centre (10ms and 100ms, for example)
* Sampling rate offsets (16.000Hz vs 16.001Hz, for example)

Another important addition is the option to use measured impulse responses instead of simulating them using the image source model.

## Installation

### Option 1: Install as a package
`pip install --index-url https://test.pypi.org/simple/ pyroomasync`

### Option 2: Install requirements and run from directory
1. Optional: Set up and activate a virtual environment such as [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html)
2. Install the requirements using `pip install -r requirements.txt` (Linux and Mac) or `py -m pip install requirements.txt` (Windows)

## Usage
After installing, you can run experiments by running the command `python -m pyroomasync path/to/experiment_config/ output_dir` or `py -m pyroomasync path/to/experiment_config/ output_dir`

## Examples
The `examples` directory contains examples on running simulations using the command line interface, as well as a Notebook showing the programming interface. Please see the README file located in that directory for more information.

## Developement

### Unit tests
A part of this code is covered using unit tests. In order to run them, run `make pytest` or `pytest tests` (Linux or Mac) or `py -m pytest tests` (Windows).


## Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research and innovation
programme under the Marie Skłodowska-Curie grant agreement No 956369

![](docs/eu-emblem.jpg)

Speech samples used were taken from the [VCTK dataset](https://datashare.ed.ac.uk/handle/10283/2950) created at the University of Edinburgh.

Room impulse responses were taken from the [Ace Challenge Corpus](http://www.ee.ic.ac.uk/naylor/ACEweb/index.html)
