import requests
from abc import *

from app.data_object import *


# Right now, this is a dumb class. But we plan to add logic to compute
# version requirements into it soon.
class Dependency(DataObject):
    def __init__(self, name):
        self.name = name


class Package(DataObject):
    def __init__(self, name, version, dependencies, licenses):
        self.name = name
        self.version = version
        self.dependencies = dependencies
        self.licenses = licenses


class PackageRepository(ABC):
    def __init__(self, http_compression=True):
        self._session = requests.Session()
        if not http_compression:
            self._session.headers.update({'Accept-Encoding': 'identity'})

    @abstractmethod
    def fetch_package(self, name, version):
        pass
