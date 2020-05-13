from typing import List
from time import sleep
from colorama import Style, Fore
from gps import gps, client, WATCH_ENABLE, WATCH_NEWSTYLE, MPS_TO_KNOTS
from sensors import Sensor


class GpsdSensor(Sensor):
    """ Class for the communication and collections of gps data coming from the gpsd daemon. """

    def __init__(self, name: str, topics: List[str]):
        """
        Create a new sensor based on the GPSd protocol. Response sentences are filtered by the topic list passed as
        argument, each topic follows this pattern: "<object>/../<attribute>".
        Available object and attribute names can be found here: https://gpsd.gitlab.io/gpsd/gpsd_json.html.
        The wildcard '#' can be used to indicate the gathering of all available data in the sub-path.
        :param name: The sensor displayable name.
        :param topics: A list of topics to watch in response sentences.
        """
        Sensor.__init__(self, name, topics)
        self.__session = None

    def __copy_report(self, report: client.dictwrapper, path: List[any]):
        """
        Copy the given gpsd report into the data variable of the sensor in the given path.
        :param report: The report as a gps library client dictwrapper.
        :param path: The destination path of the data tree.
        """
        for attr in report:
            if attr == 'class':
                path += [report['class']]
                continue
            if isinstance(report[attr], client.dictwrapper): self.__copy_report(report[attr], path + [attr])
            else: self._data[path + [attr]] = report[attr]

    def __report_get(self, report: client.dictwrapper, path: List[str]):
        """
        Get the value of the given gpsd report at the given path. Raise a KeyError if the given path is invalid.
        :param report: The report as a gps library client dictwrapper.
        :param path: The path to search in the report.
        :return: The value of the report at the given path.
        """
        if not path: return report
        if not isinstance(report[path[0]], client.dictwrapper):
            if path[1:]: raise KeyError(path[1:])
            return report[path[0]]
        return self.__report_get(report[path[0]], path[1:])

    def __start_daemon(self, tries: int):
        """
        Try to start the GPSD service for the given number of tries by querying it.
        :param tries: The numer of tries after giving up.
        :return: True if the daemon has been started successfully, false otherwise.
        """
        for i in range(tries):
            # TODO: Implement a standard print function
            print(f"{Fore.RED}[{self.getName()}] GPSD is not running, trying staring the service... [{i+1}]{Fore.RESET}")
            try:
                self.__session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
                print(f"{Fore.GREEN}[{self.getName()}]GPSD daemon started successfully!{Fore.RESET}")
                return True
            except ConnectionRefusedError: sleep(5)
        return False

    def run(self):
        """ Main routine of the thread. Get and filter gpsd reports. """
        try: self.__session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        except ConnectionRefusedError:
            if not self.__start_daemon(3): return

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        while True:
            if 'TPV/speed' in self and self['TPV/speed']: self._data['TPV', 'speed'] *= MPS_TO_KNOTS
            try:
                report = self.__session.next()
                for path in [topic[:-1] for topic in self._topics if topic[-1] == '#']:
                    self.__copy_report(report, path)
                for path in [topic for topic in self._topics if '#' not in topic]:
                    if report['class'] == path[0]: self._data[path] = self.__report_get(report, path[1:])
            except KeyError: pass
            except StopIteration:
                if not self.__start_daemon(5): return
