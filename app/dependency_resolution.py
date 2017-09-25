from enum import Enum
from io import StringIO

from app.dependency import *
from app.package_registry import *


class DependencyResolution:

    def __init__(self, version, kind, is_hidden=False):
        self.version = version
        self.kind = kind
        self.parent = None
        self.is_hidden = is_hidden
        self.children = []

    @staticmethod
    def runtime(version, is_hidden=False):
        return DependencyResolution(version, DependencyKind.RUNTIME, is_hidden)

    @staticmethod
    def development(version, is_hidden=False):
        return DependencyResolution(version, DependencyKind.DEVELOPMENT, is_hidden)

    @property
    def is_root(self): return self.parent is None

    @property
    def is_leaf(self): return self.children == []

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

    def hide(self):
        self.is_hidden = True

    def __repr__(self, level=0):
        io = StringIO()
        self.__print_node(io, self, level)
        return io.getvalue()

    def __print_node(self, io, node, level):
        self.__print_node_header(io, node, level)
        for child in node.children:
            self.__print_node(io, child, level + 1)

    def __print_node_header(self, io, node, level):
        header = '{0}{1} {2} {3}'.format(
            self.__indentation(level),
            self.__format_bullet(node),
            self.__format_kind(node),
            str(node.version)
        )
        print(header, file=io)

    def __format_kind(self, node):
        if node.kind == DependencyKind.RUNTIME:
            return '[runtime]'
        elif node.kind == DependencyKind.DEVELOPMENT:
            return '[development]'
        else:
            return '[unknown]'

    def __format_bullet(self, node):
        if node.is_hidden:
            return '•'
        elif not node.is_leaf:
            return '+'
        else:
            return '-'

    def __indentation(self, level):
        if level == 0:
            return ''
        return ('⎮  ' * (level - 1)) + '⎮--'
