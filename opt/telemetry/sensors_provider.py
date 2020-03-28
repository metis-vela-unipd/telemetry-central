from threading import Thread, Event
from colorama import Style, Fore
from utils import TimeoutVar

from mqtt_sensor import Mqtt

class Provider(Thread):
    
    def __init__ (self):
        Thread.__init__(self, name="provider_thread", daemon=True)
        self.end_setup = Event()
        self.sensors = [
            Mqtt('accelSensor', [
                'sensor/accel/#'
            ])
            # MqttSensor('test_sensor', [
            #     'test_topic'
            # ])
        ]

    def run(self):
        for sensor in self.sensors:
            sensor.start()
            sensor.end_setup.wait(timeout=20)

        while True:
            pass


if __name__ == "__main__":
    provider = Provider()
    provider.start()

    while True:
        pass