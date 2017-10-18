from io import StringIO

from app.dependency_resolution import DependencyResolution
from app.dependency import DependencyKind


class PackageDescriptorResolution(DependencyResolution):

    def __init__(self, package_descriptor):
        super().__init__(package_descriptor.version, DependencyKind.RUNTIME)
        self.package_descriptor = package_descriptor

    def __str__(self):
        return str(self.package_descriptor)

    def __repr__(self):
        io = StringIO()
        self.print(io)
        return io.getvalue()

    def print(self, file):
        print(f'+ {repr(self.package_descriptor)}', file=file)
        self.__print_children(file, DependencyKind.RUNTIME)
        self.__print_children(file, DependencyKind.DEVELOPMENT)

    def __print_children(self, file, kind):
        for child in filter(lambda i: i.kind == kind, self.children):
            file.write(child.__repr__(1))
