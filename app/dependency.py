from enum import Enum

from app.data_object import *


class DependencyKind(Enum):
    RUNTIME = 1
    DEVELOPMENT = 2
    UNKNOWN = 3


class Dependency(DataObject):

    def __init__(self, name, kind, number=None):
        self.name = name
        self.kind = kind
        self.number = None

    @staticmethod
    def runtime(name, number=None):
        return Dependency(name, DependencyKind.RUNTIME, number)

    @staticmethod
    def development(name, number=None):
        return Dependency(name, DependencyKind.DEVELOPMENT, number)
