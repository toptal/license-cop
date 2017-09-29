import json
import re
from pathlib import PurePosixPath
from configparser import ConfigParser

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *

RUNTIME_REQUIREMENT_FILES = ['requirements.txt']
DEVELOPMENT_REQUIREMENT_FILES = [
    'requirements.test.txt',
    'requirements-test.txt',
    'requirements_test.txt',
    'test-requirements.txt',
    'test.requirements.txt',
    'test_requirements.txt',
    'requirements.testing.txt',
    'requirements-testing.txt',
    'requirements_testing.txt',
    'testing-requirements.txt',
    'testing.requirements.txt',
    'testing_requirements.txt',
    'dev-requirements.txt',
    'dev.requirements.txt',
    'dev_requirements.txt',
    'requirements-dev.txt',
    'requirements.dev.txt',
    'requirements_dev.txt',
    'development-requirements.txt',
    'development.requirements.txt',
    'development_requirements.txt',
    'requirements-development.txt',
    'requirements.development.txt',
    'requirements_development.txt'
]


PATTERNS = [
    PackageDescriptorPattern.multiple_files(
        'requirements',
        RUNTIME_REQUIREMENT_FILES + DEVELOPMENT_REQUIREMENT_FILES
    ),
    PackageDescriptorPattern.one_file('pipfile', 'Pipfile')
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


def __parse_pipfile_section(parser, section, kind):
    return list(map(lambda i: Dependency(i, kind), parser[section].keys()))


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

    def _fetch_package_descriptor(self, repository, pattern_match):
        id = pattern_match.pattern_id
        if id == 'requirements':
            runtime, development = self.__from_requirements(repository, pattern_match)
        elif id == 'pipfile':
            runtime, development = self.__from_pipfile(repository, pattern_match)
        else:
            assert False, 'Unrecognized pattern ID: {0}'.format(id)

        return PackageDescriptor(
            platform='Python',
            repository=repository,
            paths=pattern_match.paths,
            runtime_dependencies=runtime,
            development_dependencies=development
        )

    def __from_requirements(self, repository, pattern_match):
        runtime = []
        development = []
        for path in pattern_match.paths:
            name = self.__filename(path)
            data = repository.read_text_file(path)
            if name in RUNTIME_REQUIREMENT_FILES:
                runtime.extend(parse_requirements_file(data, DependencyKind.RUNTIME))
            elif name in DEVELOPMENT_REQUIREMENT_FILES:
                development.extend(parse_requirements_file(data, DependencyKind.DEVELOPMENT))
        return (runtime, development)

    def __from_pipfile(self, repository, pattern_match):
        assert len(pattern_match.paths) == 1
        data = repository.read_text_file(pattern_match.paths[0])
        return parse_pipfile(data)

    def __filename(self, path):
        return PurePosixPath(path).name.lower()
