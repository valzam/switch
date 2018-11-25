import os
import switch
import zmq
import sys
from multiprocessing import Process
import requests

def run_server():
    context = zmq.Context()
    predictor = switch.Predictor()
    server_config = switch.ServerConfig(predictor=predictor,
                                      incoming_port=os.environ.get("INCOMING_PORT"),
                                      outgoing_port=os.environ.get("OUTGOING_PORT"),
                                      incoming_topic=os.environ.get("INCOMING_TOPIC"),
                                      outgoing_topic=os.environ.get("OUTGOING_TOPIC"))
    server = switch.Server(server_config)
    discovery = switch.Discovery(os.environ.get("DISCOVERY_PORT"))
    discovery.register_server(server)

    # Start the discovery in its own process
    Process(target=discovery.start, args=(context,)).start()

    server.start(context)

def run_producer():
    from switch.producer import main
    main(os.environ.get("INCOMING_PORT"),
         os.environ.get("INCOMING_TOPIC"))


def run_discovery():
    context = zmq.Context()
    discovery = switch.Discovery(os.environ.get("DISCOVERY_PORT"))
    discovery.start(context)

def ping_discovery():
    rep = requests.get(f"http://localhost:{os.environ.get('DISCOVERY_PORT')}")
    print(rep.json())

if __name__ == "__main__":
    if sys.argv[1] == "server":
        run_server()
    elif sys.argv[1] == "producer":
        run_producer()
    elif sys.argv[1] == "discovery":
        run_discovery()
    elif sys.argv[1] == "ping":
        ping_discovery()
