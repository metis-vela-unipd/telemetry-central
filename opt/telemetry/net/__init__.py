from providers import Provider
from .lora import *
from .websocket import *


def get_gateway(source, name=None, tx_rate=5, filters=None):
    if isinstance(source, Provider): return LoraTransceiver(source, name, tx_rate, filters)
