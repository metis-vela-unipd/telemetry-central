from .provider import *
from .sensor_provider import *


def get_provider(source_type, sources, name=None):
    if source_type == 'sensors': return SensorProvider(sources, name)
