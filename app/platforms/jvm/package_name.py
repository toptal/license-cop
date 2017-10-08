from app.data_object import DataObject


class JvmPackageName(DataObject):

    def __init__(self, group_id, artifact_id):
        self.group_id = group_id
        self.artifact_id = artifact_id

    @property
    def group_path(self):
        return self.group_id.replace('.', '/')

    def __str__(self):
        return '{0}:{1}'.format(self.group_id, self.artifact_id)

    def __repr__(self):
        return str(self)
