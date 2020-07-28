from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE, MPS_TO_KNOTS
from paho.mqtt.client import Client

session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
mqtt = Client('gps0')
mqtt.connect('localhost')

for report in session:
    report = dict(report)
    if report['class'] == 'TPV':
        del report['class']
        if 'time' in report:
            del report['time']
        if 'speed' in report:
            report['speed'] *= MPS_TO_KNOTS
        for key, val in report.items():
            topic = f'sensor/gps0/{key}'
            mqtt.publish(topic, str(val))
            print(f'Publish! Topic: {topic}; Value: {val}')
