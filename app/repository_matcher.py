from abc import *
from itertools import groupby

from app.data_object import DataObject


class PackageDescriptorMatch(DataObject):
    def __init__(self, nodes):
        self.nodes = nodes

    @property
    def paths(self):
        return [i.path for i in self.nodes]


class RepositoryMatch(DataObject):
    def __init__(self, matcher, repository, package_descriptor_matches):
        self.__matcher = matcher
        self.repository = repository
        self.package_descriptor_matches = package_descriptor_matches

    def package_descriptors(self):
        return list(map(
            lambda i:
                self.__matcher._fetch_package_descriptor(self.repository, i),
            self.package_descriptor_matches
        ))

    def package_descriptor_at(self, path):
        for d in self.package_descriptors():
            if path in d.paths:
                return d
        return None


class RepositoryMatcher(ABC):
    def __init__(self, patterns):
        self.__patterns = patterns

    @abstractmethod
    def _fetch_package_descriptor(self, repository, match):
        pass

    def match(self, repository):
        tree = repository.fetch_tree()
        matches = self.__match_patterns(tree)
        return RepositoryMatch(self, repository, matches) if matches else None

    def __match_patterns(self, tree):
        sort_key = (lambda i: i.parent.path)
        nodes = sorted(self.__search_patterns(tree), key=sort_key)
        return list(map(
            lambda i: PackageDescriptorMatch(list(i[1])),
            groupby(nodes, key=sort_key)
        ))

    def __search_patterns(self, tree):
        results = []
        for i in self.__patterns:
            results.extend(tree.deep_search(i))
        return results
