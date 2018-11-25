from .pb import machine_failure
from . import logging, get_timestamp
import datetime
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MachineFailurePredictor:
    def __init__(self, *args, **kwargs):
        self.a = 0.5
        self.b = 0.5
        self.c = 1

    def predict(self, datapoint_binary):
        datapoint = machine_failure.MachineDataPoint()
        datapoint.ParseFromString(datapoint_binary)
        y = self._predict(datapoint)
        response = self._build_response(y)

        logger.info(
            f"Calculated prediction based on data from {datapoint.sender}: {y}")  # pylint: disable=E1101
        return response

    def _predict(self, datapoint: machine_failure.MachineDataPoint):
        """ Actual algorithm to facilitate easier testing
        """
        y = self.a * datapoint.temperature + self.b * datapoint.velocity + self.b  # pylint: disable=E1101

        return y

    def _build_response(self, y: float):
        response = machine_failure.MachineFailurePrediction()
        response.failureChance = y
        response.timestamp = get_timestamp()

        return response

    def __str__(self):
        return f"MachineFailure"
