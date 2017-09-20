from enum import Enum
from io import StringIO

from app.package_registry import *


class DependencyResolutionKind(Enum):
    RUNTIME = 1
    RUNTIME_AND_DEVELOPMENT = 2


class DependencyResolution:

    def __init__(self, version):
        self.version = version
        self.parent = None
        self.children = []

    @property
    def is_root(self): return self.parent is None

    @property
    def is_leaf(self): return self.children == []

    @property
    def name(self): return self.version.name

    @property
    def number(self): return self.version.number

    def dependencies(self, resolution_kind):
        if resolution_kind == DependencyResolutionKind.RUNTIME:
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
        header = '{0}{1} {2}'.format(
            self.__indentation(level),
            '•' if node.is_leaf else '+',
            str(node.version)
        )
        print(header, file=io)

    def __indentation(self, level):
        if level == 0:
            return ''
        return ('⎮  ' * (level - 1)) + '⎮--'
