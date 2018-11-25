import json
import configparser
import logging
from collections import namedtuple
import time
import datetime

logging.basicConfig(format='%(asctime)s %(name)s: %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')

ServerConfig = namedtuple("ServerConfig", ["predictor", 
                            "incoming_port", "outgoing_port",
                            "incoming_topic", "outgoing_topic"])

def get_config(config_file="config.ini", section="SERVER"):
    config = configparser.ConfigParser()
    config.read(config_file)

    return config[section]

def get_timestamp():
    return time.mktime(datetime.datetime.now().timetuple())

# INTERFACE
from .server import Server
from .predictor import MachineFailurePredictor as Predictor
from .discovery import Discovery
