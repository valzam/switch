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
    server = switch.Server(server_config, context=context)
    discovery = switch.Discovery(os.environ.get("DISCOVERY_PORT"), context=context)
    discovery.register_server(server)

    server.start()
    discovery.start()

def ping_discovery():
    rep = requests.get(f"http://localhost:{os.environ.get('DISCOVERY_PORT')}")
    print(rep.json())


if __name__ == "__main__":
    run_server()

