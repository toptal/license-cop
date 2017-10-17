import xmltodict


class MavenMetadata:

    def __init__(self, latest_version):
        self.latest_version = latest_version

    @classmethod
    def parse(cls, xml):
        data = xmltodict.parse(xml)
        metadata = data['metadata']
        return cls(
            latest_version=cls.__extract_latest_version(metadata)
        )

    @classmethod
    def __extract_latest_version(cls, data):
        block = data['versioning']
        if block.get('latest'):
            return block['latest']
        return max(cls.__extract_versions(block))

    @staticmethod
    def __extract_versions(data):
        value = data['versions']['version']
        if isinstance(value, list):
            return value
        return [value]
