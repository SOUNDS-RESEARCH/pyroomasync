import numpy as np
import pyroomacoustics as pra


class ConnectedShoeBox(pra.ShoeBox):
    def __init__(self, dims, **kwargs):
        super().__init__(dims, **kwargs)

        self.mic_latencies = []

    def add_microphone_array(self, microphone_array, latency=0):
        super().add_microphone_array(microphone_array)
        n_mics = len(microphone_array)
        self.mic_latencies += _parse_latency(latency, n_mics)

    def simulate(self, **kwargs):
        super().simulate(**kwargs)

        signals = self.mic_array.signals

        return self._apply_latency(signals)

    def _apply_latency(self, signals):
 
        mic_delayed_samples = self.fs*np.array(self.mic_latencies)
        max_delayed_samples = int(mic_delayed_samples.max()) 

        output_signals = np.zeros(
            (signals.shape[0], signals.shape[1] + max_delayed_samples)
        )

        for i in range(signals.shape[0]):
            n_delayed_samples = int(mic_delayed_samples[i])
            output_signals[i, n_delayed_samples:] = signals[i]

        return output_signals 


def _parse_latency(latency, n_mics):
    if type(latency) in (int, float):
        latency = n_mics*[latency]
    elif type(latency) == list:
        n_latency = len(latency)
        if n_latency != n_mics:
            raise ValueError(
                (
                    "The latency array is of size {}. Please provide an array of "
                    "the same size as the microphone positions array ({})"
                ).format(n_latency, n_mics)
            )
    return latency

