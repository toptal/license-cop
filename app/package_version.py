from app.data_object import *


class PackageVersion(DataObject):
    def __init__(self, name, number, licenses,
                 runtime_dependencies, development_dependencies):
        self.name = name
        self.number = number
        self.runtime_dependencies = runtime_dependencies
        self.development_dependencies = development_dependencies
        self.licenses = licenses

    def __str__(self):
        return '{0}:{1} → {2}'.format(
            self.name,
            self.number,
            ', '.join(self.licenses) if self.licenses else '<no licenses found>'
        )


class PackageVersionNotFound(PackageVersion):
    def __init__(self, name, number=None):
        super().__init__(name, number, [], [], [])

    def __str__(self):
        return '{0}:{1} → <version not found on registry>'.format(
            self.name,
            'latest' if self.number is None else self.number
        )
