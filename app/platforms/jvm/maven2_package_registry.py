from app.platforms.jvm.maven_metadata import MavenMetadata
from app.platforms.jvm.maven_pom import MavenPom
from app.package_registry import PackageRegistry
from app.package_version import PackageVersion


METADATA_URL = 'https://repo.maven.apache.org/maven2/{group}/{artifact}/maven-metadata.xml'
POM_URL = 'https://repo.maven.apache.org/maven2/{group}/{artifact}/{number}/{artifact}-{number}.pom'


SCALA_VERSION = '2.11'


class Maven2PackageRegistry(PackageRegistry):

    def _fetch_version(self, name, number):
        pom = self.__fetch_pom(name, number)
        return PackageVersion(
            name=name,
            number=number,
            licenses=self.__determine_licenses(pom),
            runtime_dependencies=pom.runtime_dependencies,
            development_dependencies=pom.development_dependencies
        )

    def _fetch_latest_version(self, name):
        metadata = self.__fetch_metadata(name)
        return self._fetch_version(name, metadata.latest_version)

    def __fetch_metadata(self, name):
        response = self.__http_get_metadata(name.group_path, name.artifact_id)
        if response.status_code == 404:
            artifact_id = name.artifact_id_with_default_scala_version(SCALA_VERSION)
            response = self.__http_get_metadata(name.group_path, artifact_id)
            response.raise_for_status()
        return MavenMetadata.parse(response.text)

    def __http_get_metadata(self, group_path, artifact_id):
        url = METADATA_URL.format_map({
            'group': group_path,
            'artifact': artifact_id
        })
        return self._session.get(url)

    def __fetch_pom(self, name, number):
        response = self.__http_get_pom(name.group_path, name.artifact_id, number)
        if response.status_code == 404:
            artifact_id = name.artifact_id_with_default_scala_version(SCALA_VERSION)
            response = self.__http_get_pom(name.group_path, artifact_id, number)
            response.raise_for_status()
        return MavenPom.parse(response.text)

    def __http_get_pom(self, group_path, artifact_id, number):
        url = POM_URL.format_map({
            'group': group_path,
            'artifact': artifact_id,
            'number': number
        })
        return self._session.get(url)

    def __determine_licenses(self, pom):
        if pom.licenses:
            return pom.licenses
        return self._find_licenses_in_code_repository_urls(pom.urls)
