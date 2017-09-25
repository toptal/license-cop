import os
import re
import requests
import base64
from urllib.parse import urlparse, urljoin

from app.require_environment import *


USER_REPOSITORY_URI = 'https://github.com/{0}/{1}'
API_REPOSITORY_URI = 'https://api.github.com/repos/{0}/{1}'
API_CONTENTS_URI = 'https://api.github.com/repos/{0}/{1}/contents/{2}'

# The Licenses API is currently available for developers to preview.
# During the preview period, the API may change without advance notice.
# To access the API during the preview period, you must provide a custom
# media type in the Accept header
PREVIEW_MEDIA_TYPE = 'application/vnd.github.drax-preview+json'


TOKEN = require_environment('GITHUB_TOKEN')
URL_REGEX = '^((git[+:@])?((http:|https:)?//)?)?(www\.)?github.com[:/](?P<owner>[\w\-\.]+)/(?P<name>[\w\-\.]+)'


class GithubRepository:

    def __init__(self, owner, name, token=TOKEN, http_compression=True):
        self.__session = requests.Session()
        self.__session.headers.update({'Authorization': 'token {0}'.format(token)})
        if not http_compression:
            self.__session.headers.update({'Accept-Encoding': 'identity'})

        self.owner = owner
        self.name = name

    @staticmethod
    def from_url(url, token=TOKEN, http_compression=True):
        url = url.lower()
        path = re.match(URL_REGEX, url)
        if path:
            return GithubRepository(
                path.group('owner'),
                GithubRepository.__remove_dot_git_suffix(path.group('name')),
                token,
                http_compression
            )

    @staticmethod
    def __remove_dot_git_suffix(name):
        if name.endswith('.git'):
            return name[:-len('.git')]
        return name

    def path_exists(self, path):
        response = self.__session.head(self.__contents_uri(path))
        if response.ok:
            return True
        elif response.status_code == 404:
            return False
        response.raise_for_status()

    def read_text_file(self, path):
        response = self.__session.get(self.__contents_uri(path))
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) or data['type'] != 'file':
            raise Exception('Path "{0}" is not a file.'.format(path))
        return self.__decode_text_from_base64(data['content'])

    def license(self):
        response = self.__session.get(
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

    def __contents_uri(self, path):
        return API_CONTENTS_URI.format(self.owner, self.name, path)

    def __repository_uri(self):
        return API_REPOSITORY_URI.format(self.owner, self.name)

    def __str__(self):
        return USER_REPOSITORY_URI.format(self.owner, self.name)
