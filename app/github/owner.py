from app.github.client import *
from app.github.repository import *


ORGANIZATION_URI = 'https://github.com/{0}'
API_ORGANIZATION_REPOSITORIES_URI = 'https://api.github.com/orgs/{0}/repos'


class GithubOwner(GithubClient):

    def __init__(self, name, http_compression=True):
        super().__init__(http_compression)
        self.name = name

    @staticmethod
    def from_url(url, http_compression=True):
        parsed = parse_github_url(url)
        if parsed:
            (owner, repo, _) = parsed
            if owner and not repo:
                return GithubOwner(owner, http_compression)

    # We only support GitHub organizations at the moment.
    # This query will not work for regular users.
    def repositories(self):
        return self.__fetch_organization_repositories()

    def __fetch_organization_repositories(self):
        link = API_ORGANIZATION_REPOSITORIES_URI.format(self.name)
        repos = []
        while True:
            response = self._session.get(link)
            response.raise_for_status()
            repos.extend(self.__build_repositories(response.json()))
            if 'next' not in response.links:
                break
            link = response.links['next']['url']
        return repos

    def __build_repositories(self, data):
        return map(
            lambda i: GithubRepository(self.name, i['name']),
            data
        )

    def __str__(self):
        return ORGANIZATION_URI.format(self.name)

    def __repr__(self):
        return f'GitHub organization {str(self)}'
