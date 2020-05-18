from time import sleep

import dpath.util as dp
from colorama import Style, Fore
from gps import gps, client, WATCH_ENABLE, WATCH_NEWSTYLE, MPS_TO_KNOTS

from sensors import Sensor


class GpsdSensor(Sensor):
    """ Class for the communication and collections of gps data coming from the gpsd daemon. """

    def __init__(self, name, topics='*'):
        """
        Create a new sensor based on the GPSd protocol. Response sentences are filtered by the topic list passed as
        argument, each topic follows this pattern: "<object>/../<attribute>".
        Available objects and attributes names can be found here: https://gpsd.gitlab.io/gpsd/gpsd_json.html.
        The wildcard '*' can be used to gather all the available data in the sub-path.
        :param name: The sensor displayable name.
        :param topics: A list of topics to watch in response sentences.
        """
        super().__init__(name, topics)
        self.session = None

    @staticmethod
    def unwrap_report(report: client.dictwrapper) -> dict:
        """
        Unwrap the given report and export the class. Unwrapping means converting a dictionary wrapper to a dictionary.
        :param report: The report as a wrapped dictionary.
        :return: A dictionary tree with the report class as the root and the rest as a sub-tree.
        """
        def unwrap(wrapped_dict: client.dictwrapper):
            output = {}
            for attr in wrapped_dict:
                if not isinstance(wrapped_dict[attr], client.dictwrapper): output[attr] = wrapped_dict[attr]
                else: output[attr] = unwrap(wrapped_dict[attr])
            return output
        unwrapped_dict = unwrap(report)
        report_class = unwrapped_dict['class']
        del unwrapped_dict['class']
        return {report_class: unwrapped_dict}

    def copy_report(self, report: dict, path: str):
        """
        Copy the given gpsd report into the data variable of the sensor in the given path.
        :param report: The report as a gps library client dictwrapper.
        :param path: The destination path of the data tree. The path can contain wildcards.
        """
        for path, value in dp.search(report, path, yielded=True):
            if dp.search(report, f'{path}/*'): self.copy_report(report, f'{path}/*')
            else: self[path] = value

    def start_daemon(self, tries):
        """
        Try to start the gpsd service for the given number of tries by querying it.
        :param tries: The numer of tries after giving up.
        :return: True if the daemon has been started successfully, false otherwise.
        """
        for i in range(tries):
            # TODO: Implement a standard print function
            print(f"{Fore.RED}[{self.getName()}] GPSD is not running, trying staring the service... [{i+1}]{Fore.RESET}")
            try:
                self.session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
                print(f"{Fore.GREEN}[{self.getName()}]GPSD daemon started successfully!{Fore.RESET}")
                return True
            except ConnectionRefusedError: sleep(5)
        return False

    def run(self):
        """ Main routine of the thread. Get and filter gpsd reports. """
        super().run()
        try: self.session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        except ConnectionRefusedError:
            if not self.start_daemon(3): return

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        while True:
            if 'TPV/speed' in self and self['TPV/speed']: self['TPV/speed'] *= MPS_TO_KNOTS
            try:
                report = GpsdSensor.unwrap_report(self.session.next())
                for topic in self.topics: self.copy_report(report, topic)
            except KeyError: pass
            except StopIteration:
                if not self.start_daemon(5): return
