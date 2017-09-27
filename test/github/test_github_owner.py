import pytest
import requests

from test import *
from app.github.owner import *
from app.github.repository import *


def build_owner(name):
    return GithubOwner(name, http_compression=False)


@pytest.fixture
def docker(): return build_owner('docker')


def test_parse_valid_github_url():
    repo = GithubOwner.from_url('https://github.com/acme')
    assert repo.name == 'acme'


def test_does_not_parse_invalid_url():
    assert GithubOwner.from_url('https:///foobar') is None


def test_does_not_parse_github_url_with_repository():
    assert GithubOwner.from_url('https://github.com/acme/foobar') is None


@VCR.use_cassette('github_owner_fetch_all_organization_repositories_using_pagination.yaml')
def test_fetch_all_organization_repositories_using_pagination(docker):
    repos = docker.repositories()

    assert len(repos) == 117
    for repo in repos:
        assert repo.owner == docker.name

    assert set(map(lambda i: i.name, repos)) == set([
        'bender',
        'docker-registry',
        'dockerlite',
        'docker-py',
        'openstack-docker',
        'go-redis-server',
        'docker-tutorial',
        'openstack-heat-docker',
        'gordon',
        'docker-status',
        'compose',
        'libcontainer',
        'swarm',
        'libtrust',
        'spdystream',
        'libchan',
        'irc-minutes',
        'etcd',
        'kitematic',
        'dnsserver',
        'docker-bb',
        'jira-test',
        'machine',
        'distribution',
        'docker-network',
        'gordon-bot',
        'swarm-library-image',
        'leeroy',
        'birthdaysite',
        'libnetwork',
        'docker-bench-security',
        'libcompose',
        'whalesay',
        'hub-feedback',
        'opensource',
        'libkv',
        'notary',
        'dockercraft',
        'toolbox',
        'migrator',
        'go',
        'distribution-library-image',
        'notary-server-image',
        'notary-signer-image',
        'golem',
        'global-hack-day-3',
        'dctx',
        'dceu_tutorials',
        'hugo',
        'go-healthcheck',
        'markdownlint',
        'linkcheck',
        'community',
        'swarm-frontends',
        'ucp_lab',
        'go-units',
        'go-plugins-helpers',
        'go-connections',
        'engine-api',
        'docker-machine-driver-ci-test',
        'go-dockercloud',
        'python-dockercloud',
        'v1.10-migrator',
        'dockercloud-cli',
        'swarm-microservice-demo-v1',
        'dockercloud-network-daemon',
        'dockercloud-agent',
        'dockercloud-events',
        'dockercloud-node',
        'goamz',
        'dockercloud-haproxy',
        'notary-official-images',
        'docker-credential-helpers',
        'leadership',
        'swarmkit',
        'dockercloud-hello-world',
        'dockercloud-quickstart-python',
        'dockercloud-quickstart-go',
        'dockercloud-authorizedkeys',
        'docker-birthday-3',
        'go-events',
        'go-p9p',
        'homebrew-core',
        'infrakit',
        'jenkins-pipeline-scripts',
        'labs',
        'code-of-conduct',
        'orchestration-workshop',
        'dcus-hol-2016',
        'for-mac',
        'for-win',
        'go-metrics',
        'docker.github.io',
        'pulpo',
        'infrakit.aws',
        'communitytools-image2docker-win',
        'runc',
        'compliance',
        'communitytools-image2docker-linux',
        'infrakit.gcp',
        'for-aws',
        'for-azure',
        'docker-snap',
        'looker-slackbot',
        'dcus-hol-2017',
        'vol-test',
        'cli',
        'infrakit.digitalocean',
        'libentitlement',
        'for-linux',
        'docker-ce',
        'docker-ce-packaging',
        'containerd',
        'docker-install',
        'golang-cross',
        'runtime-spec',
        'gorethink'
    ])


@VCR.use_cassette('github_owner_fetch_organization_repositories_not_found.yaml')
def test_fetch_organization_repositories_not_found():
    with pytest.raises(requests.exceptions.HTTPError):
        build_owner('foobar-9872098098243234').repositories()
