import xmltodict

from app.platforms.jvm.package_name import JvmPackageName
from app.platforms.jvm.maven_dependency import MavenDependency


class MavenPom:

    def __init__(self,
                 group_id,
                 artifact_id,
                 version,
                 parent,
                 properties,
                 dependencies=[],
                 licenses=[],
                 urls=[]):

        self.__group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.parent = parent
        self.__properties = properties
        self.dependencies = dependencies
        self.licenses = licenses
        self.urls = urls

    @property
    def group_id(self):
        if self.__group_id:
            return self.__group_id
        return self.parent.group_id

    @property
    def properties(self):
        if self.parent:
            self.__properties.update(self.parent.properties)
        return self.__properties

    def get_property(self, name):
        builtin = self.__get_builtin_property(name)
        if builtin:
            return builtin
        return self.properties.get(name)

    def __get_builtin_property(self, name):
        parts = name.split('.')
        if parts[0] in ('project', 'pom'):
            if len(parts) > 1:
                if parts[1] == 'parent':
                    if len(parts) > 2 and self.parent:
                        return self.__extract_builtin_property(parts[2], self.parent)
                return self.__extract_builtin_property(parts[1], self)

    def __extract_builtin_property(self, part, pom):
        if part == 'groupId':
            return pom.group_id
        if part == 'artifactId':
            return pom.artifact_id
        if part == 'version':
            return pom.version

    def filter_dependencies(self, kind):
        return (i for i in self.dependencies if i.kind == kind)

    @classmethod
    def parse(cls, xml, registry):
        xml = cls.__clean_xml(xml)
        data = xmltodict.parse(xml)['project']
        return cls.__build(data, registry)

    @classmethod
    def __build(cls, data, registry):
        parent = cls.__fetch_parent(data, registry)
        properties = cls.__extract_properties(data, parent)
        return cls(
            group_id=data.get('groupId'),
            artifact_id=data.get('artifactId'),
            version=data.get('version'),
            parent=parent,
            properties=properties,
            dependencies=cls.__extract_dependencies(data, properties),
            licenses=cls.__extract_licenses(data),
            urls=cls.__extract_urls(data)
        )

    @classmethod
    def __fetch_parent(cls, data, registry):
        block = data.get('parent')
        if block:
            name = JvmPackageName(block['groupId'], block['artifactId'])
            version = block['version']
            return registry.get_pom(name, version)

    @staticmethod
    def __extract_properties(data, parent):
        block = data.get('properties')
        return dict(block) if block else {}

    @classmethod
    def __extract_dependencies(cls, data, properties):
        if not data.get('dependencies'):
            return []
        block = data['dependencies']['dependency']
        if isinstance(block, list):
            return [cls.__extract_dependency(i) for i in block]
        else:
            return [cls.__extract_dependency(block)]

    @staticmethod
    def __extract_dependency(data):
        return MavenDependency(data['groupId'], data['artifactId'], data.get('scope'))

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
            return data if isinstance(data, str) else data.get('name')

    @staticmethod
    def __extract_urls(data):
        urls = [data.get('url')]
        if data.get('scm') and 'url' in data['scm']:
            urls.append(data['scm'].get('url'))
        return set(filter(None, urls))

    @classmethod
    def __clean_xml(cls, xml):
        xml = cls.__trim_invalid_characters(xml)
        return xml.replace('&', '')

    @staticmethod
    def __trim_invalid_characters(xml):
        pos = xml.find('<')
        return xml[max(0, pos):]
