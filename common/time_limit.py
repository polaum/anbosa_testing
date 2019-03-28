import signal


class TimeLimit:
    """
    This class implements a time-limit. The following usage example limits the execution time
    of the code wrapped by the with-statement to 60 seconds.
    TimeoutError with the error_message is raised if the limit has been exceeded.
    Usage:
    with TimeLimit(seconds=60, error_message='some error happened.'):
        initialize_the_universe()
    """

    def __init__(self, seconds=1, error_message=f'Timeout'):
        self.seconds = seconds
        self.error_message = error_message
        self._did_timeout = False

    def handle_timeout(self, signum, frame):
        """ do not touch input params! """
        self._did_timeout = True
        raise Exception()

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, _type, value, traceback):
        signal.alarm(0)
        if self._did_timeout:
            raise TimeoutError(self.error_message)
