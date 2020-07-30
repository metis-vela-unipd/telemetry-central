from datetime import datetime

from paho.mqtt.client import Client
from pymongo import MongoClient


def on_message(client, userdata, message):
    now = datetime.now()
    document = {
        'topic': message.topic,
        'payload': message.payload.decode(),
        'qos': message.qos,
        'timestamp': int(now.timestamp()),
        'datetime': now.strftime('%d/%m/%Y %H:%M:%S')
    }
    data.insert_one(document)
    print(f"Store! Date: {now.strftime('%d/%m/%Y %H:%M:%S')}; Topic: {message.topic}; Payload: {message.payload.decode()}")


mongo = MongoClient()
mqtt = Client('mqtt2mongodb')
mqtt.on_message = on_message
mqtt.connect('localhost')
mqtt.subscribe('#')
db = mongo['telemetry']
data = db['data']
mqtt.loop_forever()
