from app.data_object import *


class Dependency(DataObject):
    RUNTIME = 1
    DEVELOPMENT = 2

    def __init__(self, name, kind, number=None):
        self.name = name
        self.kind = kind
        self.number = None
