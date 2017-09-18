from app.package_repository import PackageRepository, Dependency, Package

VERSIONS_URI = 'https://rubygems.org/api/v1/versions/{0}.json'
GEMS_URI = 'https://rubygems.org/api/v1/gems/{0}.json'


class RubyPackageRepository(PackageRepository):

    def fetch_package(self, name, version):
        data = self.__fetch_data(name, version)
        if data is None:
            return None
        licenses = self.__extract_licenses(data)
        dependencies = self.__fetch_dependencies(name, version)
        return Package(name, version, dependencies, licenses)

    def __extract_licenses(self, data):
        licenses = data['licenses']
        if licenses is None:
            return []
        return licenses

    def __fetch_dependencies(self, name, version):
        response = self._session.get(GEMS_URI.format(name))
        response.raise_for_status()
        data = response.json()
        dependencies = []
        dependencies.extend(data['dependencies']['development'])
        dependencies.extend(data['dependencies']['runtime'])
        return list(map(lambda i: Dependency(i['name']), dependencies))

    def __fetch_data(self, name, version):
        response = self._session.get(VERSIONS_URI.format(name))
        if response.ok:
            for data in response.json():
                if data['number'] == version:
                    return data
