import requests
from itertools import chain
from bs4 import BeautifulSoup, Tag


BASE_URL = 'https://mvnrepository.com/artifact/{group}/{artifact}/{number}'


class MvnRepository:

    def __init__(self, http_compression=True):
        self._session = requests.Session()
        if not http_compression:
            self._session.headers.update({'Accept-Encoding': 'identity'})

    def fetch_licenses(self, name, number):
        for artifact_id in name.artifact_id_variations:
            response = self.__get_page(name.group_id, artifact_id, number)
            if response.ok:
                licenses = self.__process_html(response.text)
                if licenses:
                    return licenses
            elif response.status_code != 404:
                response.raise_for_status()
        return []

    def __get_page(self, group_id, artifact_id, number):
        return self._session.get(BASE_URL.format_map({
            'group': group_id,
            'artifact': artifact_id,
            'number': number
        }))

    def __process_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        license_tag = soup.find('th', text='License')
        if license_tag:
            return self.__find_licenses(self.__sibling_tags(license_tag))

    @staticmethod
    def __find_licenses(tags):
        license_tags = chain.from_iterable(i.find_all('span', class_='b lic') for i in tags)
        return [i.text for i in license_tags]

    @staticmethod
    def __sibling_tags(tag):
        return (i for i in tag.next_siblings if isinstance(i, Tag))
