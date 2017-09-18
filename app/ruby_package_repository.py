from app.package_repository import *

VERSIONS_URI = 'https://rubygems.org/api/v1/versions/{0}.json'
GEMS_URI = 'https://rubygems.org/api/v1/gems/{0}.json'


class RubyPackageRepository(PackageRepository):

    def fetch_licenses(self, package_name, package_number):
        info = self.__fetch_version_info(package_name, package_number)
        if info is not None:
            licenses = info['licenses']
            if licenses is None:
                return []
            return licenses

    def fetch_immediate_dependencies(self, package_name, package_number):
        response = self._session.get(GEMS_URI.format(package_name))
        if response.ok:
            data = response.json()
            dependencies = []
            dependencies.extend(data['dependencies']['development'])
            dependencies.extend(data['dependencies']['runtime'])
            return list(map(lambda i: i['name'], dependencies))

    def __fetch_version_info(self, package_name, package_number):
        response = self._session.get(VERSIONS_URI.format(package_name))
        if response.ok:
            for info in response.json():
                if info['number'] == package_number:
                    return info
