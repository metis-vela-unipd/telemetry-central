from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE, MPS_TO_KNOTS
from threading import Thread, Timer, Event
from colorama import Style, Fore
from utils import TimeoutVar

class Gpsd(Thread):
    """ Thread for the communication and collections of gps data coming from the gpsd daemon. """

    def __init__(self):
        """ Initialize timeout variables and gpsd session. """
        Thread.__init__(self, name="gpsd_thread", daemon=True)
        self.session = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        self.fix = TimeoutVar(False, 5)
        self.speed = TimeoutVar(-1, 3)
        self.heading = TimeoutVar(-1, 3)
        self.end_setup = Event()

    def run(self):
        """ Continuously get gpsd sentences and update variables accordingly. """
        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()
        while True:
            try:
                report = self.session.next()
                if report['class'] == 'TPV':
                    self.fix.setValue(not(report.mode==1))
                    if hasattr(report, 'speed'): self.speed.setValue(round(report.speed * MPS_TO_KNOTS, 1))
                    if hasattr(report, 'track'): self.heading.setValue(round(report.track))
            except KeyError:
                pass
            except StopIteration:
                print(f"{Fore.RED}[{self.getName()}] GPSD has terminated, quitting...{Fore.RESET}")
                break
