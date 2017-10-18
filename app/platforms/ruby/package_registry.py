from app.package_registry import *
from app.package_version import *
from app.dependency import *


GEMS_URI = 'https://rubygems.org/api/v1/gems/{0}.json'
VERSIONS_URI = 'https://rubygems.org/api/v1/versions/{0}.json'


class RubyPackageRegistry(PackageRegistry):

    def _fetch_version(self, name, number):
        package_data = self.__fetch_package_data(name)
        version_data = self.__fetch_version_data(name, number)
        return self.__build_version(name, number, package_data, version_data)

    def _fetch_latest_version(self, name):
        package_data = self.__fetch_package_data(name)
        number = package_data['version']
        version_data = self.__fetch_version_data(name, number)
        return self.__build_version(name, number, package_data, version_data)

    def __fetch_package_data(self, name):
        response = self._session.get(GEMS_URI.format(name))
        response.raise_for_status()
        return response.json()

    def __fetch_version_data(self, name, number):
        response = self._session.get(VERSIONS_URI.format(name))
        response.raise_for_status()
        for data in response.json():
            if data['number'] == number:
                return data
        raise PackageVersionNotFoundError(f'Could not find package version {name}:{number}.')

    def __parse_dependencies(self, data, kind):
        return list(map(
            lambda i: Dependency(i['name'], kind),
            data['dependencies'][
                'runtime' if kind == DependencyKind.RUNTIME else 'development'
            ]
        ))

    def __determine_licenses(self, package_data, version_data):
        licenses = self.__extract_licenses(version_data)
        if licenses:
            return licenses
        return self.__fetch_licenses(package_data)

    def __extract_licenses(self, data):
        licenses = data['licenses']
        if licenses is None:
            return []
        return licenses

    def __fetch_licenses(self, data):
        urls = [
            data['source_code_uri'],
            data['homepage_uri'],
            data['project_uri']
        ]
        return self._find_licenses_in_code_repository_urls(filter(None, urls))

    def __build_version(self, name, number, package_data, version_data):
        return PackageVersion(
            name,
            number,
            licenses=self.__determine_licenses(package_data, version_data),
            runtime_dependencies=self.__parse_dependencies(package_data, DependencyKind.RUNTIME),
            development_dependencies=self.__parse_dependencies(package_data, DependencyKind.DEVELOPMENT)
        )
