### Setup
* Setup virtualenv or any other python 3 installion
* Install requirements.txt
* Create and source .env file
* Use Makefile to run everything

### Example .env file
```
# Set necessary paths
PYTHONPATH=~/dev/python/switch
PROTOC=~/dev/protobuf/bin/protoc

# Server configuration
INCOMING_PORT=5556
OUTGOING_PORT=5566
INCOMING_TOPIC=Data_1A
OUTGOING_TOPIC=Predictions_1A
```

## Design
switch/server.py

* Creates a sub socket for producers to connect to
* Creates a pub socket for consumers to connect to
* Gets instantiated with a specific ML model that will be used during message handling
