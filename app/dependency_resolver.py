from collections import deque

from app.package_repository import *
from app.dependency_resolution import *


class DependencyResolver:
    def __init__(self, repository):
        self.__repository = repository

    def resolve_version(self, kind, name, number):
        root = self.__build_node(kind, name, number)
        visited_dependencies = set()
        nodes_to_expand = deque()

        nodes_to_expand.append(root)
        while nodes_to_expand:
            current_node = nodes_to_expand.popleft()
            for dependency in current_node.dependencies:
                if dependency not in visited_dependencies:
                    child = self.__build_node(current_node.kind, dependency.name)
                    current_node.add_child(child)
                    visited_dependencies.add(dependency)
                    nodes_to_expand.append(child)
        return root

    def __build_node(self, kind, name, number=None):
        if number is not None:
            version = self.__repository.fetch_version(name, number)
        else:
            version = self.__repository.fetch_latest_version(name)
        return DependencyResolution(kind, version)
