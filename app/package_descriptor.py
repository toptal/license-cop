from app.data_object import *


class PackageDescriptor(DataObject):
    def __init__(self, platform, repository, path, runtime_dependencies, development_dependencies):
        self.platform = platform
        self.repository = repository
        self.path = path
        self.runtime_dependencies = runtime_dependencies
        self.development_dependencies = development_dependencies
