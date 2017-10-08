from app.platforms.jvm.maven_metadata import MavenMetadata
from app.platforms.jvm.maven_pom import MavenPom
from app.package_registry import PackageRegistry
from app.package_version import PackageVersion


METADATA_URI = 'https://repo.maven.apache.org/maven2/{group}/{artifact}/maven-metadata.xml'
POM_URI = 'https://repo.maven.apache.org/maven2/{group}/{artifact}/{number}/{artifact}-{number}.pom'


class Maven2PackageRegistry(PackageRegistry):

    def _fetch_version(self, name, number):
        response = self._session.get(self.__pom_uri(name, number))
        response.raise_for_status()
        pom = MavenPom.parse(response.text)
        return PackageVersion(
            name=name,
            number=number,
            licenses=self.__determine_licenses(pom),
            runtime_dependencies=pom.runtime_dependencies,
            development_dependencies=pom.development_dependencies
        )

    def _fetch_latest_version(self, name):
        response = self._session.get(self.__metadata_uri(name))
        response.raise_for_status()
        metadata = MavenMetadata.parse(response.text)
        return self._fetch_version(name, metadata.latest_version)

    def __metadata_uri(self, name):
        return METADATA_URI.format_map({
            'group': name.group_path,
            'artifact': name.artifact_id
        })

    def __pom_uri(self, name, number):
        return POM_URI.format_map({
            'group': name.group_path,
            'artifact': name.artifact_id,
            'number': number
        })

    def __determine_licenses(self, pom):
        if pom.licenses:
            return pom.licenses
        return self._find_licenses_in_code_repository_urls(pom.urls)
