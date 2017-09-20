from abc import *


class RepositoryFilter(ABC):

    @abstractmethod
    def match(self, repository):
        pass

    @abstractmethod
    def filter_dependencies(self, repository):
        pass
