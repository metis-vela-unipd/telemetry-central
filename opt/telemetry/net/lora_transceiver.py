from threading import Thread, Event
from time import sleep

import serial
from serial.threaded import LineReader, ReaderThread
from colorama import Style
from gpiozero import DigitalInputDevice, DigitalOutputDevice

NULL_DATA = '-'


class LoraTransceiver(Thread):
    """ Class communicates via UART interface with an attached LoRa transceiver. """

    def __init__(self, provider):
        """
        Initialize the object by giving the provider of sensor data.
        :param provider: The SensorProvider object.
        """
        super().__init__(name='lora_transceiver', daemon=True)
        self.provider = provider
        self.serial = None
        self.aux = None
        self.m0 = None
        self.m1 = None
        self.tx_rate = 5
        self.protocol = None
        self.end_setup = Event()

    def run(self):
        """ Main routine of the thread. Finish initialization, gather and send sensor data. """
        self.serial = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.aux = DigitalInputDevice(17)
        self.m0 = DigitalOutputDevice(22)
        self.m1 = DigitalOutputDevice(27)
        self.protocol = ReaderThread(self.serial, LoraProtocol).__enter__()

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        while True:
            sleep(self.tx_rate)
            lat = self.provider['gps/TPV/lat']
            lon = self.provider['gps/TPV/lon']
            speed = self.provider['gps/TPV/speed']
            track = self.provider['gps/TPV/track']
            line = LineBuilder() \
                .append(str(lat) if lat is not None else NULL_DATA) \
                .append(str(lon) if lon is not None else NULL_DATA) \
                .append(str(round(speed, 1)) if speed is not None else NULL_DATA) \
                .append(str(round(track)) if track is not None else NULL_DATA)
            self.protocol.write_line(line.build())


class LoraProtocol(LineReader):
    def __init__(self):
        super().__init__()
        self.untracked_packets = 0
        self.ack_rate = 5

    def connection_made(self, transport):
        super().connection_made(transport)

    def write_line(self, text):
        super().write_line(text)
        self.untracked_packets += 1

    def handle_line(self, line):
        if line == 'ACK': self.untracked_packets -= self.ack_rate

    def connection_lost(self, exc):
        pass


class LineBuilder:
    def __init__(self, start='', separator=' '):
        self.line = start
        self.separator = separator

    def append(self, segment):
        if self.line: self.line += self.separator
        self.line += segment
        return self

    def build(self):
        return self.line
