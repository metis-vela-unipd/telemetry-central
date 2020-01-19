from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
from threading import Thread

class Gpsd(Thread):

    def __init__(self):
        # Listen on port 2947 (gpsd) of localhost
        self.session = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

    def run(self):
        while True:
            try:
                report = self.session.next()
                # Wait for a 'TPV' report and display the current time
                # To see all report data, uncomment the line below
                # print(report)
                if report['class'] == 'TPV':
                    if hasattr(report, 'time'):
                        print(report.time)
            except KeyError:
                pass
            except KeyboardInterrupt:
                quit()
            except StopIteration:
                self.session = None
                print("GPSD has terminated")
