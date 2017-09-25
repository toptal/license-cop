import json

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *
from app.platforms.nodejs.shared import parse_dependencies


class NodejsRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__(['package.json'])

    def _fetch_package_descriptor(self, repository, path):
        raw_data = repository.read_text_file(path)
        data = json.loads(raw_data)

        return PackageDescriptor(
            platform='Node.js',
            repository=repository,
            path=path,
            runtime_dependencies=parse_dependencies(data, Dependency.RUNTIME),
            development_dependencies=parse_dependencies(data, Dependency.DEVELOPMENT)
        )
