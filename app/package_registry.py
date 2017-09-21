import requests
from abc import *

from app.github_repository import *


class PackageRegistry(ABC):
    def __init__(self, http_compression=True):
        self._session = requests.Session()
        if not http_compression:
            self._session.headers.update({'Accept-Encoding': 'identity'})
        self._http_compression = http_compression

    @abstractmethod
    def fetch_version(self, name, number):
        pass

    @abstractmethod
    def fetch_latest_version(self, name):
        pass

    def _search_licenses_in_code_repository_urls(self, urls):
        for url in urls:
            licenses = self.__fetch_licenses(url)
            if licenses:
                return licenses
        return []

    # Right now, only GitHub is supported, but this could be extended
    # to support BitBucket or other platforms.
    def __fetch_licenses(self, url):
        if url:
            repository = self.__github_repository(url)
            if repository:
                return [repository.license]

    def __github_repository(self, url):
        return GithubRepository.from_url(
            url, http_compression=self._http_compression)
