import sys
import requests
from abc import *

from app.data_object import *
from app.github.repository import *


class PackageVersionNotFoundError(Exception):
    pass


class PackageRegistry(ABC):

    class __Id(DataObject):
        def __init__(self, name, number=None):
            self.name = name
            self.number = number

        def __iter__(self):
            data = (self.name, ) if self.number is None\
                                 else (self.name, self.number)
            return data.__iter__()

        def __str__(self):
            return '{0}:{1}'.format(
                self.name,
                'latest' if self.number is None else self.number
            )

    def __init__(self, http_compression=True):
        self._session = requests.Session()
        if not http_compression:
            self._session.headers.update({'Accept-Encoding': 'identity'})
        self._http_compression = http_compression
        self.__cache = {}

    @abstractmethod
    def _fetch_version(self, name, number):
        pass

    @abstractmethod
    def _fetch_latest_version(self, name):
        pass

    def fetch_version(self, name, number):
        id = self.__Id(name, number)
        return self.__cached_fetch(id, self._fetch_version)

    def fetch_latest_version(self, name):
        id = self.__Id(name)
        return self.__cached_fetch(id, self._fetch_latest_version)

    def __cached_fetch(self, id, fetch_function):
        if id in self.__cache:
            return self.__cache[id]
        return self.__cache_miss(id, fetch_function)

    def __cache_miss(self, id, fetch_function):
        try:
            self.__report_progress('  → {0}'.format(id))
            version = fetch_function(*id)
            self.__cache[id] = version
            return version
        except requests.exceptions.HTTPError as e:
            raise PackageVersionNotFoundError('Could not find package version {0}. {1}'.format(id, e))

    def __report_progress(self, message):
        sys.stdout.write('\033[K')
        print(message)
        sys.stdout.write('\033[F')
        sys.stdout.flush()

    def _find_licenses_in_code_repository_urls(self, urls):
        for url in urls:
            try:
                license = self.__fetch_license(url)
                if license:
                    return [license]
            except requests.exceptions.HTTPError as e:
                continue
        return []

    # Right now, only GitHub is supported, but this could be extended
    # to support BitBucket or other platforms.
    def __fetch_license(self, url):
        if url:
            repository = self.__github_repository(url)
            if repository:
                return repository.license()

    def __github_repository(self, url):
        return GithubRepository.from_url(
            url, http_compression=self._http_compression)
