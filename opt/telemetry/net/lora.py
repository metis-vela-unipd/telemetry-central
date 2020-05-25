from threading import Thread, Event
from time import sleep

import serial
from colorama import Style
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from serial.threaded import LineReader, ReaderThread

NULL_DATA = '-'

# TODO: Add synchronization mechanism
# TODO: Mode change and AUX waiting


class LoraTransceiver(Thread):
    """ Communicate via UART interface with an attached LoRa transceiver. """

    def __init__(self, provider, name=None):
        """ Initialize the object by giving the provider of sensor data. \n
        :param provider: The SensorProvider object.
        """
        super().__init__(name=name, daemon=True)
        self.provider = provider
        self.serial = None
        self.aux = None
        self.m0 = None
        self.m1 = None
        self.tx_rate = 5
        self.protocol = None
        self.end_setup = Event()
        self.start()

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
            lat = self.provider['gps']['TPV/lat']
            lon = self.provider['gps']['TPV/lon']
            speed = self.provider['gps']['TPV/speed']
            track = self.provider['gps']['TPV/track']
            line = LoraMessage() \
                .append(str(lat) if lat is not None else NULL_DATA) \
                .append(str(lon) if lon is not None else NULL_DATA) \
                .append(str(round(speed, 1)) if speed is not None else NULL_DATA) \
                .append(str(round(track)) if track is not None else NULL_DATA)
            self.protocol.write_line(line.build())


class LoraProtocol(LineReader):
    def __init__(self, ack_rate=5):
        super().__init__()
        self.sent = 0
        self.untracked = 0
        self.delivered = 0
        self.lost = 0
        self.ack_rate = ack_rate

    def write_line(self, text):
        super().write_line(text)
        self.sent += 1
        if self.untracked >= self.ack_rate: self.lost += 1
        else: self.untracked += 1

    def handle_line(self, line):
        line = LoraMessage.parse(line)
        if line[0] == 'ACK':
            if self.ack_rate > self.untracked:
                self.delivered += self.untracked
                self.untracked = 0
            else:
                self.delivered += self.ack_rate
                self.untracked -= self.ack_rate

    def connection_lost(self, exc):
        pass

    def __str__(self):
        return f"Sent packets: {self.sent}\n" \
               f"Unacknowledged packets: {self.untracked}\n" \
               f"Acknowledged packets: {self.delivered}\n" \
               f"Lost packets: {self.lost}\n"
    __repr__ = __str__


class LoraMessage:
    def __init__(self, header='', separator=' '):
        self.message = header
        self.separator = separator

    def append(self, field):
        if self.message: self.message += self.separator
        self.message += field
        return self

    def build(self, footer=''):
        return self.message + footer

    @staticmethod
    def parse(message, separator=' '):
        return message.split(separator)
