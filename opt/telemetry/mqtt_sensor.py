from threading import Thread, Event
from colorama import Style, Fore
import paho.mqtt.client as client


class MqttSensor(Thread):

    def __init__(self, sensor_name, topic_list=()):
        Thread.__init__(self, name=sensor_name + "_thread", daemon=True)
        self.topic_list = topic_list

        self.data = {}

        self.client = client.Client(sensor_name)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.end_setup = Event()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected")
        for topic in self.topic_list:
            self.client.subscribe(topic)
            print("Sub to : " + topic)

    def on_message(self, client, userdata, msg):
        self.data[msg.topic] = msg.payload.decode()
        print('Got message from ' + msg.topic + ' : ' + msg.payload.decode())

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected")

    def run(self):
        self.client.connect("localhost")
        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        while True:
            self.client.loop()
            if not self.client.is_connected():
                break

    def get_log_line(self):
        return ",".join(self.data.values())

    def get_log_header(self):
        return ",".join(self.data.keys())


if __name__ == "__main__":
    test_sensor = MqttSensor("test_sensor", ["test_topic"])
    test_sensor.start()
    print(test_sensor.get_log_header())
    while True:
        print(test_sensor.get_log_line())
