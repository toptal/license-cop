import json
import re
from configparser import ConfigParser

from app.dependency import *
from app.repository_matcher import *
from app.manifest import *


PIPFILE_PATTERN = 'Pipfile'

RUNTIME_REQUIREMENTS_PATTERNS = (
    'requirements.txt',
    'requirements'
)

DEVELOPMENT_REQUIREMENTS_PATTERNS = (
    'requirements?test.txt',
    'requirements?test',
    'requirements?dev.txt',
    'requirements?dev',
    'requirements?development.txt',
    'requirements?development',
    'test?requirements.txt',
    'test?requirements',
    'dev?requirements.txt',
    'dev?requirements',
    'development?requirements.txt',
    'development?requirements'
)

PATTERNS = [
    PIPFILE_PATTERN,
    *RUNTIME_REQUIREMENTS_PATTERNS,
    *DEVELOPMENT_REQUIREMENTS_PATTERNS
]

REQUIREMENT_REGEX = re.compile(r'^\s*(\w[\w\-\.]+)\s*')


def parse_requirements_file(data, kind):
    dependencies = []
    for line in data.splitlines():
        m = REQUIREMENT_REGEX.match(line)
        if m:
            name = m.group(1)
            dependencies.append(Dependency(name, kind))
    return dependencies


def __clean_pipfile_entry(e):
    e = e.replace('"', '')
    e = e.replace("'", '')
    e = e.strip()
    return e


def __parse_pipfile_section(parser, section, kind):
    return list(map(
        lambda i: Dependency(i, kind),
        map(lambda i: __clean_pipfile_entry(i), parser[section].keys())
    ))


def parse_pipfile(data):
    parser = ConfigParser()
    parser.read_string(data)
    return (
        __parse_pipfile_section(parser, 'packages', DependencyKind.RUNTIME),
        __parse_pipfile_section(parser, 'dev-packages', DependencyKind.DEVELOPMENT)
    )


class PythonRepositoryMatcher(RepositoryMatcher):
    def __init__(self):
        super().__init__(PATTERNS)

    def _fetch_manifest(self, repository, match):
        runtime = []
        development = []

        for node in match.nodes:
            data = repository.read_text_file(node.path)
            self.__collect_dependencies(node, data, runtime, development)

        return Manifest(
            platform='Python',
            repository=repository,
            paths=match.paths,
            runtime_dependencies=runtime,
            development_dependencies=development
        )

    def __collect_dependencies(self, node, data, runtime, development):
        if self.__pipfile(node):
            r, d = parse_pipfile(data)
            runtime.extend(r)
            development.extend(d)
        elif self.__runtime_requirements_file(node):
            runtime.extend(
                parse_requirements_file(data, DependencyKind.RUNTIME))
        elif self.__development_requirements_file(node):
            development.extend(
                parse_requirements_file(data, DependencyKind.DEVELOPMENT))
        else:
            assert False, f'Unrecognized node: {node}'

    def __pipfile(self, node):
        return node.match(PIPFILE_PATTERN)

    def __development_requirements_file(self, node):
        return node.match_any(DEVELOPMENT_REQUIREMENTS_PATTERNS)

    def __runtime_requirements_file(self, node):
        return node.match_any(RUNTIME_REQUIREMENTS_PATTERNS)
