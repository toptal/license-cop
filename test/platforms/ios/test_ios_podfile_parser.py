import pytest

from test import *
from app.platforms.ios.podfile_parser import PodfileParser


@pytest.fixture
def parser():
    return PodfileParser()


def test_parse_empty_file(parser):
    assert list(parser.parse('')) == []


def test_file_without_pods(parser):
    content = '''
        project :name
        target :hello do
        end
    '''
    assert list(parser.parse(content)) == []


def test_file_with_pods(parser):
    content = '''
        project :name
        pod 'Pod1'
        pod 'Pod2/SubPod'
        pod 'Pod3', :options => []
        target :hello do
            pod 'Pod4'
        end
    '''
    assert list(parser.parse(content)) == [
        'Pod1',
        'Pod2',
        'Pod3',
        'Pod4'
    ]
