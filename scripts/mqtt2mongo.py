from datetime import datetime

from paho.mqtt.client import Client
from pymongo import MongoClient


class Store:
    def __init__(self):
        self.tag = ''

    def on_message(self, client, userdata, message):
        if message.topic == 'data/tag':
            self.tag = message.payload.decode()
        now = datetime.now()
        document = {
            'topic': message.topic,
            'payload': message.payload.decode(),
            'tag': self.tag,
            'qos': message.qos,
            'timestamp': int(now.timestamp()),
            'datetime': now.strftime('%d/%m/%Y %H:%M:%S')
        }
        data.insert_one(document)
        print(f"Store! Date: {now.strftime('%d/%m/%Y %H:%M:%S')}; Topic: {message.topic}; Payload: {message.payload.decode()}; Tag: '{self.tag}'")


mongo = MongoClient()
mqtt = Client('mongodb')
mqtt.on_message = Store().on_message
mqtt.connect('localhost')
mqtt.subscribe('#')
db = mongo['telemetry']
data = db['data']
mqtt.loop_forever()
