from typing import List

from utils import TimeoutVar


class DataTree:
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
            self.__dict__[key] = DataTree(subpaths) if subpaths else TimeoutVar(3)

    def __getitem__(self, path: List[any]):
        """
        Get the item for the correspondent path. Raise a KeyError if the given path is invalid.
        :param path: A list of objects from the root to the leafs.
        :return: The value of the TimeoutVar or a DataTree object if the path does not refer to a leaf.
        """
        if path[0] not in self.__dict__ or (isinstance(self.__dict__[path[0]], TimeoutVar) and path[1:]):
            raise KeyError(path)
        if path[1:]: return self.__dict__[path[0]][path[1:]]
        elif isinstance(self.__dict__[path[0]], TimeoutVar): return self.__dict__[path[0]].value
        else: return self.__dict__[path[0]]

    def __setitem__(self, path: List[any], value):
        """
        Set the value of the object in the given path. Raise a KeyError if the given path is invalid.
        :param path: A list of objects from the root to the leafs.
        :param value: The value to set to the object.
        """
        if path[0] not in self.__dict__: self.__dict__[path[0]] = DataTree() if path[1:] else TimeoutVar(3)
        if isinstance(self.__dict__[path[0]], TimeoutVar) and path[1:]: raise KeyError(path)
        if path[1:]: self.__dict__[path[0]][path[1:]] = value
        elif isinstance(self.__dict__[path[0]], TimeoutVar): self.__dict__[path[0]].value = value
        else: self.__dict__[path[0]] = value

    def __contains__(self, path: List[any]):
        """
        Tell if the given path is contained in the tree.
        :param path: A list of objects from the root to the leafs.
        :return: True if the path is contained in the tree, false otherwise.
        """
        if not path[0] in self.__dict__: return False
        if isinstance(self.__dict__[path[0]], TimeoutVar) and path[1:]: return False
        return path[1:] in self.__dict__[path[0]] if path[1:] else True

    def __iter__(self):
        """
        Return an iterator through the current level of the tree.
        :return: The iterator object.
        """
        items = []
        for key, obj in self.__dict__.items():
            items += [(key, obj.value)] if isinstance(obj, TimeoutVar) else [(key, obj)]
        return items.__iter__()

    def __str__(self):
        """
        Define the string representation of the object.
        :return: The string representation of the current and next tree levels.
        """
        return str(self.__dict__)
    __repr__ = __str__
