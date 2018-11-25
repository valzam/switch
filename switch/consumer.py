import zmq
import random
import time
import json
from switch import pb


def main(port="5556", topic="Data_1A"):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)  # pylint: disable=E1101
    socket.connect(f"tcp://localhost:{port}")
    socket.setsockopt_string(
        zmq.SUBSCRIBE, "predictions")  # pylint: disable=E1101

    while True:# pylint: disable=E0632
        (topic, payload) = socket.recv_multipart()  # pylint: disable=E0632
        message = pb.Prediction()
        message.ParseFromString(payload)

        print(f"Received: {message}")


if __name__ == "__main__":
    import os
    main(os.environ.get("OUTGOING_PORT"),
         os.environ.get("OUTGOING_TOPIC"))
