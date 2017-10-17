import re

from app.data_object import DataObject


SCALA_VERSION_REGEX = re.compile(r'_([A-Za-z0-9\.\-]+\.[A-Za-z0-9\.\-]+)$')


class JvmPackageName(DataObject):

    def __init__(self, group_id, artifact_id, scala_version=None):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.__explicit_scala_version = scala_version
        self.__implicit_scala_version = self.__extract_scala_version(artifact_id)

    @property
    def artifact_id_with_scala_version(self):
        if self.__implicit_scala_version:
            return self.artifact_id
        if self.__explicit_scala_version:
            return f'{self.artifact_id}_{self.__explicit_scala_version}'
        return self.artifact_id

    @property
    def artifact_id_without_scala_version(self):
        return SCALA_VERSION_REGEX.sub('', self.artifact_id)

    @property
    def scala_version(self):
        if self.__implicit_scala_version:
            return self.__implicit_scala_version
        return self.__explicit_scala_version

    def __extract_scala_version(self, artifact_id):
        m = SCALA_VERSION_REGEX.search(artifact_id)
        if m:
            return m.group(1)

    @property
    def group_path(self):
        return self.group_id.replace('.', '/')

    def __str__(self):
        return f'{self.group_id}:{self.artifact_id_with_scala_version}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not other:
            return False
        return str(self).__eq__(str(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))
