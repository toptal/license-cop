from app.base_license_fetcher import BaseLicenseFetcher

GET_VERSIONS_URI = 'https://rubygems.org/api/v1/versions/{0}.json'


class RubyLicenseFetcher(BaseLicenseFetcher):

    def fetch_licenses(self, name, number):
        version = self.__fetch_version(name, number)
        if version is not None:
            licenses = version['licenses']
            if licenses is None:
                return []
            return licenses

    def __fetch_version(self, name, number):
        response = self._session.get(GET_VERSIONS_URI.format(name))
        if response.ok:
            for version in response.json():
                if version['number'] == number:
                    return version
