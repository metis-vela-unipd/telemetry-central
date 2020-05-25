import json

from colorama import Style, Fore

from sensors import MqttSensor, GpsdSensor
from providers import Provider


class SensorProvider(Provider):
    """ Class for the gathering of data coming through sensors. Each sensor can be accessed by classical python array
    access with square brackets. Sensor data can be accessed with paths that has the sensor name as the first key. \n
    Example: sensor_provider['sensor_name/path/to/variable']
    """

    def __init__(self, name=None):
        """ Initialize the sensor provider. """
        super().__init__(name)
        self.start()

    @staticmethod
    def init_sensor(protocol, name=None, topics='*'):
        """ Initialize the sensor that handles communications for the given protocol. \n
        :param protocol: The protocol name. Supported protocols are 'mqtt' and 'gpsd'.
        :param name: The display name of the sensor.
        :param topics: The topics list.
        :return: An instance of the newly created sensor.
        """
        if protocol == 'gpsd': return GpsdSensor(name, [topic for topic in topics])
        elif protocol == 'mqtt': return MqttSensor(name, [f'sensor/{name}/{topic}' for topic in topics])

    def run(self):
        """ Main routine of the thread. Initialize and start sensors. """
        with open('sources.json') as sources_file:
            sensors = json.load(sources_file)['sensor_provider']
        for sensor in sensors:
            self.sources[sensor['name']] = SensorProvider.init_sensor(sensor['protocol'], sensor['name'], sensor['topics'])

        for sensor in self.sources.values(): sensor.end_setup.wait(timeout=20)

        if False in [sensor.end_setup.isSet() for sensor in self.sources.values()]:
            print(f"{Fore.RED}[{self.getName()}] Sensors initialization failed, quitting...")
            return
        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()
