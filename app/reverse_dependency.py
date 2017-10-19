from app.data_object import DataObject
from app.dependency import DependencyKind


class ReverseDependency(DataObject):

    def __init__(self, version):
        self.version = version
        self.runtime_references = []
        self.development_references = []

    @property
    def name(self): return self.version.name

    @property
    def number(self): return self.version.number

    @property
    def formatted_runtime_references(self):
        return self.__formatted_references(self.runtime_references)

    @property
    def formatted_development_references(self):
        return self.__formatted_references(self.development_references)

    @staticmethod
    def __formatted_references(references):
        return ', '.join(str(i.version.id) for i in references)

    def add_reference(self, reference, kind):
        if reference:
            if kind == DependencyKind.DEVELOPMENT:
                self.development_references.append(reference)
            else:
                self.runtime_references.append(reference)
