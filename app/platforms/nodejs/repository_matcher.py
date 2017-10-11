import json

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *
from app.platforms.nodejs.shared import parse_dependencies


class NodejsRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__(['package.json'])

    def _fetch_package_descriptor(self, repository, match):
        package_json = match.paths[0]

        data = json.loads(repository.read_text_file(package_json))

        return PackageDescriptor(
            platform='Node.js',
            repository=repository,
            paths=match.paths,
            runtime_dependencies=parse_dependencies(data, DependencyKind.RUNTIME),
            development_dependencies=parse_dependencies(data, DependencyKind.DEVELOPMENT)
        )
