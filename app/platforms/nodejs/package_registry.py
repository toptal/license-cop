from app.package_registry import *

from app.package_version import *
from app.dependency import *
from app.platforms.nodejs.shared import parse_dependencies


VERSION_URI = 'http://registry.npmjs.org/{0}/{1}'
PACKAGE_URI = 'http://registry.npmjs.org/{0}'


class NodejsPackageRegistry(PackageRegistry):

    def _fetch_version(self, name, number):
        response = self._session.get(VERSION_URI.format(name, number))
        response.raise_for_status()
        version_data = response.json()
        return self.__build_version(version_data)

    def _fetch_latest_version(self, name):
        response = self._session.get(PACKAGE_URI.format(name))
        response.raise_for_status()
        package_data = response.json()
        number = package_data['dist-tags']['latest']
        version_data = package_data['versions'][number]
        return self.__build_version(version_data)

    def __build_version(self, data):
        return PackageVersion(
            name=data['name'],
            number=data['version'],
            licenses=self.__extract_licenses(data),
            runtime_dependencies=parse_dependencies(data, Dependency.RUNTIME),
            development_dependencies=parse_dependencies(data, Dependency.DEVELOPMENT),
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
