import pika
import librosa
import numpy as np

from settings import (
    CONNECTION_PARAMETERS,
    QUEUE_NAME,
    BLOCK_SIZE
)


def _load_blocks(audio_signal_path):
    signal, sr = librosa.load(audio_signal_path)
    n_blocks = int(signal.shape[0]/BLOCK_SIZE)

    blocks = np.reshape(
        signal[:int(n_blocks*BLOCK_SIZE)],
        (n_blocks, BLOCK_SIZE)
    )

    return blocks


class AudioPublisher:
    def __init__(self):

        self.connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE_NAME)

    def publish(self, audio_signal_path):

        blocks = _load_blocks(audio_signal_path)

        for block in blocks:
            block_str = block.tobytes()
            self.channel.basic_publish(exchange='',
                                routing_key=QUEUE_NAME,
                                body=block_str)



if __name__ == "__main__":
    audio_publisher = AudioPublisher()
    audio_publisher.publish("../speech_samples/p225_001.wav")
