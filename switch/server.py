import zmq
import random
import sys
import configparser
from datetime import datetime

from . import pb, logging, ServerConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Server:
    """ This class instantiates a Publish-Subscribe based server that takes message, predicts based on the contents 
    of the message and then sends back an answer.
    """

    def __init__(self, config: ServerConfig):
        self.predictor = config.predictor
        self.incoming_port = config.incoming_port
        self.outgoing_port = config.outgoing_port
        self.incoming_topic = config.incoming_topic
        self.outgoing_topic = config.outgoing_topic

    def start(self, context: zmq.Context):
        """ Server stats to receive and handle incoming messages
        """
        # Create endpoints
        self._incoming_endpoint = self._build_incoming_endpoint(context)
        self._outgoing_endpoint = self._build_outgoing_endpoint(context)
        
        logger.info(f"""Started server, waiting for messages
                    Topics: {self.incoming_topic} --> {self.outgoing_topic}
                    Ports: {self.incoming_port} --> {self.outgoing_port}""")
        while True:
            payload = self._receive_message()
            prediction = self._handle_incoming_message(payload)
            self._publish_message(prediction)

    def _handle_incoming_message(self, payload):
        """ Forward the payload to the predictor. Predictor needs to know the correct protobuf class
        """
        response = self.predictor.predict(payload)

        return response

    def _receive_message(self):
        (topic, payload) = self._incoming_endpoint.recv_multipart(
        )  # pylint: disable=E0632

        logger.info(f"Received message on topic {str(topic.decode('ascii'))}")
        return payload

    def _publish_message(self, message):
        self._outgoing_endpoint.send_multipart(
            [bytes(self.outgoing_topic, encoding='utf-8'), message.SerializeToString()])

        logger.info(f"Sent out prediction to topic {self.outgoing_topic}")

    def _build_incoming_endpoint(self, context: zmq.Context):
        """ Subscribe endpoint to collect datapoints from producer 
        """
        incoming_socket = context.socket(zmq.SUB)  # pylint: disable=E1101
        incoming_socket.bind(f"tcp://*:{self.incoming_port}")
        incoming_socket.setsockopt_string(
            zmq.SUBSCRIBE, self.incoming_topic)  # pylint: disable=E1101
        return incoming_socket

    def _build_outgoing_endpoint(self, context: zmq.Context):
        """ Publish endpoint to send out predictions made by predictor
        """
        outgoing_socket = context.socket(zmq.PUB)  # pylint: disable=E1101
        outgoing_socket.bind(f"tcp://*:{self.outgoing_port}")

        return outgoing_socket
