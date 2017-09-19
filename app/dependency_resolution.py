from enum import Enum

from app.package_repository import *


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

    def dependencies(self, resolution_kind):
        if resolution_kind == DependencyResolutionKind.RUNTIME:
            return self.version.runtime_dependencies
        else:
            return (self.version.runtime_dependencies +
                    self.version.development_dependencies)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
