import sys
from textwrap import dedent

from app import *
from app.github_repository import *
from app.platform_resolver import *


def main():
    if len(sys.argv) < 2:
        print(
            dedent(
                '''\
                usage: license-cop <url>

                where <url> is a valid GitHub repository URL. Example:

                    $ license-cop https://github.com/toptal/license-cop
                '''
            ),
            file=sys.stderr
        )
        sys.exit(1)

    url = sys.argv[1]
    repository = GithubRepository.from_url(url)

    if not repository:
        print(
            'Invalid GitHub repository, or missing read permissions: {0}'.format(url),
            file=sys.stderr
        )
        sys.exit(1)

    print('==> Processing {0}'.format(url))

    for platform in PLATFORM_RESOLVERS:
        print()
        print('==> Looking for {0} artifacts...'.format(platform.name))
        if platform.match(repository):
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            print('==> Resolving {0} dependencies:'.format(platform.name))
            print()
            resolutions = platform.resolve(repository)
            sys.stdout.write('\033[K')
            for resolution in resolutions:
                print(repr(resolution))
        else:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            print('==> Could not find {0} artifacts.'.format(platform.name))


if __name__ == "__main__":
    main()
