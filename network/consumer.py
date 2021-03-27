import pika
import librosa
import numpy as np
import os, sys

from settings import (
    CONNECTION_PARAMETERS,
    QUEUE_NAME
)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


class AudioConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE_NAME)

    def consume(self):
        self.channel.basic_consume(
            queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

if __name__ == '__main__':
    try:    
        audio_consumer = AudioConsumer()
        audio_consumer.consume()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
