import re

import paho.mqtt.client as client

from .sensor import Sensor


class MqttSensor(Sensor):
    """ Class for the communication and collections of data coming from the Mosquitto MQTT broker. """

    def __init__(self, name, filters):
        """ Create a new sensor based on the MQTT protocol. The client automatically subscribes to the
        topics passed as argument. \n
        :param name: The sensor displayable name.
        :param filters: A list of topics to subscribe to. Each topic follows the MQTT topic name convention.
        """
        super().__init__(name, filters)
        self.client = client.Client(name)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect('localhost')
        self.start()

    def on_connect(self):
        """ Subscribe to all the requested topics. """
        for topic in self.filters: self.client.subscribe(f'sensor/{self.getName()}/{topic.replace("*", "#")}')

    def on_message(self, msg):
        """ Write received data in the correspondent DataTree location. """
        topic = re.sub('^sensor/.*/', '', msg.topic)
        self.set(topic, msg.payload.decode())

    def run(self):
        """ Main routine of the thread. Finish initialization and enter the listening loop. """
        self.client.loop_forever(retry_first_connection=True)
