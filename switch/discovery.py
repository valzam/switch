from . import Server, logging
import zmq
import json
from multiprocessing import Process

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Discovery(Process):
    """ Implements a simple HTTP interface with information about the running server
    """
    def __init__(self, port: int, context: zmq.Context, daemon=False):
        super().__init__(daemon=daemon)

        self.running_servers = {}
        self.context = context
        self.port = port
        self.endpoint = None

    def register_server(self, server: Server):
        self.running_servers[str(server.predictor)] = {
            "incoming_port": server.incoming_port,
            "outgoing_port": server.outgoing_port,
            "incoming_topic": server.incoming_topic,
            "outgoing_topic": server.outgoing_topic
        }

    def run(self, ):
        self.endpoint = self._build_endpoint(self.context)
        logger.info(f"Starting discovery process on port {self.port}")
        while True:
            identity, request = self.endpoint.recv_multipart()
            logger.info(f"Received discovery request: {request}")

            JSON_RESPONSE = '\r\n'.join([
                "HTTP/1.0 200 OK",
                "Content-Type: application/json",
                "",
                f"{json.dumps(self.running_servers)}"
            ])
            self.endpoint.send_multipart([identity, bytes(JSON_RESPONSE, encoding="utf-8")])
            self.endpoint.send_multipart([identity, bytes('', encoding="utf-8")])

    def _build_endpoint(self, context: zmq.Context):
        socket=context.socket(zmq.ROUTER)  # pylint: disable=E1101
        socket.router_raw = True 
        socket.bind(f"tcp://*:{self.port}")

        return socket
