from threading import Thread, Event, Timer
from typing import List


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
        self._data = _DataTree(self._topics)
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


class _DataTree:
    """
    Tree data structure to store sensor readings.
    Values can be accessed either by path (list of keys) or by subclass access (dot notation).
    Each leaf of the tree is a TimeoutVar with timeout of 3 seconds.
    """

    def __init__(self, paths: List[List[any]] = '#'):
        """
        Initialize TimeoutVar objects of the given known paths.
        Subtrees correspondent to paths with the wildcard '#' are left empty.
        If called without arguments an empty tree (without leaves) is created.
        """
        keys = [key for key in list(dict.fromkeys([path[0] for path in paths if path and '' not in path])) if key != '#']
        if not keys: return
        for key in keys:
            subpaths = [path[1:] for path in paths if path and path[0] == key and path[1:]]
            self.__dict__[key] = _DataTree(subpaths) if subpaths else _TimeoutVar(3)

    def __getitem__(self, path: List[any]):
        """
        Get the item for the correspondent path. Raise a KeyError if the given path is invalid.
        :param path: A list of objects from the root to the leafs.
        :return: The value of the TimeoutVar or a DataTree object if the path does not refer to a leaf.
        """
        if path[0] not in self.__dict__ or (isinstance(self.__dict__[path[0]], _TimeoutVar) and path[1:]):
            raise KeyError(path)
        if path[1:]: return self.__dict__[path[0]][path[1:]]
        elif isinstance(self.__dict__[path[0]], _TimeoutVar): return self.__dict__[path[0]].value
        else: return self.__dict__[path[0]]

    def __setitem__(self, path: List[any], value):
        """
        Set the value of the object in the given path. Raise a KeyError if the given path is invalid.
        :param path: A list of objects from the root to the leafs.
        :param value: The value to set to the object.
        """
        if path[0] not in self.__dict__: self.__dict__[path[0]] = _DataTree() if path[1:] else _TimeoutVar(3)
        if isinstance(self.__dict__[path[0]], _TimeoutVar) and path[1:]: raise KeyError(path)
        if path[1:]: self.__dict__[path[0]][path[1:]] = value
        elif isinstance(self.__dict__[path[0]], _TimeoutVar): self.__dict__[path[0]].value = value
        else: self.__dict__[path[0]] = value

    def __contains__(self, path: List[any]):
        """
        Tell if the given path is contained in the tree.
        :param path: A list of objects from the root to the leafs.
        :return: True if the path is contained in the tree, false otherwise.
        """
        if not path[0] in self.__dict__: return False
        if isinstance(self.__dict__[path[0]], _TimeoutVar) and path[1:]: return False
        return path[1:] in self.__dict__[path[0]] if path[1:] else True

    def __iter__(self):
        """
        Return an iterator through the current level of the tree.
        :return: The iterator object.
        """
        items = []
        for key, obj in self.__dict__.items():
            items += [(key, obj.value)] if isinstance(obj, _TimeoutVar) else [(key, obj)]
        return items.__iter__()

    def __repr__(self):
        """
        Define the representation of the object.
        :return: The string representation of the current and next tree levels.
        """
        return f"<DataTree: {self.__dict__}>"


class _TimeoutVar:
    """
    Class for the creation of variables with timeout.
    A timeout variable auto resets itself to a default value if it's not changed after the set timeout time.
    """

    def __init__(self, timeout_sec: float):
        """
        Initialize the variable. The variable is initially outdated.
        :param timeout_sec: The time interval to wait before resetting the variable.
        """
        self.__value = None
        self.__timeout_sec = timeout_sec
        self.__timeout_timer = None

    @property
    def value(self):
        """
        Getter method for the value of the variable.
        :return: The value of the variable, or eventually None, if the variable is outdated.
        """
        return self.__value

    @value.setter
    def value(self, value: any):
        """
        Setter method for the value of the variable. By setting the variable the timeout timer is reset.
        :param value: The value of the variable.
        """
        self.__value = value
        if self.__value:
            if self.__timeout_timer is not None: self.__timeout_timer.cancel()
            self.__timeout_timer = Timer(self.__timeout_sec, setattr, [self, 'value', None])
            self.__timeout_timer.start()

    def __repr__(self):
        """
        Define the representation of the variable.
        :return: The string representation of the actual state of the value.
        """
        return f"<TimeoutVar: {self.__value}>" if self.__value else "Outdated"
