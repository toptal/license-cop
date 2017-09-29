from app.data_object import *


class PackageDescriptor(DataObject):

    def __init__(self, platform, repository, paths, runtime_dependencies, development_dependencies):
        self.platform = platform
        self.repository = repository
        self.paths = paths
        self.runtime_dependencies = runtime_dependencies
        self.development_dependencies = development_dependencies

    def __str__(self):
        return '{0} - {1} [{2}]'.format(
            self.repository,
            self.platform,
            ", ".join(self.paths)
        )
