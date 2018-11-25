import zmq
import switch


def test_end2end():
    context = zmq.Context()
    predictor = switch.Predictor()
    server_config = switch.ServerConfig(predictor=predictor, zmq_context=context,
                                      incoming_port=5556, outgoing_port=5566,
                                      incoming_topic="Data_1A", outgoing_topic="Predictions_1A")
    server = switch.Server(server_config)

    assert(True)
    
