from app.data_object import *


class PackageVersion(DataObject):
    def __init__(self, name, number, licenses,
                 runtime_dependencies, development_dependencies):
        self.name = name
        self.number = number
        self.runtime_dependencies = runtime_dependencies
        self.development_dependencies = development_dependencies
        self.licenses = licenses
