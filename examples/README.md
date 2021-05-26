# Examples

This folder contains some example simulations using pyroomasync.

## Running the examples

### Generating output files using the example config files
From the pyroomasync root directory, run the command `python -m pyroomasync path/to/example_config.json output_dir` to generate the simulation output at `output_dir`.

### Running the Jupyter Notebook examples
From the pyroomasync root directory, run the command `jupyter notebook` to start a jupyter server. Then select the `pyroomasync_usage_example.ipynb` from the file explorer

## Example 1: Big room simulation

The file `big_room_simulation_example.json` defines a 100m³ room. It contains
one microphone at coordinates x=80m, y=80m and height=1m as well as a source at 
x=20m, y=20m and height=1m.

As no RIRs are provided in the config file, pyroomasync will simulate them using pyroomacoustics. You can hear the resulting signal contains a lot of reverberation.

## Example 2: Small room simulation with delayed microphones

The file `small_room_delayed_microphones_simulation_example.json` defines a 3m³ room. It contains two microphones at positions (0.5, 0.5, 1) and (1.5, 1.5, 1) and a source at the middle, at (1, 1, 1). The second microphone has a latency of 100ms with respect to the first one.

As no RIRs are provided in the config file, pyroomasync will simulate them using pyroomacoustics. As the room is small and microphones are close, there is not much reverberation in the resulting signals.

## Example 3: Room simulation using the ACE Challenge Corpus

This simulation uses Room Impulse Responses from the [ACE Challenge](http://www.ee.ic.ac.uk/naylor/ACEweb/index.html). The room and microphone arrangements can be seen in the description of the "lobby" room in the file `examples/data/ace/ACE_Corpus_Microphone_arrangements.pdf`.
