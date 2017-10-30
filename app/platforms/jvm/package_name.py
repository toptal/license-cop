import re

from app.data_object import DataObject


SCALA_VERSION_REGEX = re.compile(r'_([A-Za-z0-9\.\-]+\.[A-Za-z0-9\.\-]+)$')


class JvmPackageName(DataObject):

    def __init__(self, group_id, artifact_id, scala_version=None):
        self.group_id = group_id
        self.artifact_id = self.__remove_scala_version(artifact_id)
        self.scala_version = self.__extract_scala_version(artifact_id, scala_version)

    @property
    def group_path(self):
        return self.group_id.replace('.', '/')

    @property
    def scala_version_without_patch(self):
        if self.scala_version:
            parts = self.scala_version.split('.')
            return f'{parts[0]}.{parts[1]}'

    @property
    def artifact_id_variations(self):
        if self.scala_version is None:
            return (self.artifact_id,)
        return (
            f'{self.artifact_id}_{self.scala_version}',
            f'{self.artifact_id}_{self.scala_version_without_patch}',
            self.artifact_id
        )

    @staticmethod
    def __extract_scala_version(artifact_id, default):
        m = SCALA_VERSION_REGEX.search(artifact_id)
        return m.group(1) if m else default

    @staticmethod
    def __remove_scala_version(artifact_id):
        return SCALA_VERSION_REGEX.sub('', artifact_id)

    def __str__(self):
        name = f'{self.group_id}:{self.artifact_id}'
        return f'{name}_{self.scala_version}' if self.scala_version else name

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
