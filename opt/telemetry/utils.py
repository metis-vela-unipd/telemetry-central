from threading import Timer

class TimeoutVar:
    """
    Class for the creation of variables with timeout.

    A timeout variable auto resets itself to a default value if it's not changed after the set timeout time.
    In this case the default value represent the unavailable state of the gps data.
    """

    def __init__(self, default, timeout_sec):
        """ Set options and initialize variable to it's default value. """
        self.actual = default
        self.default = default
        self.timeout_sec = timeout_sec
        self.timeout_timer = None

    def setValue(self, value):
        """ Set the value of the variable and reset the timeout timer. """
        self.actual = value
        if self.actual != self.default:
            if self.timeout_timer is not None: self.timeout_timer.cancel()
            self.timeout_timer = Timer(self.timeout_sec, self.setValue, [self.default])
            self.timeout_timer.start()
    
    def isDefault(self):
        """ Tell if the variable value is the default one. """
        return self.actual == self.default