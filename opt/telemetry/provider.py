from threading import Thread, Event
from colorama import Style, Fore
from mqtt import MqttSensor
from gpsd import GpsdSensor

SENSORS_LUT = {
    'accel': ['#'],
    'gps': ['TPV/lat', 'TPV/lon', 'TPV/mode', 'TPV/speed', 'TPV/track'],
    'wind': ['#']
}


class SensorProvider(Thread):
    """
    Class for the gathering of data coming through sensors. Each sensor can be accessed by classical python array
    access with square brackets. Sensor data can be accessed with paths that has the sensor name as the first key. \n
    Example: sensor_provider['sensor_name/path/to/variable']
    """

    def __init__(self):
        """ Initialize the sensor provider. """
        Thread.__init__(self, name='sensor_provider', daemon=True)
        self.__sensors = None
        self.end_setup = Event()

    def __getitem__(self, path: str):
        """
        Access sensor data by the given path.
        :param path: The path as a slash separated keys string.
        :return: The item correspondent to the path.
        """
        path = path.strip('/')
        if not path: return {name: sensor['/'] for name, sensor in self.__sensors.items()}
        if not path.split('/')[1:]: return self.__sensors[path.split('/')[0]]['/']
        return self.__sensors[path.split('/')[0]][path[path.find('/'):]]

    def __iter__(self):
        """
        Return an iterator through each sensor of the provider.
        :return: The iterator object.
        """
        return self.__sensors.items().__iter__()

    def run(self):
        """ Main routine of the thread. Initialize and start sensors. """
        self.__sensors = {
            'accel': MqttSensor('accel', [f'sensor/accel/{topic}' for topic in SENSORS_LUT['accel']]),
            'gps': GpsdSensor('gps', SENSORS_LUT['gps']),
            'wind': MqttSensor('wind', [f'sensor/wind/{topic}' for topic in SENSORS_LUT['wind']])
        }
        for sensor in self.__sensors.values(): sensor.start()
        for sensor in self.__sensors.values(): sensor.end_setup.wait(timeout=20)

        if False in [sensor.end_setup.isSet() for sensor in self.__sensors.values()]:
            print(f"{Fore.RED}[{self.getName()}] Sensors initialization failed, quitting...")
            return
        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        while True: pass
