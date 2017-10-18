import sys
import traceback
from textwrap import dedent

from app import *
from app.github.owner import *
from app.github.repository import *
from app.platform import *
from app.reporting.excel import ExcelReport
from app.reporting.plain_text import PlainTextReport


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


def process_repository(repository, report):
    for platform in PLATFORMS:
        print(f'--> Looking for {platform} package descriptors...')
        match = platform.match(repository)
        if match:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            print(f'--> Resolving {platform} dependencies (will take a while...)')
            report.process(match)
            sys.stdout.write('\033[K')
        else:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            print(f'--> Did not find any {platform} package descriptors.')


def get_github(url):
    github = GithubOwner.from_url(url)
    if github:
        return github

    github = GithubRepository.from_url(url)
    if github:
        return github

    print(f'Invalid GitHub URL, or missing read permissions: {url}', file=sys.stderr)
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
        print(f'==> Processing repository {i+1} of {len(repos)} [{repo.url}]')
        try:
            process_repository(repo, report)
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()


def main():
    (url, filename) = parse_arguments()
    github = get_github(url)
    print(f'• Checking {repr(github)}')
    print(f'• Report will be saved in "{filename}"')
    try:
        report = ExcelReport(filename, max_depth=None)
        # report = PlainTextReport(filename)
        process_repositories(github, report)
    except KeyboardInterrupt:
        print('Aborting...')
    finally:
        report.close()


if __name__ == '__main__':
    main()
