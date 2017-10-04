import re

from app.package_registry import *
from app.package_version import *
from app.dependency import *


POD_URI = 'https://cocoapods.org/pods/{0}'
VERSIONS_URI = 'https://rubygems.org/api/v1/versions/{0}.json'
PODSPEC_URL_REGEX = re.compile(r"<a\s+href=\"([^\"]+?)\"\s*>\s*See Podspec\s*<\/a>", re.S)


class IosPackageRegistry(PackageRegistry):

    def _fetch_version(self, name, number):
        raise RuntimeError('Fetching the specific version for CocoaPods is not supported yet.')

    def _fetch_latest_version(self, name):
        raw_github_path = self.__determine_podspec_url(name)
        podspec = self.__get_podspec(raw_github_path)
        return self.__build_version(name, podspec)

    def __get_cocoapod_page(self, name):
        response = self._session.get(POD_URI.format(name))
        response.raise_for_status()
        return response.text

    def __get_podspec(self, url):
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def __determine_podspec_url(self, name):
        page = self.__get_cocoapod_page(name)
        github_path = PODSPEC_URL_REGEX.search(page).group(1)
        return github_path.replace('github.com', 'raw.githubusercontent.com').replace('blob/', '')

    def __parse_dependencies(self, package_data, kind):
        return [
            Dependency(name, kind)
            for name in package_data.get('dependencies', {}).keys()
        ]

    def __determine_licenses(self, package_data):
        license = package_data.get('license')
        if isinstance(license, dict):
            return [license.get('type').strip()]
        if isinstance(license, str):
            return [license]
        return self.__fetch_licenses(package_data)

    def __fetch_licenses(self, package_data):
        urls = [
            package_data.get('source', {}).get('git')
        ]
        return self._find_licenses_in_code_repository_urls(filter(None, urls))

    def __build_version(self, name, package_data):
        return PackageVersion(
            name,
            package_data['version'],
            licenses=self.__determine_licenses(package_data),
            runtime_dependencies=self.__parse_dependencies(package_data, DependencyKind.RUNTIME),
            development_dependencies=[]
        )
