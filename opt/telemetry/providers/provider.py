class Provider:
    """ Class for gathering of data coming from generic sources. Maps the sources into a dictionary with the
    correspondent instance of the sensor. Sources can be accessed via typical square brackets notation.
    """

    def __init__(self, sources, name):
        """ Initialize the provider with the given name. \n
        :param name: The display name of the provider.
        """
        self.name = name
        self.sources = sources

    def get(self, path):
        """ Get the item in the given position identified by the key. \n
        :param path: The source path.
        :return: The source instance correspondent to the key.
        """
        if path == '/': return {source: self.sources[source]['/'] for source in self.sources}
        if '/' in path: return self.sources[path[:path.find('/')]][path[path.find('/') + 1:]]
        else: return self.sources[path]['/']
    __getitem__ = get

    def __contains__(self, path):
        """ Tell if a path is contained in the dictionary of sources. \n
        :param path: The source name.
        :return: True if the key is present in the dictionary, false otherwise.
        """
        return path[path.find('/') + 1:] in self.sources[path[:path.find('/')]] if '/' in path else path in self.sources

    def keys(self):
        """ Return the list of keys. \n
        :return: A KeysView object containing all the keys.
        """
        keys = []
        for source in self.sources: keys += [f'{source}/{key}' for key in self.sources[source].keys()]
        return keys

    def items(self):
        """ Return the items of the dictionary of sources. \n
        :return: An ItemsView object containing all the items as a tuple (path, value).
        """
        items = []
        for source in self.sources: items += [(f'{source}/{key}', value) for key, value in self.sources[source].items()]
        return items

    def __iter__(self):
        """ Get an iterator over the dictionary of sources. \n
        :return: The Iterator object.
        """
        return self.keys().__iter__()

    def __len__(self):
        """ Return the number of sources paths in the dictionary. \n
        :return: An integer representing the length of the dictionary of sources.
        """
        return len(self.sources.keys())

    def __str__(self):
        """ Return a string representation of the provider. \n
        :return: The string representation as the representation of the values in the dictionary of sources.
        """
        return f'<{__name__}: {str(self["/"])}>'
    __repr__ = __str__

    def stop(self): pass
