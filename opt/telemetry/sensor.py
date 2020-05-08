from threading import Thread, Event
from typing import List
from utils import DataTree


class Sensor(Thread):
    """
    Class for the definition of generic sensor objects. \n
    Each sensor has:
     - A protected DataTree structure with TimeoutVar as leaves to store live data coming from sensors;
     - A protected list of topics to which the sensor is watching;
     - An 'end setup' Event to set when the setup is finished.
    Classic python array access with square brackets can be used to access sensor data. Variables can be addressed
    with the correspondent topic path. \n
    Example: sensor['path/to/variable']
    """

    def __init__(self, name: str, topics: List[str] = '#'):
        """
        Create a new sensor object with the given name and watching topics.
        :param name: The sensor displayable name.
        :param topics: A list of topics to watch.
        """
        Thread.__init__(self, name=name + '_sensor', daemon=True)
        self._topics = [topic.strip('/').split('/') for topic in topics if topic]
        self._data = DataTree(self._topics)
        self.end_setup = Event()

    def __getitem__(self, path: str):
        """
        Return the item value correspondent to the given path.
        :param path: The path as a string composed by slash separated keys.
        :return: The current value of the TimeoutVar or None, if the value is outdated.
        """
        path = path.strip('/')
        if not path: return self._data
        return self._data[path.split('/')]

    def __contains__(self, path: str):
        """
        Tell if variable is contained in the DataTree.
        :param path: The variable path as slash separated keys.
        :return: True if the variable is contained in the DataTree, false otherwise.
        """
        return path.strip('/').split('/') in self._data

    def __iter__(self):
        """
        Iterate through the DataTree with tuples (path, value).
        :return: The iterator object
        """
        return self._data.__iter__()
