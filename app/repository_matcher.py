from abc import *
from itertools import groupby

from app.data_object import DataObject


class ManifestMatch(DataObject):
    def __init__(self, nodes):
        self.nodes = nodes

    @property
    def paths(self):
        return [i.path for i in self.nodes]


class RepositoryMatch(DataObject):
    def __init__(self, matcher, repository, manifest_matches):
        self.__matcher = matcher
        self.repository = repository
        self.manifest_matches = manifest_matches
        self.__manifests = None

    @property
    def manifests(self):
        if not self.__manifests:
            self.__manifests = [
                self.__matcher._fetch_manifest(self.repository, i)
                for i in self.manifest_matches
            ]
        return self.__manifests

    def manifest_at(self, path):
        for d in self.manifests:
            if path in d.paths:
                return d
        return None


class RepositoryMatcher(ABC):
    def __init__(self, patterns):
        self.__patterns = patterns

    @abstractmethod
    def _fetch_manifest(self, repository, match):
        pass

    def match(self, repository):
        matches = self.__match_patterns(repository.master_tree)
        return RepositoryMatch(self, repository, matches) if matches else None

    def __match_patterns(self, tree):
        sort_key = (lambda i: i.parent.path)
        nodes = sorted(self.__search_patterns(tree), key=sort_key)
        return [ManifestMatch(list(i[1])) for i in groupby(nodes, key=sort_key)]

    def __search_patterns(self, tree):
        results = []
        for i in self.__patterns:
            results.extend(tree.deep_search(i))
        return results
