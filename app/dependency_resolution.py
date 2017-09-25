from enum import Enum
from io import StringIO

from app.dependency import *
from app.package_registry import *


class DependencyResolution:

    def __init__(self, version, kind):
        self.version = version
        self.kind = kind
        self.parent = None
        self.children = []

    @staticmethod
    def runtime(version):
        return DependencyResolution(version, DependencyKind.RUNTIME)

    @staticmethod
    def development(version):
        return DependencyResolution(version, DependencyKind.DEVELOPMENT)

    @property
    def is_root(self): return self.parent is None

    @property
    def is_leaf(self): return self.children == []

    @property
    def name(self): return self.version.name

    @property
    def number(self): return self.version.number

    def dependencies(self, runtime_only):
        if runtime_only:
            return self.version.runtime_dependencies
        else:
            return (self.version.runtime_dependencies +
                    self.version.development_dependencies)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return self

    def __repr__(self):
        io = StringIO()
        self.__print_node(io, self, 0)
        return io.getvalue()

    def __print_node(self, io, node, level):
        self.__print_node_header(io, node, level)
        for child in node.children:
            self.__print_node(io, child, level + 1)

    def __print_node_header(self, io, node, level):
        header = '{0}{1} {2} {3}'.format(
            self.__indentation(level),
            '•' if node.is_leaf else '+',
            self.__format_kind(node.kind),
            str(node.version)
        )
        print(header, file=io)

    def __format_kind(self, kind):
        if kind == DependencyKind.RUNTIME:
            return '[runtime]'
        elif kind == DependencyKind.DEVELOPMENT:
            return '[development]'
        else:
            return '[unknown]'

    def __indentation(self, level):
        if level == 0:
            return ''
        return ('⎮  ' * (level - 1)) + '⎮--'
