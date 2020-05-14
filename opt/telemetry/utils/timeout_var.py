from threading import Timer


class TimeoutVar:
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

    def __str__(self):
        """
        Define the string representation of the variable.
        :return: The string representation of the value of the object.
        """
        return str(self.__value)
    __repr__ = __str__
