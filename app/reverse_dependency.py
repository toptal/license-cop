from app.data_object import DataObject
from app.dependency import DependencyKind


class ReverseDependency(DataObject):

    def __init__(self, version):
        self.version = version
        self.runtime_references = []
        self.development_references = []

    @property
    def name(self):
        return self.version.name

    @property
    def number(self):
        return self.version.number

    def add_reference(self, reference, kind):
        if kind == DependencyKind.DEVELOPMENT:
            self.development_references.append(reference)
        else:
            self.runtime_references.append(reference)
