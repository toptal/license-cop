import re

from app.package_registry import *
from app.package_version import *
from app.dependency import *
from app.platforms.nodejs.shared import parse_dependencies


VERSION_URI = 'http://registry.npmjs.org/{0}/{1}'
PACKAGE_URI = 'http://registry.npmjs.org/{0}'

SCOPED_PACKAGE_REGEX = '@[\w\-\.]+/[\w\-\.]+'


class NodejsPackageRegistry(PackageRegistry):

    def _fetch_version(self, name, number):
        # There's a bug in the Node.js registry API that prevents
        # regular (and much more efficient) queries to be performed
        # for scoped package names (ex: @foo/bar). Hence, we need to
        # implement a workaround here.
        # Please refer to: https://github.com/npm/registry/issues/34
        if self.__scoped_package(name):
            return self.__fetch_version_for_scoped_package(name, number)
        version_data = self.__fetch_version_data(name, number)
        return self.__build_version(version_data)

    def _fetch_latest_version(self, name):
        return self._fetch_version(name, 'latest')

    def __fetch_version_for_scoped_package(self, name, number):
        package_data = self.__fetch_package_data(name)
        version_data = self.__extract_version_data(package_data, name, number)
        return self.__build_version(version_data)

    def __fetch_version_data(self, name, number):
        response = self._session.get(VERSION_URI.format(name, number))
        response.raise_for_status()
        return response.json()

    def __extract_version_data(self, package_data, name, number):
        if number == 'latest':
            number = package_data['dist-tags']['latest']
        if number in package_data['versions']:
            return package_data['versions'][number]
        raise PackageVersionNotFound(
            'Could not find package version {0}:{1}.'.format(name, number))

    def __fetch_package_data(self, name):
        name = self.__normalize_scoped_package_name(name)
        response = self._session.get(PACKAGE_URI.format(name))
        response.raise_for_status()
        return response.json()

    def __scoped_package(self, name):
        return re.match(SCOPED_PACKAGE_REGEX, name) is not None

    def __normalize_scoped_package_name(self, name):
        return name.replace('/', '%2F')

    def __build_version(self, data):
        return PackageVersion(
            name=data['name'],
            number=data['version'],
            licenses=self.__extract_licenses(data),
            runtime_dependencies=parse_dependencies(data, DependencyKind.RUNTIME),
            development_dependencies=parse_dependencies(data, DependencyKind.DEVELOPMENT),
        )

    def __extract_licenses(self, data):
        if 'license' in data:
            return [data['license']]
        else:
            urls = []
            if 'repository' in data:
                urls.append(data['repository']['url'])
            if 'homepage' in data:
                urls.append(data['homepage'])
            return self._find_licenses_in_code_repository_urls(urls)
