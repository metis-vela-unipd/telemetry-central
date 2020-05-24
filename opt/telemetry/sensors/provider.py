from threading import Event, Thread

import dpath.util as dp
from colorama import Fore, Style

from .gpsd import GpsdSensor
from .mqtt import MqttSensor

SENSORS_LUT = {
    'accel': ['*'],
    'gps': ['TPV/lat', 'TPV/lon', 'TPV/mode', 'TPV/speed', 'TPV/track'],
    'wind': ['*']
}


class SensorProvider(Thread):
    """ Class for the gathering of data coming through sensors. Each sensor can be accessed by classical python array
    access with square brackets. Sensor data can be accessed with paths that has the sensor name as the first key. \n
    Example: sensor_provider['sensor_name/path/to/variable']
    """

    def __init__(self):
        """ Initialize the sensor provider. """
        super().__init__(name='sensor_provider', daemon=True)
        self.sensors = None
        self.end_setup = Event()

    def __getitem__(self, path):
        """ Access sensor data by the given path. \n
        :param path: The path as a slash separated keys string.
        :return: The item correspondent to the path.
        """
        return dp.get(self.sensors, path)

    def run(self):
        """ Main routine of the thread. Initialize and start sensors. """
        self.sensors = {
            'accel': MqttSensor('accel', [f'sensor/accel/{topic}' for topic in SENSORS_LUT['accel']]),
            'gps': GpsdSensor('gps', SENSORS_LUT['gps']),
            'wind': MqttSensor('wind', [f'sensor/wind/{topic}' for topic in SENSORS_LUT['wind']])
        }
        for sensor in self.sensors.values(): sensor.start()
        for sensor in self.sensors.values(): sensor.end_setup.wait(timeout=20)

        if False in [sensor.end_setup.isSet() for sensor in self.sensors.values()]:
            print(f"{Fore.RED}[{self.getName()}] Sensors initialization failed, quitting...")
            return
        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()
