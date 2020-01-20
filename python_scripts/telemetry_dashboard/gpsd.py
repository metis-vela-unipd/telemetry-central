from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE, MPS_TO_KNOTS
from threading import Thread

class Gpsd(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        self.speed = 0
        self.heading = 0

    def run(self):
        while True:
            try:
                report = self.session.next()
                print(report)
                if report['class'] == 'TPV': 
                    if hasattr(report, 'speed'): self.speed = round(report.speed * MPS_TO_KNOTS)
                    if hasattr(report, 'track'): self.heading = round(report.track)
            except KeyError:
                pass
            except StopIteration:
                print("GPSD has terminated, quitting...")
                break
