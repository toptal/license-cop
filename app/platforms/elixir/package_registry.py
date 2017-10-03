from app.package_registry import *
from app.package_version import *
from app.dependency import *


LIB_URI = 'https://hex.pm/api/packages/{0}'
VERSION_URI = 'https://hex.pm/api/packages/{0}/releases/{1}'


class ElixirPackageRegistry(PackageRegistry):

    def _fetch_version(self, name, number):
        package_data = self.__fetch_package_data(name)
        version_data = self.__fetch_version_data(name, number)
        return self.__build_version(name, number, package_data, version_data)

    def _fetch_latest_version(self, name):
        package_data = self.__fetch_package_data(name)
        latest_version = package_data['releases'][0]['version']
        version_data = self.__fetch_version_data(name, latest_version)
        return self.__build_version(name, latest_version, package_data, version_data)

    def __fetch_package_data(self, name):
        response = self._session.get(LIB_URI.format(name))
        response.raise_for_status()
        return response.json()

    def __fetch_version_data(self, name, number):
        response = self._session.get(VERSION_URI.format(name, number))
        response.raise_for_status()
        return response.json()

    def __parse_dependencies(self, data, kind):
        return [
            Dependency(dep, kind)
            for dep in data.get('requirements', {}).keys()
        ]

    def __determine_licenses(self, package_data, version_data):
        licenses = package_data.get('meta', {}).get('licenses', [])
        if licenses:
            return licenses
        return self.__fetch_licenses(package_data)

    def __fetch_licenses(self, data):
        urls = [
            data.get('meta', {}).get('links', {}).get('GitHub')
        ]
        return self._find_licenses_in_code_repository_urls(filter(None, urls))

    def __build_version(self, name, number, package_data, version_data):
        return PackageVersion(
            name,
            number,
            licenses=self.__determine_licenses(package_data, version_data),
            runtime_dependencies=self.__parse_dependencies(version_data, DependencyKind.RUNTIME),
            development_dependencies=[]
        )
