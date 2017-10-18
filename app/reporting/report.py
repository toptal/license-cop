from abc import ABC, abstractmethod


class Report(ABC):

    def __init__(self, max_depth=None):
        self._max_depth = max_depth

    def process(self, match):
        for i in match.resolve(self._max_depth):
            self._write(i)

    @abstractmethod
    def _write(self, resolution):
        pass

    @abstractmethod
    def close(self):
        pass
