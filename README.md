# pyroomasync

## Introduction

Microphone arrays have been used for many audio signal processing tasks such as source localization and speech enhancement. In an ideal cenario, these microphones are fully synchronized, arriving at the same time at a processing unit which is able to gather and the signals. For some practical cenarios, the microphones may be connected using different networks (WiFi versus Ethernet, for example). Furthermore, these devices may have different sampling rates.

This project extends the functionality of the [pyroomacoustics](https://github.com/LCAV/pyroomacoustics/)
package to simulate such asynchronous microphone networks. It allows microphones to have:

* Different latencies with respect to a processing unit (10ms and 100ms, for example)
* Different sampling rates (16.000Hz vs 32.000Hz, for example)
* Imprecise sampling rates (16.000Hz vs 16.001Hz, for example)

Another important addition is the option to use measured impulse responses instead of simulating them using the image source model.

## Installation

### Option 1: Install as a package [Waiting for publication]
`pip install pyroomasync`

### Option 2: Install requirements and run from directory
Install the requirements using `pip install -r requirements.txt`. You may want to do that in a virtual environment such as [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html)

## Running experiments
After installing, you can run experiments by running the command `python -m pyroomasync path_to_experiment_config_file output_dir`. For example, you can run `python -m pyroomasync examples/sample_rir_config.json logs` to save the experiment results in the `logs` folder.

## Examples
The `examples` directory contains examples on running simulations using the command line interface, as well as a Notebook showing the programming interface. Please see the README file located in the directory for more information.

## Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research and innovation
programme under the Marie Skłodowska-Curie grant agreement No 956369

![](docs/eu-emblem.jpg)

Speech samples used were taken from the [VCTK dataset](https://datashare.ed.ac.uk/handle/10283/2950) created at the University of Edinburgh.

Room impulse responses were taken from the [Ace Challenge Corpus](http://www.ee.ic.ac.uk/naylor/ACEweb/index.html)