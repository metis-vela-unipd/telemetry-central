from gpiozero import DigitalInputDevice
from paho.mqtt.client import Client
from serial import Serial, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
from serial.threaded import ReaderThread, LineReader


class Lora(LineReader):
    def handle_line(self, line):
        pass


def on_message(client, userdata, message):
    lora.write_line(f'{message.topic} {message.payload.decode()}')
    print(f"Transmit! Topic: {message.topic}; Payload: {message.payload.decode()}")


serial = Serial(
    port='/dev/ttyAMA1',
    baudrate=9600,
    parity=PARITY_NONE,
    stopbits=STOPBITS_ONE,
    bytesize=EIGHTBITS,
    timeout=1
)
aux = DigitalInputDevice(25)
m0 = DigitalInputDevice(10)
m1 = DigitalInputDevice(11)
lora = ReaderThread(serial, Lora).__enter__()
mqtt = Client('lora')
mqtt.on_message = on_message
mqtt.connect('localhost')
mqtt.subscribe('sensor/gps0/lat')
mqtt.subscribe('sensor/gps0/lon')
mqtt.loop_forever()
