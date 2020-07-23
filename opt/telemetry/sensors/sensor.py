from threading import Thread, Event, Timer

import dpath.util as dp
import pandas as pd


class Sensor(Thread):
    """ Class for the definition of generic sensor objects. \n
    Each sensor has:
     - A protected tree structure with auto-resettable variables as leaves to store live data coming from sensors;
     - A protected list of topics to which the sensor is watching;
     - An 'end setup' Event to set when the setup is finished.
    Classic python array access with square brackets can be used to access sensor data. Variables can be addressed
    with the correspondent topic path. \n
    Example: sensor['path/to/variable']
    """

    def __init__(self, name, filters):
        """ Create a new sensor object with the given name and watching topics. \n
        :param name: The sensor displayable name.
        :param filters: A list of topics to watch. The wildcard '*' can be used to gather all available data in the
                       specified subtree.
        """
        super().__init__(name=name, daemon=True)
        self.name = name
        self.timers = {}
        self.timeout_sec = 3
        self.data = {}
        self.filters = filters
        self.end_setup = Event()
        wild_paths = [path[:-1].rstrip('/') for path in self.filters if path[-1] is '*']
        wild_paths.sort(key=len)
        for wild_path in wild_paths:
            if wild_path: dp.new(self.data, wild_path, {})
        for path in [filter for filter in self.filters if filter[-1] is not '*']: dp.new(self.data, path, None)

    def __getitem__(self, path):
        """ Return the item value correspondent to the given path. \n
        :param path: The path as a string composed by slash separated keys.
        :return: The current value of the variable or None, if the value is outdated.
        """
        return dp.get(self.data, path)

    def set(self, path, value):
        """ Set the value at the variable correspondent to the given path. This action will restart the reset timer. \n
        :param path: The path as a string composed by slash separated keys.
        :param value: The value to set to the variable.
        """
        dp.new(self.data, path, value)
        if value is not None:
            if path in self.timers and self.timers[path]: self.timers[path].cancel()
            self.timers[path] = Timer(self.timeout_sec, dp.set, [self.data, path, None])
            self.timers[path].start()

    def __contains__(self, path):
        """ Tell if the data tree contains the variable located in the path. \n
        :param path: The variable path as slash separated keys.
        :return: True if the tree contains the variable, false otherwise.
        """
        return bool(dp.search(self.data, path))

    def keys(self):
        """ Return the keys of the dictionary tree. \n
        :return: A list of the sensor data variable keys.
        """
        return list(pd.json_normalize(self.data, sep='/').keys())

    def items(self):
        """ Return the items of the dictionary tree. \n
        :return: An ItemsView object of the sensor data variable.
        """
        return [(key, self[key]) for key in self]

    def __iter__(self):
        """ Return an iterator for the sensor. \n
        :return: An Iterator object of the sensor data variable.
        """
        return self.keys().__iter__()

    def __len__(self):
        """ Return the length of the sensor data. \n
        :return: An integer representing the length of the sensor data variable.
        """
        return len(self.keys())

    def __str__(self):
        """ Define the string representation of the sensor. \n
        :return: A string representing the data variable of the sensor.
        """
        return f'<{__name__}: {str(self.data)}>'
    __repr__ = __str__

    def run(self):
        """ Method that needs to be implemented from subclasses. """
        raise NotImplementedError

    def stop(self): pass
