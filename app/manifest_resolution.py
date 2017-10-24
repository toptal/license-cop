from io import StringIO

from app.dependency_resolution import DependencyResolution
from app.dependency import DependencyKind


class ManifestResolution(DependencyResolution):

    def __init__(self, manifest):
        super().__init__(manifest.version, DependencyKind.RUNTIME)
        self.manifest = manifest

    def __str__(self):
        return str(self.manifest)

    def __repr__(self):
        io = StringIO()
        self.print(io)
        return io.getvalue()

    def print(self, file):
        print(f'+ {repr(self.manifest)}', file=file)
        self.__print_children(file, DependencyKind.RUNTIME)
        self.__print_children(file, DependencyKind.DEVELOPMENT)

    def __print_children(self, file, kind):
        for child in (i for i in self.children if i.kind == kind):
            file.write(child.__repr__(1))
