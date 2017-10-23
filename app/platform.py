from app.dependency_resolver import DependencyResolver
from app.manifest_resolution import ManifestResolution


class PlatformRepositoryMatch:

    def __init__(self, platform, repository, match):
        self.platform = platform
        self.repository = repository
        self.__match = match
        self.__cache = {}

    @property
    def manifests(self):
        return self.__match.manifests

    def resolve(self, max_depth=None):
        if max_depth not in self.__cache:
            self.__cache[max_depth] = self.platform.resolve(self, max_depth)
        return self.__cache[max_depth]


class Platform:

    def __init__(self, name, matcher, registry):
        self.name = name
        self.__matcher = matcher
        self.__registry = registry

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def match(self, repository):
        m = self.__matcher.match(repository)
        if m:
            return PlatformRepositoryMatch(self, repository, m)

    def resolve(self, match, max_depth):
        return [self.__resolve_manifest(i, max_depth) for i in match.manifests]

    def __resolve_manifest(self, manifest, max_depth):
        resolver = DependencyResolver(self.__registry)
        root = ManifestResolution(manifest)
        if max_depth is None or max_depth > 0:
            root.add_children(self.__resolve_dependencies(resolver, max_depth, manifest.runtime_dependencies))
            root.add_children(self.__resolve_dependencies(resolver, max_depth, manifest.development_dependencies))
        return root

    def __resolve_dependencies(self, resolver, max_depth, dependencies):
        max_depth = None if max_depth is None else max_depth - 1
        return (resolver.resolve(i, max_depth) for i in dependencies)
