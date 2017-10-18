from enum import Enum
from io import StringIO

from app.package_version import *
from app.dependency import *
from app.reverse_dependency import *
from app.package_registry import *


class DependencyResolution:

    def __init__(self, version, kind, hidden=False):
        self.version = version
        self.kind = kind
        self.parent = None
        self.hidden = hidden
        self.children = []

    @classmethod
    def runtime(cls, version, hidden=False):
        return cls(version, DependencyKind.RUNTIME, hidden)

    @classmethod
    def development(cls, version, hidden=False):
        return cls(version, DependencyKind.DEVELOPMENT, hidden)

    @property
    def is_runtime(self): return self.kind == DependencyKind.RUNTIME

    @property
    def is_development(self): return self.kind == DependencyKind.DEVELOPMENT

    @property
    def is_root(self): return self.parent is None

    @property
    def is_leaf(self): return self.children == []

    @property
    def is_tree(self): return not self.is_leaf

    @property
    def found(self):
        return not isinstance(self.version, PackageVersionNotFound)

    @property
    def name(self): return self.version.name

    @property
    def number(self): return self.version.number

    def dependencies(self, runtime_only=False):
        if runtime_only:
            return self.version.runtime_dependencies
        else:
            return (self.version.runtime_dependencies +
                    self.version.development_dependencies)

    def has_dependencies(self, runtime_only=False):
        if runtime_only:
            return len(self.version.runtime_dependencies) > 0
        else:
            return (len(self.version.runtime_dependencies) > 0 or
                    len(self.version.development_dependencies) > 0)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return self

    def add_children(self, children):
        for i in children:
            self.add_child(i)
        return self

    def hide(self):
        self.hidden = True

    def reverse_dependencies(self):
        collected = {}
        self.__reverse_dependencies(collected)
        return collected.values()

    def __reverse_dependencies(self, collected):
        for child in self.children:
            v = child.version
            if v not in collected:
                collected[v] = ReverseDependency(v)
            collected[v].add_reference(child.parent, child.kind)
            child.__reverse_dependencies(collected)

    def __repr__(self, level=0):
        io = StringIO()
        self.__print(io, level)
        return io.getvalue()

    def __print(self, io, level):
        self.__print_header(io, level)
        for child in self.children:
            child.__print(io, level + 1)

    def __print_header(self, io, level):
        header = '{0}{1} [{2}] {3}'.format(
            self.__indentation(level),
            self.__bullet(),
            str(self.kind),
            repr(self.version)
        )
        print(header, file=io)

    def __bullet(self):
        if self.hidden:
            return '•'
        elif not self.found:
            return '!'
        elif self.is_leaf:
            return '='
        else:
            return '+'

    @staticmethod
    def __indentation(level):
        if level == 0:
            return ''
        return ('⎮  ' * (level - 1)) + '⎮--'
