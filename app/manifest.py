from app.data_object import *
from app.package_version import PackageVersion


class ManifestVersion(PackageVersion):
    def __init__(self, manifest):
        super().__init__(
            name=f'{{{manifest.formatted_paths}}}',
            number=None,
            runtime_dependencies=manifest.runtime_dependencies,
            development_dependencies=manifest.development_dependencies,
            licenses=[]
        )

    @property
    def id(self):
        return self.name


class Manifest(DataObject):

    def __init__(self, platform, repository, paths, runtime_dependencies, development_dependencies):
        self.platform = platform
        self.repository = repository
        self.paths = paths
        self.runtime_dependencies = runtime_dependencies
        self.development_dependencies = development_dependencies
        self.version = ManifestVersion(self)

    @property
    def formatted_paths(self):
        return '|'.join(self.paths)

    @property
    def urls(self):
        return [self.repository.master_url(i) for i in self.paths]

    def __str__(self):
        return f'{self.repository} {{{self.formatted_paths}}} [{self.platform}]'

    def __repr__(self):
        return str(self)
