from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE, MPS_TO_KNOTS
from threading import Thread, Timer, Event
from colorama import Style, Fore

class _TimeoutVar:
    """
    Class for the creation of variables with timeout.

    A timeout variable auto resets itself to a default value if it's not changed after the set timeout time.
    In this case the default value represent the unavailable state of the gps data.
    """

    def __init__(self, default, timeout_sec):
        """ Set options and initialize variable to it's default value. """
        self.actual = default
        self.default = default
        self.timeout_sec = timeout_sec
        self.timeout_timer = None

    def setValue(self, value):
        """ Set the value of the variable and reset the timeout timer. """
        self.actual = value
        if self.actual != self.default:
            if self.timeout_timer is not None: self.timeout_timer.cancel()
            self.timeout_timer = Timer(self.timeout_sec, self.setValue, [self.default])
            self.timeout_timer.start()
    
    def isDefault(self):
        """ Tell if the variable value is the default one. """
        return self.actual == self.default


class Gpsd(Thread):
    """ Thread for the communication and collections of gps data coming from the gpsd daemon. """

    def __init__(self):
        """ Initialize timeout variables and gpsd session. """
        Thread.__init__(self, name="gpsd_thread", daemon=True)
        self.session = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        self.fix = _TimeoutVar(False, 5)
        self.speed = _TimeoutVar(-1, 3)
        self.heading = _TimeoutVar(-1, 3)
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
