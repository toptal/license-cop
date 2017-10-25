from app.data_object import *


class PackageVersion(DataObject):
    def __init__(self, name, number, licenses,
                 runtime_dependencies, development_dependencies):
        self.name = name
        self.number = number
        self.runtime_dependencies = runtime_dependencies
        self.development_dependencies = development_dependencies
        self.licenses = licenses

    @property
    def id(self):
        return f'{str(self.name)}:{self.formatted_number}'

    @property
    def formatted_number(self):
        return str(self.number) if self.number else 'latest'

    @property
    def formatted_licenses(self):
        return '|'.join(self.licenses) if self.licenses else '<no licenses found>'

    def __str__(self):
        return self.id

    def __repr__(self):
        return f'{str(self)} → {self.formatted_licenses}'


class PackageVersionNotFound(PackageVersion):
    def __init__(self, name, number=None):
        super().__init__(name, number, [], [], [])

    def __repr__(self):
        return f'{str(self)} → <version not found on registry>'
