from threading import Thread, Event


class Provider(Thread):
    """ Class for gathering of data coming from generic sources. Maps the sources into a dictionary with the
    correspondent instance of the sensor. Sources can be accessed via typical square brackets notation.
    """

    def __init__(self, name=None):
        """ Initialize the provider with the given name. \n
        :param name: The display name of the provider.
        """
        super().__init__(name=name, daemon=True)
        self.sources = {}
        self.end_setup = Event()

    def get(self, key):
        """ Get the item in the given position identified by the key. \n
        :param key: The source name.
        :return: The source instance correspondent to the key.
        """
        return self.sources[key]
    __getitem__ = get

    def __contains__(self, key):
        """ Tell if a key is contained in the dictionary of sources. \n
        :param key: The source name.
        :return: True if the key is present in the dictionary, false otherwise.
        """
        return key in self.sources

    def keys(self):
        """ Return the list of keys. \n
        :return: A KeysView object containing all the keys.
        """
        return self.sources.keys()

    def items(self):
        """ Return the items of the dictionary of sources. \n
        :return: An ItemsView object containing all the items as a tuple (key, value).
        """
        return self.sources.items()

    def __iter__(self):
        """ Get an iterator over the dictionary of sources. \n
        :return: The Iterator object.
        """
        return self.sources.__iter__()

    def __len__(self):
        """ Return the number of sources in the dictionary. \n
        :return: An integer representing the length of the dictionary of sources.
        """
        return len(self.sources)

    def __str__(self):
        """ Return a string representation of the provider. \n
        :return: The string representation as the representation of the values in the dictionary of sources.
        """
        return f'<{__name__}: {str(self.sources)}>'
    __repr__ = __str__
