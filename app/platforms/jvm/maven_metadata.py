import xmltodict


class MavenMetadata:

    def __init__(self, latest_version):
        self.latest_version = latest_version

    @classmethod
    def parse(cls, xml):
        data = xmltodict.parse(xml)
        metadata = data['metadata']
        return cls(
            latest_version=metadata['versioning']['latest']
        )
