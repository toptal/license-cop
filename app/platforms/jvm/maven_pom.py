import xmltodict

from app.dependency import Dependency, DependencyKind
from app.platforms.jvm.package_name import JvmPackageName


class MavenPom:

    def __init__(self,
                 group_id,
                 artifact_id,
                 runtime_dependencies,
                 development_dependencies,
                 licenses,
                 urls):

        self.group_id = group_id
        self.artifact_id = artifact_id
        self.runtime_dependencies = runtime_dependencies
        self.development_dependencies = development_dependencies
        self.licenses = licenses
        self.urls = urls

    @classmethod
    def parse(cls, xml):
        xml = cls.__trim_invalid_characters(xml)
        data = xmltodict.parse(xml)
        project = data['project']
        dependencies = cls.__extract_dependencies(project)
        return cls(
            group_id=project.get('groupId'),
            artifact_id=project.get('artifactId'),
            runtime_dependencies=list(filter(lambda i: i.is_runtime, dependencies)),
            development_dependencies=list(filter(lambda i: i.is_development, dependencies)),
            licenses=cls.__extract_licenses(project),
            urls=cls.__extract_urls(project)
        )

    @classmethod
    def __extract_dependencies(cls, data):
        if not data.get('dependencies'):
            return []
        block = data['dependencies']['dependency']
        if isinstance(block, list):
            return [cls.__extract_dependency(i) for i in block]
        else:
            return [cls.__extract_dependency(block)]

    @classmethod
    def __extract_dependency(cls, data):
        return Dependency(
            JvmPackageName(data['groupId'], data['artifactId']),
            cls.__dependency_kind_from(data.get('scope'))
        )

    @staticmethod
    def __dependency_kind_from(data):
        if data and data.strip() == 'test':
            return DependencyKind.DEVELOPMENT
        return DependencyKind.RUNTIME

    @classmethod
    def __extract_licenses(cls, data):
        if not data.get('licenses'):
            return []
        block = data['licenses']['license']
        if isinstance(block, list):
            return list(filter(None, [cls.__extract_license(i) for i in block]))
        else:
            return list(filter(None, [cls.__extract_license(block)]))

    @staticmethod
    def __extract_license(data):
        if data:
            if isinstance(data, str):
                return data
            return data.get('name')

    @staticmethod
    def __extract_urls(data):
        urls = list()
        urls.append(data.get('url'))
        if data.get('scm') and 'url' in data['scm']:
            urls.append(data['scm'].get('url'))
        return set(filter(None, urls))

    @staticmethod
    def __trim_invalid_characters(xml):
        trim_index = 0
        for i, char in enumerate(xml):
            if char == '<':
                trim_index = i
                break
        return xml[trim_index:]
