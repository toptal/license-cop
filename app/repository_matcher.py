from abc import *


class RepositoryMatcher(ABC):

    class __Match:
        def __init__(self, matcher, repository, paths):
            self.__matcher = matcher
            self.__repository = repository
            self.__paths = paths

        def package_descriptors(self):
            return list(map(
                lambda path:
                    self.__matcher._fetch_package_descriptor(self.__repository, path),
                self.__paths
            ))

    def __init__(self, paths):
        self._paths = paths

    def match(self, repository):
        for path in self._paths:
            # For now, this is a dumb filename match.
            # However, we will be using the GitHub search API
            # in the future.
            # https://stackoverflow.com/questions/25564760/how-can-i-search-file-name-in-specific-github-repository
            if repository.path_exists(path):
                return RepositoryMatcher.__Match(self, repository, self._paths)
        return None

    @abstractmethod
    def _fetch_package_descriptor(self, repository, path):
        pass
