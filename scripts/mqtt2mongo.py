from datetime import datetime

from paho.mqtt.client import Client
from pymongo import MongoClient
from time import sleep


def on_message(client, userdata, message):
    if message.topic == 'control/log/tag':
        global tag
        tag = message.payload.decode()
        return
    if message.topic == 'control/log/rate':
        global rate
        rate = float(message.payload.decode())
        return
    data[message.topic] = message.payload


mongo = MongoClient()
mqtt = Client('mongodb')
mqtt.on_message = on_message
mqtt.connect('localhost')
mqtt.subscribe('#')
db = mongo['telemetry']
data = {}
tag = ''
rate = 2
mqtt.loop_start()
while True:
    now = datetime.now()
    data['timestamp'] = int(now.timestamp())
    data['datetime'] = now.strftime('%d-%m-%Y %H:%M:%S')
    mongo.telemetry.data.insert_one(data)
    data = {}
    sleep(1/rate)
