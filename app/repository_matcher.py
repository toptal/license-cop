from abc import *

from app.data_object import DataObject


class PackageDescriptorPattern(DataObject):
    def __init__(self, id, files):
        self.id = id
        self.files = files

    @staticmethod
    def one_file(id, file):
        return PackageDescriptorPattern(id, [file])

    @staticmethod
    def multiple_files(id, files):
        return PackageDescriptorPattern(id, files)


class PackageDescriptorPatternMatch(DataObject):
    def __init__(self, pattern_id, paths):
        self.pattern_id = pattern_id
        self.paths = paths


class RepositoryMatch(DataObject):
    def __init__(self, matcher, repository, pattern_matches):
        self.__matcher = matcher
        self.repository = repository
        self.pattern_matches = pattern_matches

    def package_descriptors(self):
        return list(map(
            lambda i:
                self.__matcher._fetch_package_descriptor(self.repository, i),
            self.pattern_matches
        ))


class RepositoryMatcher(ABC):
    def __init__(self, patterns):
        self._patterns = patterns

    def match(self, repository):
        matches = []
        for pattern in self._patterns:
            m = self.__match_pattern(repository, pattern)
            if m:
                matches.append(m)

        return RepositoryMatch(self, repository, matches) if matches else None

    def __match_pattern(self, repository, pattern):
        # For now, this is a dumb filename match.
        # However, we will be using the GitHub search API
        # in the future.
        # https://stackoverflow.com/questions/25564760/how-can-i-search-file-name-in-specific-github-repository
        pattern_matches = []
        for file in pattern.files:
            if repository.path_exists(file):
                pattern_matches.append(file)
        if pattern_matches:
            return PackageDescriptorPatternMatch(pattern.id, pattern_matches)

    @abstractmethod
    def _fetch_package_descriptor(self, repository, pattern_match):
        pass
