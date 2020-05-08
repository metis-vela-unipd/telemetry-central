from threading import Thread, Event
from time import sleep
from colorama import Style
import serial
from gpiozero import DigitalInputDevice
from provider import SensorProvider


class LoraTransceiver(Thread):

    def __init__(self, provider: SensorProvider):
        Thread.__init__(self, name='lora_transceiver', daemon=True)
        self.__serial = None
        self.__provider = provider
        self.end_setup = Event()

    def run(self):
        self.__serial = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        while True:
            self.__serial.write(self.__provider['gps/TPV/speed'])
            sleep(5)
