import re

from app.data_object import DataObject


SCALA_VERSION_REGEX = re.compile(
    r'(_[A-Za-z0-9\.\-]+\.[A-Za-z0-9\.\-]+)$'
)


class JvmPackageName(DataObject):

    def __init__(self, group_id, artifact_id):
        self.group_id = group_id
        self.artifact_id = artifact_id

    def artifact_id_with_default_scala_version(self, scala_version):
        if SCALA_VERSION_REGEX.search(self.artifact_id):
            return self.artifact_id
        return '{0}_{1}'.format(self.artifact_id, scala_version)

    @property
    def group_path(self):
        return self.group_id.replace('.', '/')

    def __str__(self):
        return '{0}:{1}'.format(self.group_id, self.artifact_id)

    def __repr__(self):
        return str(self)
