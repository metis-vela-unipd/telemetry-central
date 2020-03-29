#  Copyright (c) 2020 Matteo Carnelos.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE, MPS_TO_KNOTS
from threading import Thread, Event
from colorama import Style, Fore
from utils import TimeoutVar


class GpsdSensor(Thread):
    """ Thread for the communication and collections of gps data coming from the gpsd daemon. """

    def __init__(self):
        """ Initialize timeout variables and gpsd session. """
        Thread.__init__(self, name="gpsd_sensor_thread", daemon=True)
        self.session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        self.fix = TimeoutVar(False, 5)
        self.speed = TimeoutVar(-1, 3)
        self.heading = TimeoutVar(-1, 3)
        self.end_setup = Event()

    @property
    def speed_display(self):
        """ Get a displayable value for the speed variable. """
        return "-" if self.speed.is_default() or not self.has_fix else str(self.speed.actual)

    @property
    def heading_display(self):
        """ Get a displayable value for the heading variable. """
        return "-" if self.heading.is_default() or not self.has_fix else str(self.heading.actual)

    @property
    def has_fix(self):
        """ Tell if the gps has a FIX. """
        return not self.fix.is_default()

    def run(self):
        """ Continuously get gpsd sentences and update variables accordingly. """
        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()
        while True:
            try:
                report = self.session.next()
                if report['class'] == 'TPV':
                    self.fix.set_value(not report.mode == 1)
                    if hasattr(report, 'speed'):
                        self.speed.set_value(round(report.speed * MPS_TO_KNOTS, 1))
                    if hasattr(report, 'track'):
                        self.heading.set_value(round(report.track))
            except KeyError:
                pass
            except StopIteration:
                print(f"{Fore.RED}[{self.getName()}] GPSD has terminated, quitting...{Fore.RESET}")
                break
