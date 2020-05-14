from threading import Thread, Event, Timer
from typing import List
import dpath.util as dp


class Sensor(Thread):
    """
    Class for the definition of generic sensor objects. \n
    Each sensor has:
     - A protected tree structure with auto-resettable variables as leaves to store live data coming from sensors;
     - A protected list of topics to which the sensor is watching;
     - An 'end setup' Event to set when the setup is finished.
    Classic python array access with square brackets can be used to access sensor data. Variables can be addressed
    with the correspondent topic path. \n
    Example: sensor['path/to/variable']
    """

    def __init__(self, name: str, topics: List[str] = '*'):
        """
        Create a new sensor object with the given name and watching topics.
        :param name: The sensor displayable name.
        :param topics: A list of topics to watch. The wildcard '*' can be used to gather all available data in the
                       specified subtree.
        """
        Thread.__init__(self, name=name, daemon=True)
        self.__timers = {}
        self.__data = {}
        self._topics = topics
        self.end_setup = Event()

    def get(self, path: str) -> any:
        """
        Return the item value correspondent to the given path.
        :param path: The path as a string composed by slash separated keys.
        :return: The current value of the variable or None, if the value is outdated.
        """
        return dp.get(self.__data, path)
    __getitem__ = get

    def __setitem__(self, path: str, value: any):
        """
        Set the value at the variable correspondent to the given path. This action will restart the reset timer.
        :param path: The path as a string composed by slash separated keys.
        :param value: The value to set to the variable.
        """
        dp.new(self.__data, path, value)
        if value is not None:
            if path in self.__timers and not self.__timers[path]: self.__timers[path].cancel()
            self.__timers[path] = Timer(3, dp.set, [self.__data, path, None])
            self.__timers[path].start()

    def __contains__(self, path: str) -> bool:
        """
        Tell if variable is contained in the data tree.
        :param path: The variable path as slash separated keys.
        :return: True if the variable is contained in the tree, false otherwise.
        """
        return bool(dp.search(self.__data, path))

    def keys(self):
        """
        Return the keys of the dictionary tree.
        :return: A KeysView object of the sensor data variable.
        """
        return self.__data.keys()

    def items(self):
        """
        Return the items of the dictionary tree.
        :return: An ItemsView object of the sensor data variable.
        """
        return self.__data.items()

    def __iter__(self):
        """
        Return an iterator for the sensor.
        :return: An Iterator object of the sensor data variable.
        """
        return self.__data.__iter__()

    def __len__(self):
        """
        Return the length of the sensor data.
        :return: An integer representing the length of the sensor data variable.
        """
        return len(self.__data)

    def __str__(self):
        """
        Define the string representation of the sensor.
        :return: A string representing the data variable of the sensor.
        """
        return f'<{__name__}: {str(self.__data)}>'
    __repr__ = __str__

    def run(self):
        """
        Main routine of the thread. Initialize the tree. This method must be called from the subclasses as the first
        statement of the run routine.
        """
        wild_paths = [topic[:-2] for topic in self._topics if topic[-1] is '*']
        wild_paths.sort(key=len)
        for wild_path in wild_paths:
            if wild_path: dp.new(self.__data, wild_path, {})
        for path in [topic for topic in self._topics if topic[-1] is not '*']: dp.new(self.__data, path, None)
