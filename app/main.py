import sys
from textwrap import dedent

from app import *
from app.github_repository import *
from app.platform import *


def print_usage():
    print(
        dedent(
            '''\
            usage: license-cop <github-url> <report-file>

            where:

                <github-url>  is a valid GitHub repository URL.
                <report-file> is the file where the report will be written to.

            example:

                $ license-cop https://github.com/toptal/license-cop report.txt
            '''
        ),
        file=sys.stderr
    )


def process(repository, report):
    for platform in PLATFORMS:
        print('>> Looking for {0} package descriptors...'.format(platform.name))
        match = platform.match(repository)
        if match:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            print('>> Found {0} package descriptors. This will take a while...'.format(platform.name))
            platform.resolve(match, report)
            sys.stdout.write('\033[K')
        else:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            print('>> Did not find any {0} package descriptors.'.format(platform.name))


def get_repository(url):
    repository = GithubRepository.from_url(url)
    if not repository:
        print(
            'Invalid GitHub repository, or missing read permissions: {0}'.format(url),
            file=sys.stderr
        )
        sys.exit(1)
    return repository


def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    repository = get_repository(sys.argv[1])
    report_filename = sys.argv[2]

    with open(report_filename, 'w') as report:
        print('Processing {0}'.format(repository))
        process(repository, report)


if __name__ == "__main__":
    main()
