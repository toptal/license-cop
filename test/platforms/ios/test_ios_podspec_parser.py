import pytest

from test import *
from app.platforms.ios.podspec_parser import PodspecParser


@pytest.fixture
def parser():
    return PodspecParser()


def test_parse_empty_file(parser):
    assert list(parser.parse('')) == []


def test_file_without_pods(parser):
    content = """
        Pod::Spec.new do |s|
            s.name = "Name"
            s.version = "1.0.1"
        end
    """
    assert list(parser.parse(content)) == []


def test_file_with_pods(parser):
    content = """
        Pod::Spec.new do |s|
            s.name = "Name"
            s.version = "1.0.1"
            s.dependency 'Dep1', '~> 1.2'
            s.ios.dependency 'Dep2', '~> 0.9'
            s.dependency 'Dep3'
        end
    """
    assert list(parser.parse(content)) == [
        'Dep1',
        'Dep2',
        'Dep3'
    ]
