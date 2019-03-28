from datetime import datetime


class Timer:
    @property
    def duration(self):
        return self.__duration

    def __enter__(self):
        self.start = datetime.now()
        return self

    def __exit__(self, *args, **kwargs):
        self.__duration = datetime.now() - self.start
