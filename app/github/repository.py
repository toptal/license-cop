import base64

from app.github.client import *
from app.github.git_node import *


REPOSITORY_URI = 'https://github.com/{0}/{1}'
API_REPOSITORY_URI = 'https://api.github.com/repos/{0}/{1}'
API_CONTENTS_URI = 'https://api.github.com/repos/{0}/{1}/contents/{2}'
RECURSIVE_TREE_URI = 'https://api.github.com/repos/{0}/{1}/git/trees/{2}?recursive=1'

# The Licenses API is currently available for developers to preview.
# During the preview period, the API may change without advance notice.
# To access the API during the preview period, you must provide a custom
# media type in the Accept header
PREVIEW_MEDIA_TYPE = 'application/vnd.github.drax-preview+json'


class GithubRepository(GithubClient):

    def __init__(self, owner, name, http_compression=True):
        super().__init__(http_compression)
        self.owner = owner
        self.name = name

    @staticmethod
    def from_url(url, http_compression=True):
        parsed = parse_github_url(url)
        if parsed:
            (owner, repo, _) = parsed
            if owner and repo:
                return GithubRepository(
                    owner,
                    repo,
                    http_compression
                )

    def path_exists(self, path):
        response = self._session.head(self.__contents_uri(path))
        if response.ok:
            return True
        elif response.status_code == 404:
            return False
        response.raise_for_status()

    def read_text_file(self, path):
        response = self._session.get(self.__contents_uri(path))
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) or data['type'] != 'file':
            raise Exception('Path "{0}" is not a file.'.format(path))
        return self.__decode_text_from_base64(data['content'])

    def fetch_tree(self, sha='master'):
        response = self._session.get(self.__recursive_tree_uri(sha))
        response.raise_for_status()
        data = response.json()
        return self.__build_tree(data)

    def __build_tree(self, data):
        tree = GitNode.root()
        for node in data['tree']:
            type = node['type']
            path = node['path']
            if type == 'tree':
                tree.add_tree(path)
            elif type == 'blob':
                tree.add_blob(path)
            else:
                raise NotImplementedError(
                    'GitHub path {0} has an unsupported type: {1}'.format(path, type))
        return tree

    def license(self):
        response = self._session.get(
            self.__repository_uri(),
            headers={'Accept': PREVIEW_MEDIA_TYPE}
        )
        response.raise_for_status()
        return self.__extract_license(response.json())

    def __decode_text_from_base64(self, encoded):
        return base64.b64decode(encoded).decode('utf-8')

    def __extract_license(self, data):
        license = data['license']
        return license['spdx_id'] if license else None

    def __repository_uri(self):
        return API_REPOSITORY_URI.format(self.owner, self.name)

    def __contents_uri(self, path):
        return API_CONTENTS_URI.format(self.owner, self.name, path)

    def __recursive_tree_uri(self, sha):
        return RECURSIVE_TREE_URI.format(self.owner, self.name, sha)

    def __str__(self):
        return REPOSITORY_URI.format(self.owner, self.name)

    def __repr__(self):
        return "GitHub repository {0}".format(str(self))
