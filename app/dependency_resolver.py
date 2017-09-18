from app.package_repository import *
from app.dependency_resolution import *


class DependencyResolver:
    def __init__(self, repository):
        self.__repository = repository

    def resolve_version(self, kind, name, number):
        root = self.__build_node(kind, name, number)
        nodes_to_expand = [root]
        while nodes_to_expand:
            node = nodes_to_expand.pop()
            expansion = self.__expand_node(node)
            nodes_to_expand.extend(expansion)
        return root

    def __expand_node(self, node):
        expansion = []
        for dependency in node.dependencies:
            if not node.is_circular(dependency):
                child = self.__build_node(node.kind, dependency.name)
                node.add_child(child)
                expansion.append(child)
        return expansion

    def __build_node(self, kind, name, number=None):
        if number is not None:
            version = self.__repository.fetch_version(name, number)
        else:
            version = self.__repository.fetch_latest_version(name)
        return DependencyResolution(kind, version)
