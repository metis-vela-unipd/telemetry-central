from threading import Thread, Event
from colorama import Style, Fore
from utils import TimeoutVar

from mqtt_sensor import MqttSensor
from gps_sensor import GpsSensor

class SensorProvider(Thread):
    
    def __init__ (self):
        Thread.__init__(self, name="provider_thread", daemon=True)
        self.end_setup = Event()
        self.sensors = {
            'accelSensor' : MqttSensor('accelSensor', [
                'sensor/accel/#'
            ]),
            'gps': GpsSensor(),
            'windSensor' : MqttSensor('windSensor', [
                'sensor/wind/#'
            ])
        }

    def run(self):
        for sensor in self.sensors.values():
            sensor.start()
            sensor.end_setup.wait(timeout=20)

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        # while True:
            # if not sensor.is_alive():
                # print(f"{Fore.YELLOW}[main_thread] Provider dead, attempting recovery...{Fore.RESET}")
                # sensor = SensorProvider()
                # sensor.start()
                # sensor.end_setup.wait(timeout=20)
                # if provider.end_setup.isSet():
                    # print(f"{Fore.GREEN}[main_thread] Done recovery!{Fore.RESET}")

    def get_sensor(self, sensor_name):
        if sensor_name in self.sensors:
            return self.sensors[sensor_name]
        return None

if __name__ == "__main__":
    provider = SensorProvider()
    provider.start()

    while True:
        pass