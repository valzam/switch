import zmq
import switch
import random
import time
import json
import os
from multiprocessing import Process

from switch.pb import machine_failure

class mock_Predictor:
    def predict(self, msg):
        response = machine_failure.MachineFailurePrediction()
        response.failureChance = 5
        response.timestamp = 123556

        return response

def start_consumer(port="5556", topic="Data_1A"):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)  # pylint: disable=E1101
    socket.connect(f"tcp://{os.environ.get('SERVER_IP')}:{port}")
    socket.setsockopt_string(
        zmq.SUBSCRIBE, topic)  # pylint: disable=E1101

    (topic, payload) = socket.recv_multipart()  # pylint: disable=E0632
    message = machine_failure.MachineFailurePrediction()
    message.ParseFromString(payload)

    return message


def start_producer(port="5556", topic="Data_1A"):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)  # pylint: disable=E1101
    socket.connect(f"tcp://{os.environ.get('SERVER_IP')}:{port}")
    datapoint = machine_failure.MachineDataPoint()

    datapoint.sender = "schmoi"
    datapoint.temperature = 1
    datapoint.velocity = 1
    datapoint.pressure = 1
    datapoint.timestamp = switch.get_timestamp()

    while True:
        socket.send_multipart(
            [bytes(topic, encoding='utf-8'), datapoint.SerializeToString()])
        print(f"Sent message to topic {topic} on endpoint {os.environ.get('SERVER_IP')}:{port}")
        time.sleep(1)


def test_end2end():
    context = zmq.Context()
    predictor = mock_Predictor()
    server_config = switch.ServerConfig(predictor=predictor,
                                        incoming_port=os.environ.get("INCOMING_PORT"),
                                        outgoing_port=os.environ.get("OUTGOING_PORT"),
                                        incoming_topic=os.environ.get("INCOMING_TOPIC"),
                                        outgoing_topic=os.environ.get("OUTGOING_TOPIC"))
    server = switch.Server(server_config, context=context, daemon=True)  # pylint: disable=E1123
    server.start()
    Process(target=start_producer, args=(os.environ.get("INCOMING_PORT"),
                                         os.environ.get("INCOMING_TOPIC")), daemon=True).start()

    result = start_consumer(os.environ.get("OUTGOING_PORT"), os.environ.get("OUTGOING_TOPIC"))

    assert(result.failureChance == 5.0)  # pylint: disable=E1101
