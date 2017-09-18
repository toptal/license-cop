import requests
from abc import *
from enum import Enum

from app.data_object import *


class DependencyKind(Enum):
    RUNTIME = 1
    DEVELOPMENT = 2


# Right now, this is a dumb class. But we plan to add logic to compute
# version requirements into it soon.
class Dependency(DataObject):
    def __init__(self, name):
        self.name = name


class PackageVersion(DataObject):
    def __init__(self, name, number, licenses,
                 runtime_dependencies, development_dependencies):
        self.name = name
        self.number = number
        self.runtime_dependencies = runtime_dependencies
        self.development_dependencies = development_dependencies
        self.licenses = licenses


class PackageRepository(ABC):
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
