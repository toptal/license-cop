import os
import requests
import base64

from app.require_environment import *


REPOSITORY_URI = 'https://api.github.com/repos/{0}/{1}'
CONTENTS_URI = 'https://api.github.com/repos/{0}/{1}/contents/{2}'

# The Licenses API is currently available for developers to preview.
# During the preview period, the API may change without advance notice.
# To access the API during the preview period, you must provide a custom
# media type in the Accept header
PREVIEW_MEDIA_TYPE = 'application/vnd.github.drax-preview+json'


class GithubRepository:

    def __init__(self, owner, name,
                 token=require_environment('GITHUB_TOKEN'),
                 http_compression=True):
        self.__session = requests.Session()
        self.__session.headers.update({'Authorization': 'token {0}'.format(token)})
        if not http_compression:
            self.__session.headers.update({'Accept-Encoding': 'identity'})

        self.__owner = owner
        self.__name = name

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

    @property
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
        return CONTENTS_URI.format(self.__owner, self.__name, path)

    def __repository_uri(self):
        return REPOSITORY_URI.format(self.__owner, self.__name)
