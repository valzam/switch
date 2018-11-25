import zmq
import random
import time
import json
import os
from switch import get_timestamp
from switch.pb import machine_failure


def main(port="5556", topic="Data_1A"):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)  # pylint: disable=E1101
    socket.connect(f"tcp://{os.environ.get('SERVER_IP')}:{port}")
    datapoint = machine_failure.MachineDataPoint()

    datapoint.sender = "schmoi"
    datapoint.temperature = 1
    datapoint.velocity = 1
    datapoint.pressure = 1
    datapoint.timestamp = get_timestamp()

    while True:
        socket.send_multipart(
            [bytes(topic, encoding='utf-8'), datapoint.SerializeToString()])
        print(f"Sent message to topic {topic} on endpoint {os.environ.get('SERVER_IP')}:{port}")
        time.sleep(1)
