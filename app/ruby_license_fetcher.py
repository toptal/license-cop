from app.base_license_fetcher import BaseLicenseFetcher

VERSIONS_URI = 'https://rubygems.org/api/v1/versions/{0}.json'
GEMS_URI = 'https://rubygems.org/api/v1/gems/{0}.json'


class RubyLicenseFetcher(BaseLicenseFetcher):

    def fetch_licenses(self, name, number):
        info = self.__fetch_version_info(name, number)
        if info is not None:
            licenses = info['licenses']
            if licenses is None:
                return []
            return licenses

    def fetch_immediate_dependencies(self, name, number):
        response = self._session.get(GEMS_URI.format(name))
        if response.ok:
            data = response.json()
            dependencies = []
            dependencies.extend(data['dependencies']['development'])
            dependencies.extend(data['dependencies']['runtime'])
            return list(map(lambda i: i['name'], dependencies))

    def __fetch_version_info(self, name, number):
        response = self._session.get(VERSIONS_URI.format(name))
        if response.ok:
            for info in response.json():
                if info['number'] == number:
                    return info
