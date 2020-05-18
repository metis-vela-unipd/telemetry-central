import re

import paho.mqtt.client as client
from colorama import Style

from sensors import Sensor


class MqttSensor(Sensor):
    """ Class for the communication and collections of data coming from the Mosquitto MQTT broker. """

    def __init__(self, name, topics='*'):
        """
        Create a new sensor based on the MQTT protocol. The client automatically subscribes to the topics passed as
        argument.
        :param name: The sensor displayable name.
        :param topics: A list of topics to subscribe to. Each topic follows the MQTT topic name convention.
        """
        super().__init__(name, [re.sub('^sensor/.*/', '', topic) for topic in topics])
        self.client = client.Client(name)

    def on_connect(self):
        """ Subscribe to all the requested topics. """
        for topic in self.topics: self.client.subscribe(topic.replace('*', '#'))

    def on_message(self, msg):
        """ Write received data in the correspondent DataTree location. """
        topic = msg.topic.replace('sensor/', '')[msg.topic.find('/'):]
        self[topic] = msg.payload.decode()

    def run(self):
        """ Main routine of the thread. Finish initialization and enter listening loop. """
        Sensor.run(self)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect('localhost')

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        self.client.loop_forever(retry_first_connection=True)
