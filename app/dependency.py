from enum import Enum

from app.data_object import *


class DependencyKind(Enum):
    RUNTIME = 1
    DEVELOPMENT = 2
    UNKNOWN = 3

    def __str__(self):
        if self == DependencyKind.RUNTIME:
            return 'runtime'
        elif self == DependencyKind.DEVELOPMENT:
            return 'development'
        else:
            return 'unknown'


class Dependency(DataObject):

    def __init__(self, name, kind, number=None):
        self.name = name
        self.kind = kind
        self.number = number

    @staticmethod
    def runtime(name, number=None):
        return Dependency(name, DependencyKind.RUNTIME, number)

    @staticmethod
    def development(name, number=None):
        return Dependency(name, DependencyKind.DEVELOPMENT, number)

    def __str__(self):
        number = 'latest' if self.number is None else self.number
        return '[{0}] {1}:{2}'.format(self.kind, self.name, number)

    def __repr__(self):
        return str(self)
