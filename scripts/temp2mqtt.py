from time import sleep

from gpiozero import CPUTemperature
from paho.mqtt.client import Client

cpu = CPUTemperature()
mqtt = Client('temp')
mqtt.connect('localhost')

while True:
    mqtt.publish('system/temp', str(cpu.temperature))
    print(f"Publish! Topic: system/temp; Payload: {cpu.temperature}")
    sleep(30)
