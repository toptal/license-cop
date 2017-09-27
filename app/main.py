import sys
from textwrap import dedent

from app import *
from app.github.owner import *
from app.github.repository import *
from app.platform import *


def print_usage():
    print(
        dedent(
            '''\
            USAGE:

                license-cop <github-url> <report-file>

            where:

                <github-url>  is a valid GitHub organization or repository URL.
                <report-file> is the file where the report will be written to.

            EXAMPLES:

                $ license-cop https://github.com/acme report.txt

            will batch process all repositories from the "acme" organization
            and write the results to "report.txt".

                $ license-cop https://github.com/acme/foobar report.txt

            will process only the "foobar" repository from the "acme"
            organization, writing the results to "report.txt".
            '''
        ),
        file=sys.stderr
    )


def process_repository(repo, report):
    for platform in PLATFORMS:
        print('--> Looking for {0} package descriptors...'.format(platform.name))
        match = platform.match(repo)
        if match:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            print('--> Resolving {0} dependencies. This will take a while...'.format(platform.name))
            platform.resolve(match, report)
            sys.stdout.write('\033[K')
        else:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            print('--> Did not find any {0} package descriptors.'.format(platform.name))


def get_github(url):
    github = GithubOwner.from_url(url)
    if github:
        return github

    github = GithubRepository.from_url(url)
    if github:
        return github

    print('Invalid GitHub URL, or missing read permissions: {0}'.format(url), file=sys.stderr)
    sys.exit(1)


def parse_arguments():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    return (sys.argv[1], sys.argv[2])


def get_repositories(github):
    if isinstance(github, GithubOwner):
        return github.repositories()
    elif isinstance(github, GithubRepository):
        return [github]


def process_repositories(github, report):
    repos = get_repositories(github)
    for i, repo in enumerate(repos):
        print('==> Checking repository {0} of {1} [{2}]'.format(i+1, len(repos), repo))
        process_repository(repo, report)


def main():
    (url, filename) = parse_arguments()
    github = get_github(url)
    print('• Checking {0}'.format(repr(github)))
    print('• Report will be saved in "{0}"'.format(filename))
    with open(filename, 'w') as report:
        process_repositories(github, report)


if __name__ == "__main__":
    main()
