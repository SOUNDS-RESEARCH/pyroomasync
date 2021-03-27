import pika 

# AMPQ Configuration
CONNECTION_PARAMETERS = pika.ConnectionParameters('localhost')
QUEUE_NAME = "microphone"

# Audio configuration
BLOCK_SIZE = 1024 # Send audio in blocks of 1024 samples
