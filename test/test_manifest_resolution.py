import pytest
from textwrap import dedent

from app.package_version import *
from app.dependency import *
from app.dependency_resolution import *
from app.manifest import *
from app.manifest_resolution import *
from app.github.repository import *


@pytest.fixture
def repository():
    return GithubRepository.from_url('https://github.com/rails/rails')


@pytest.fixture
def manifest(repository):
    return Manifest(
        'Ruby',
        repository,
        ['Gemfile'],
        runtime_dependencies=[
            Dependency.runtime('activesupport'),
            Dependency.runtime('activemodel'),
            Dependency.runtime('activerecord'),
            Dependency.runtime('builder'),
            Dependency.runtime('erubi')
        ],
        development_dependencies=[
            Dependency.development('actionpack'),
            Dependency.development('activemodel')
        ]
    )


def version(name, number='5.1.4', licenses=['MIT']):
    return PackageVersion(
        name=name,
        number=number,
        licenses=licenses,
        runtime_dependencies=[
            Dependency.runtime('activesupport'),
            Dependency.runtime('activemodel'),
            Dependency.runtime('activerecord'),
            Dependency.runtime('builder'),
            Dependency.runtime('erubi')
        ],
        development_dependencies=[
            Dependency.development('actionpack'),
            Dependency.development('activemodel')
        ]
    )


def runtime_node(name, number, licenses, hidden=False):
    return DependencyResolution.runtime(version(name, number, licenses), hidden)


def development_node(name, number, licenses, hidden=False):
    return DependencyResolution.development(version(name, number, licenses), hidden)


def runtime_resolution():
    return (
        runtime_node('rails', '5.1.4', ['MIT'])
        .add_child(
            runtime_node('activesupport', '5.1.4', ['MIT'])
            .add_child(runtime_node('concurrent-ruby', '1.0.2', ['BSD']))
            .add_child(runtime_node('i18n', '0.7', ['Ruby', 'MIT']))
            .add_child(runtime_node('minitest', '5.1', ['MIT']))
        )
        .add_child(
            runtime_node('activerecord', '5.1.4', ['MIT'])
            .add_child(
                runtime_node('activemodel', '5.1.4', ['MIT'])
                .add_child(runtime_node('activesupport', '5.1.4', ['MIT'], hidden=True))
            )
            .add_child(development_node('activesupport', '5.1.4', ['MIT'], hidden=True))
            .add_child(development_node('arel', '8.0', ['Apache']))
        )
        .add_child(runtime_node('activemodel', '5.1.4', ['MIT'], hidden=True))
    )


def development_resolution():
    return (
        development_node('rails', '5.1.4', ['MIT'])
        .add_child(
            runtime_node('activerecord', '5.1.4', ['MIT'])
            .add_child(
                runtime_node('activemodel', '5.1.4', ['MIT'])
                .add_child(runtime_node('activesupport', '5.1.4', ['MIT'], hidden=True))
            )
        )
    )


def test_repr(manifest):
    resolution = ManifestResolution(manifest)
    resolution.add_children([
        runtime_resolution(),
        runtime_resolution(),
        development_resolution(),
        development_resolution()
    ])

    assert repr(resolution) == dedent(
        '''\
        + https://github.com/rails/rails {Gemfile} [Ruby]
        ⎮--+ [runtime] rails:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--= [runtime] concurrent-ruby:1.0.2 → BSD
        ⎮  ⎮  ⎮--= [runtime] i18n:0.7 → Ruby|MIT
        ⎮  ⎮  ⎮--= [runtime] minitest:5.1 → MIT
        ⎮  ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--• [development] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--= [development] arel:8.0 → Apache
        ⎮  ⎮--• [runtime] activemodel:5.1.4 → MIT
        ⎮--+ [runtime] rails:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--= [runtime] concurrent-ruby:1.0.2 → BSD
        ⎮  ⎮  ⎮--= [runtime] i18n:0.7 → Ruby|MIT
        ⎮  ⎮  ⎮--= [runtime] minitest:5.1 → MIT
        ⎮  ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--• [development] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--= [development] arel:8.0 → Apache
        ⎮  ⎮--• [runtime] activemodel:5.1.4 → MIT
        ⎮--+ [development] rails:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮--+ [development] rails:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        '''
    )
