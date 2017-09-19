from app.data_object import *


# Right now, this is a dumb class. But we plan to add logic to compute
# version requirements into it soon.
class Dependency(DataObject):
    def __init__(self, name):
        self.name = name
