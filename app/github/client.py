import re
import requests

from app.require_environment import *


TOKEN = require_environment('GITHUB_TOKEN')


URL_REGEX = re.compile(
    r'^((git[+:@])?((http:|https:)?//)?)?(www\.)?github\.com[:/]'
    r'(?P<owner>[\w\-]+)(/(?P<repo>[\w\-\.]+)/?(?P<path>#?.*))?'
)


def __remove_dot_git_suffix(path):
    if path:
        if path.endswith('.git'):
            return path[:-len('.git')]
        return path


def __cleanup(path):
    return path if path else None


def parse_github_url(url):
    match = URL_REGEX.match(url.lower())
    if match:
        owner = __cleanup(match.group('owner'))
        repo = __remove_dot_git_suffix(__cleanup(match.group('repo')))
        path = __cleanup(match.group('path'))
        return (owner, repo, path)


class GithubClient:
    def __init__(self, http_compression=True):
        self._session = requests.Session()
        self._session.headers.update({'Authorization': 'token {0}'.format(TOKEN)})
        if not http_compression:
            self._session.headers.update({'Accept-Encoding': 'identity'})
