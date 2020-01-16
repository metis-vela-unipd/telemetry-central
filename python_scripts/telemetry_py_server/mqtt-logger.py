import csv
import paho.mqtt.subscribe as sub

file = open('testFile.txt', 'w', newline='')
csv_writer = csv.writer(file)

def print_msg(client, userdata, message):
    # print("%s : %s" % (message.topic, str(message.payload, encoding='utf-8')))
    csv_writer.writerow(str(message.payload, encoding='utf-8').split(','))
    file.flush()

try:
    sub.callback(print_msg, "WindInfo", hostname="localhost")
except KeyboardInterrupt:
    file.close()