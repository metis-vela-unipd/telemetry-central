from threading import Thread, Event
from colorama import Fore, Style
import subprocess


class Logger(Thread):
    """ Simple class for logging of gps data. """

    def __init__(self, provider):
        """ Initialize thread and set the provider. """
        Thread.__init__(self, name="logger_thread", daemon=True)
        self.provider = provider
        self.is_logging = False
        self.end_setup = Event()

    def start_log(self):
        """ Start the logging process. By now it's just the gpxlogger process. """
        if self.is_logging:
            return False
        process = subprocess.Popen(['startlog'])
        process.wait(timeout=5)
        if process.returncode == 0:
            print(f"{Fore.CYAN}[{self.getName()}] Started logging process in '~/telemetry-logs/gpx/'{Fore.RESET}")
            self.is_logging = True
            return True
        return False

    def stop_log(self):
        """ Stop the logging process. """
        if not self.is_logging:
            return False
        process = subprocess.Popen(['pkill', '-SIGTERM', '-f', 'gpxlogger'])
        process.wait(timeout=5)
        if process.returncode == 0:
            self.is_logging = False
            print(f"{Fore.CYAN}[{self.getName()}] Stopped logging process{Fore.RESET}")
            return True
        return False

    def run(self):
        """ Finish setup and enter main loop. By now nothing is done in the main loop. """
        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        # Temporarily do nothing
        while True:
            pass
