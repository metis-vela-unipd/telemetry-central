from threading import Thread, Event
from typing import List
from time import sleep
from colorama import Style
import serial
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from providers import SensorProvider

NULL_DATA = '-'
SEPARATOR = ' '
END_OF_PACKET = '\n'


class LoraTransceiver(Thread):
    """ Class that communicates via UART interface with an attached LoRa transceiver. """

    def __init__(self, provider: SensorProvider):
        """
        Initialize the object by giving the provider of sensor data.
        :param provider: The SensorProvider object.
        """
        Thread.__init__(self, name='lora_transceiver', daemon=True)
        self.__provider = provider
        self.__serial = None
        self.__aux = None
        self.__m0 = None
        self.__m1 = None
        self.end_setup = Event()

    def __send_packet(self, packet: List[str]) -> int:
        """
        Pack and send the given packet via LoRa modulation.
        :param packet: The packet to send as a list of strings.
        :return: The number of bytes sent.
        """
        packet_str = ''
        for record in packet: packet_str += record + SEPARATOR
        packet_str = packet_str[:-1]
        packet_str += END_OF_PACKET
        return self.__serial.write(packet_str.encode())

    def run(self):
        """ Main routine of the thread. Finish initialization, gather and send sensor data. """
        self.__serial = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.__aux = DigitalInputDevice(17)
        self.__m0 = DigitalOutputDevice(22)
        self.__m1 = DigitalOutputDevice(27)

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        while True:
            sleep(5)
            lat = self.__provider['gps/TPV/lat']
            lon = self.__provider['gps/TPV/lon']
            speed = self.__provider['gps/TPV/speed']
            track = self.__provider['gps/TPV/track']
            packet = [
                str(lat) if lat else NULL_DATA,
                str(lon) if lon else NULL_DATA,
                str(round(speed, 1)) if speed else NULL_DATA,
                str(round(track)) if track else NULL_DATA
            ]
            self.__send_packet(packet)
