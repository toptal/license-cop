from app.package_repository import *

GEMS_URI = 'https://rubygems.org/api/v1/gems/{0}.json'
VERSIONS_URI = 'https://rubygems.org/api/v1/versions/{0}.json'


class RubyPackageRepository(PackageRepository):

    def fetch_version(self, name, number):
        package_data = self.__fetch_package_data(name)
        if package_data is None:
            return None
        version_data = self.__fetch_version_data(name, number)
        if version_data is None:
            return None
        return self.__build_version(name, number, package_data, version_data)

    def fetch_latest_version(self, name):
        package_data = self.__fetch_package_data(name)
        if package_data is None:
            return None
        number = package_data['version']
        version_data = self.__fetch_version_data(name, number)
        return self.__build_version(name, number, package_data, version_data)

    def __fetch_package_data(self, name):
        response = self._session.get(GEMS_URI.format(name))
        if response.ok:
            return response.json()

    def __fetch_version_data(self, name, version):
        response = self._session.get(VERSIONS_URI.format(name))
        if response.ok:
            for data in response.json():
                if data['number'] == version:
                    return data

    def __extract_dependencies(self, data):
        dependencies = []
        dependencies.extend(data['dependencies']['development'])
        dependencies.extend(data['dependencies']['runtime'])
        return list(map(lambda i: Dependency(i['name']), dependencies))

    def __extract_licenses(self, data):
        licenses = data['licenses']
        if licenses is None:
            return []
        return licenses

    def __build_version(self, name, number, package_data, version_data):
        return PackageVersion(
            name,
            number,
            dependencies=self.__extract_dependencies(package_data),
            licenses=self.__extract_licenses(version_data)
        )
