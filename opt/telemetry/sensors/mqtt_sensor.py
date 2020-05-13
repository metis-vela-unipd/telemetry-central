from typing import List
from colorama import Style
import paho.mqtt.client as client
from sensors import Sensor


class MqttSensor(Sensor):
    """ Class for the communication and collections of data coming from the Mosquitto MQTT broker. """

    def __init__(self, name: str, topics: List[str]):
        """
        Create a new sensor based on the MQTT protocol. The client automatically subscribes to the topics passed as
        argument.
        :param name: The sensor displayable name.
        :param topics: A list of topics to subscribe to. Each topic follows the MQTT topic name convention.
        """
        Sensor.__init__(self, name, [topic[topic.find('/'):][topic.find('/'):] for topic in topics])
        self.__client = client.Client(name)

    def __on_connect(self):
        """ Subscribe to all the requested topics. """
        for topic in self._topics: self.__client.subscribe(topic)

    def __on_message(self, msg):
        """ Write received data in the correspondent DataTree location. """
        topic = msg.topic[msg.topic.find('/'):][msg.topic.find('/'):]
        self._data[topic.strip('/').split('/')] = msg.payload.decode()

    def run(self):
        """ Main routine of the thread. Finish initialization and enter listening loop. """
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect('localhost')

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        self.__client.loop_forever(retry_first_connection=True)
