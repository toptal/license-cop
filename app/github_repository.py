import os
import requests
import base64

from app.require_environment import *


CONTENTS_URI = 'https://api.github.com/repos/{0}/{1}/contents/{2}'


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

    def __contents_uri(self, path):
        return CONTENTS_URI.format(self.__owner, self.__name, path)

    def __decode_text_from_base64(self, encoded):
        return base64.b64decode(encoded).decode('utf-8')
