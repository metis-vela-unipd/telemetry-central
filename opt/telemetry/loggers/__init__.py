from net import LoraTransceiver
from providers import SensorProvider
from .logger import *
from .lora_logger import *
from .sensor_logger import *


def get_logger(source, name=None, log_rate=5, filters=None):
    if isinstance(source, SensorProvider):
        return SensorLogger(source, name, log_rate, filters)
    if isinstance(source, LoraTransceiver):
        return LoraLogger(source, name, log_rate, filters)
