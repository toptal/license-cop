from fnmatch import fnmatchcase
from pathlib import PurePosixPath


class GitNode:
    def __init__(self, name, parent, is_tree):
        self.name = name
        self.is_tree = is_tree
        self.children = []
        self.__parent = parent
        self.__path = None

    @property
    def parent(self):
        return self.__parent

    @property
    def path(self):
        if self.__path is None:
            self.__path = self.__compute_path()
        return self.__path

    def __compute_path(self):
        parts = []
        node = self
        while True:
            parts.append(node.name)
            if not node.parent:
                break
            node = node.parent
        parts.reverse()
        return str(PurePosixPath('').joinpath(*parts))

    @classmethod
    def root(cls, name=''):
        return cls(name, None, True)

    def add_tree(self, path):
        return self._add_path(path, True)

    def add_blob(self, path):
        return self._add_path(path, False)

    def navigate(self, path):
        parts = self.__split_path(path)
        node = self
        for p in parts:
            results = node.shallow_search(p)
            if not results:
                return None
            assert len(results) == 1
            node = results[0]
        return node

    def match(self, wildcard_pattern):
        return fnmatchcase(self.name, wildcard_pattern)

    def match_any(self, wildcard_patterns):
        return any(self.match(i) for i in wildcard_patterns)

    def deep_search(self, wildcard_pattern):
        node = self
        results = []
        for child in self.children:
            if child.match(wildcard_pattern):
                results.append(child)
            results.extend(child.deep_search(wildcard_pattern))
        return results

    def shallow_search(self, wildcard_pattern):
        return [i for i in self.children if i.match(wildcard_pattern)]

    def search_siblings(self, wildcard_pattern):
        if not self.parent:
            return []
        results = self.parent.shallow_search(wildcard_pattern)
        return [i for i in results if i is not self]

    def _add_path(self, path, is_tree):
        parts = self.__split_path(path)
        node = self
        for p in parts[:-1]:
            node = node._add_child(p, True)
        node._add_child(parts[-1], is_tree)

    def _add_child(self, name, is_tree):
        if not self.is_tree:
            raise ValueError(f'Path "{self.path}" is not a tree.')
        existing = self.__get_child(name)
        if not existing:
            child = GitNode(name, self, is_tree)
            self.children.append(child)
            return child
        return existing

    def __get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child

    def __split_path(self, path):
        return PurePosixPath(path).parts

    def __str__(self):
        return self.path

    def __repr__(self):
        return str(self)
