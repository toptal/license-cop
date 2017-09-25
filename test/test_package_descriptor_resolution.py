import pytest
from textwrap import dedent

from app.package_version import *
from app.dependency import *
from app.dependency_resolution import *
from app.package_descriptor import *
from app.package_descriptor_resolution import *
from app.github_repository import *


@pytest.fixture
def repository():
    return GithubRepository.from_url('https://github.com/rails/rails')


@pytest.fixture
def descriptor(repository):
    return PackageDescriptor(
        'Ruby',
        repository,
        'Gemfile',
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


def runtime_resolution():
    return DependencyResolution.runtime(version('rails', '5.1.4'))\
        .add_child(
            DependencyResolution.runtime(version('activesupport', '5.1.4', ['MIT']))
            .add_child(DependencyResolution.runtime(version('concurrent-ruby', '1.0.2', ['BSD'])))
            .add_child(DependencyResolution.runtime(version('i18n', '0.7', ['Ruby', 'MIT'])))
            .add_child(DependencyResolution.runtime(version('minitest', '5.1', ['MIT'])))
        )\
        .add_child(
            DependencyResolution.runtime(version('activerecord', '5.1.4', ['MIT']))
            .add_child(
                DependencyResolution.runtime(version('activemodel', '5.1.4', ['MIT']))
                .add_child(DependencyResolution.runtime(version('activesupport', '5.1.4', ['MIT']), is_hidden=True))
            )
            .add_child(DependencyResolution.development(version('activesupport', '5.1.4', ['MIT']), is_hidden=True))
            .add_child(DependencyResolution.development(version('arel', '8.0', ['Apache'])))
        )\
        .add_child(DependencyResolution.runtime(version('activemodel', '5.1.4', ['MIT']), is_hidden=True))


def development_resolution():
    return DependencyResolution.development(version('rails', '5.1.4'))\
        .add_child(
            DependencyResolution.runtime(version('activerecord', '5.1.4', ['MIT']))
            .add_child(
                DependencyResolution.runtime(version('activemodel', '5.1.4', ['MIT']))
                .add_child(DependencyResolution.runtime(version('activesupport', '5.1.4', ['MIT']), is_hidden=True))
            )
        )


def test_repr(descriptor):
    resolution = PackageDescriptorResolution(
        descriptor,
        runtime_resolutions=[
            runtime_resolution(),
            runtime_resolution()
        ],
        development_resolutions=[
            development_resolution(),
            development_resolution()
        ]
    )

    assert repr(resolution) == dedent(
        '''\
        + https://github.com/rails/rails - Ruby [Gemfile]
        ⎮--+ [runtime] rails:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--- [runtime] concurrent-ruby:1.0.2 → BSD
        ⎮  ⎮  ⎮--- [runtime] i18n:0.7 → Ruby, MIT
        ⎮  ⎮  ⎮--- [runtime] minitest:5.1 → MIT
        ⎮  ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--• [development] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--- [development] arel:8.0 → Apache
        ⎮  ⎮--• [runtime] activemodel:5.1.4 → MIT
        ⎮--+ [runtime] rails:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--- [runtime] concurrent-ruby:1.0.2 → BSD
        ⎮  ⎮  ⎮--- [runtime] i18n:0.7 → Ruby, MIT
        ⎮  ⎮  ⎮--- [runtime] minitest:5.1 → MIT
        ⎮  ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--• [development] activesupport:5.1.4 → MIT
        ⎮  ⎮  ⎮--- [development] arel:8.0 → Apache
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
