import csv
import os
from datetime import datetime
from pathlib import Path
from threading import Thread
from time import sleep


class LoraLogger(Thread):

    def __init__(self, protocol, name, log_rate, filters):
        super().__init__(name=name, daemon=True)
        self.protocol = protocol
        self.logging = False
        self.log_rate = log_rate
        self.root_path = f'{Path.home()}/telemetry-logs/{name}'
        self.file_name = datetime.now().strftime('%d-%b-%Y_%H:%M:%S')
        self.csv_file = None
        os.makedirs(f'{self.root_path}/csv', exist_ok=True)
        self.csv_file = open(f'{self.root_path}/csv/{self.file_name}.csv', mode='w', buffering=1)
        self.csv_writer = csv.DictWriter(self.csv_file, self.protocol.statistics.keys())
        self.csv_writer.writeheader()
        self.start()

    def run(self):
        while True:
            sleep(self.log_rate)
            self.csv_writer.writerow(self.protocol.statistics)

    def stop(self): pass
