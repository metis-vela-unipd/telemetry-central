from threading import Thread, Event
from colorama import Style, Fore
from utils import TimeoutVar

from mqttSensor import MqttSensor

class SensorProvider(Thread):
    
    def __init__ (self):
        Thread.__init__(self, name="sensor_provider_thread", daemon=True)
        self.end_setup = Event()
        self.sensors = [
            MqttSensor('accelSensor', [
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
    provider = SensorProvider()
    provider.start()

    while True:
        pass