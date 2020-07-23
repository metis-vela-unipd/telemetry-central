from .gpsd_sensor import *
from .mqtt_sensor import *
from .sensor import *


def get_sensor(protocol, name=None, filters=None):
    """ Initialize the sensor that handles communications for the given protocol. \n
    :param protocol: The protocol name. Supported protocols are 'mqtt' and 'gpsd'.
    :param name: The display name of the sensor.
    :param filters: The topics list.
    :return: An instance of the newly created sensor.
    """
    filters = ['*'] if filters is None else [filter['path'] for filter in filters]
    if protocol == 'gpsd': return GpsdSensor(name, filters)
    elif protocol == 'mqtt': return MqttSensor(name, filters)
