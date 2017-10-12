import re

from app.data_object import DataObject
from app.platforms.jvm.package_name import JvmPackageName
from app.dependency import Dependency, DependencyKind


INTERPOLATION_REGEX = re.compile(r'\$\{([\w\.\-]+)\}')


class MavenDependency(DataObject):

    def __init__(self, group_id, artifact_id, scope=None):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.scope = scope

    def __interpolate(self, text, pom):
        def replace(match):
            value = pom.get_property(match.group(1))
            return value if value else match.group(0)
        return INTERPOLATION_REGEX.sub(replace, text)

    @property
    def kind(self):
        if self.scope == 'test':
            return DependencyKind.DEVELOPMENT
        return DependencyKind.RUNTIME

    def to_dependency(self, pom):
        group_id = self.__interpolate(self.group_id, pom)
        artifact_id = self.__interpolate(self.artifact_id, pom)
        return Dependency(JvmPackageName(group_id, artifact_id), self.kind)
