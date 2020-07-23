import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from threading import Thread
from time import sleep

import pandas as pd


class SensorLogger(Thread):

    def __init__(self, provider, name, log_rate, filters):
        super().__init__(name=name, daemon=True)
        self.provider = provider
        self.logging = False
        self.log_rate = log_rate
        self.root_path = f'{Path.home()}/telemetry-logs/{name}'
        self.file_name = datetime.now().strftime('%d-%b-%Y_%H:%M:%S')
        self.json_file = None
        os.makedirs(f'{self.root_path}/gpx', exist_ok=True)
        os.makedirs(f'{self.root_path}/json', exist_ok=True)
        os.makedirs(f'{self.root_path}/csv', exist_ok=True)
        subprocess.run(['pkill', '-SIGINT', '-f', 'gpxlogger'])
        process = subprocess.Popen(['gpxlogger', '-d', '-f', f'{self.root_path}/gpx/{self.file_name}.gpx'])
        process.wait(timeout=5)
        self.json_file = open(f'{self.root_path}/json/{self.file_name}.json', mode='w', buffering=1)
        self.json_file.write('[\n')
        sleep(self.log_rate)
        self.write_record()
        self.start()

    def write_record(self):
        record = {
            'timestamp': datetime.timestamp(datetime.now()),
            'logging': self.logging
        }
        record = {**record, **self.provider['/']}
        self.json_file.write(json.dumps(record, indent=2))

    def json_to_csv(self):
        with open(f'{self.root_path}/json/{self.file_name}.json') as json_file:
            pd.json_normalize(json.load(json_file), sep='/').to_csv(f'{self.root_path}/csv/{self.file_name}.csv')

    def run(self):
        while True:
            sleep(5)
            self.json_file.write(',\n')
            self.write_record()

    def stop(self):
        self.json_file.write('\n]\n')
        self.json_file.close()
        self.json_to_csv()
        subprocess.run(['pkill', '-SIGINT', '-f', 'gpxlogger'])
