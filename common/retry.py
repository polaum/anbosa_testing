import logging
import time
from functools import wraps


class Retry:
    """
    usage:
    1.  @Retry(AssertionError, retries=5, interval=5)
        def my_function():
    2. Retry(AssertionError, retries=5, interval=5).this(my_function)
    """

    def __init__(self, exceptions_to_catch=Exception, retries: int = 3, interval: float = 1.0):
        """
        :param exceptions_to_catch: can be a tuple of exceptions
        :param retries: amount of retries
        :param interval: timeout between the retries
        """
        self._retry = self.retry(exceptions_to_catch, retries, interval)

    def __call__(self, f):
        return self._retry(f)

    @staticmethod
    def retry(exceptions_to_catch, retries: int = 2, interval: float = 2.0):
        def decorate_retry(f):

            @wraps(f)
            def f_retry(*args, **kwargs):
                logging.debug(f'RETRY: Giving function "{f.__name__}" {retries} chances to succeed.')
                for retry in range(1, retries + 1):
                    try:
                        return f(*args, **kwargs)
                    except exceptions_to_catch as e:
                        logging.warning(f'RETRY: {f.__name__} Attempt {retry}/{retries} failed for: {str(e).strip()} '
                                        f'args: {args} kwargs: {kwargs}')
                        if retry < retries:
                            logging.debug(f'RETRY: Retrying in {interval}s')
                            time.sleep(interval)
                        else:
                            raise e

            return f_retry

        return decorate_retry

    def this(self, func, *args, **kwargs):
        return self._retry(func)(*args, **kwargs)
