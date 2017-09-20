import requests
from abc import *


class PackageRegistry(ABC):
    def __init__(self, http_compression=True):
        self._session = requests.Session()
        if not http_compression:
            self._session.headers.update({'Accept-Encoding': 'identity'})

    @abstractmethod
    def fetch_version(self, name, number):
        pass

    @abstractmethod
    def fetch_latest_version(self, name):
        pass
