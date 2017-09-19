from app.package_repository import *


class DependencyResolution:
    def __init__(self, kind, version):
        self.kind = kind
        self.version = version
        self.parent = None
        self.children = []

    @property
    def name(self): return self.version.name

    @property
    def number(self): return self.version.number

    @property
    def licenses(self): return self.version.licenses

    @property
    def dependencies(self):
        if self.kind == DependencyKind.RUNTIME:
            return self.version.runtime_dependencies
        else:
            return self.version.development_dependencies

    @property
    def is_root(self): return self.parent is None

    @property
    def is_leaf(self): return self.children == []

    def add_child(self, dependency_resolution):
        dependency_resolution.parent = self
        self.children.append(dependency_resolution)
