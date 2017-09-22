from abc import *


class RepositoryFilter(ABC):

    @abstractmethod
    def match(self, repository):
        pass

    @abstractmethod
    def extract_dependencies(self, repository):
        pass
