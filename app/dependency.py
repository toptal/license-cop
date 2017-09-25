from app.data_object import *


class Dependency(DataObject):
    RUNTIME = 1
    DEVELOPMENT = 2

    def __init__(self, name, kind, number=None):
        self.name = name
        self.kind = kind
        self.number = None

    @staticmethod
    def runtime(name, number=None):
        return Dependency(name, Dependency.RUNTIME, number)

    @staticmethod
    def development(name, number=None):
        return Dependency(name, Dependency.DEVELOPMENT, number)
