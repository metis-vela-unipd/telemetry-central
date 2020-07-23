from sensors import get_sensor
from .provider import Provider


class SensorProvider(Provider):
    """ Class for the gathering of data coming through sensors. Each sensor can be accessed by classical python array
    access with square brackets. Sensor data can be accessed with paths that has the sensor name as the first key. \n
    Example: sensor_provider['sensor_name/path/to/variable']
    """

    def __init__(self, sources, name):
        """ Initialize the sensor provider. """
        sensors = {}
        for sensor in sources:
            sensors[sensor['name']] = get_sensor(sensor['protocol'], sensor['name'], sensor['filters'])
        super().__init__(sensors, name)
