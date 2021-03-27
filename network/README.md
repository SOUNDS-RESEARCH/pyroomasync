# microphone-broker

## Intallation
1. Install Docker
2. Download the Rabbitmq image: `docker pull rabbitmq`
3. Run Rabbitmq: `docker run -d --hostname my-rabbit --name some-rabbit rabbitmq:3-management`
4. Send a message: `python sender.py`

## Monitoring
http://localhost:15672/