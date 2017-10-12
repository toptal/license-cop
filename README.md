# License Cop

A nifty script that fetches the licenses for all your third-party libraries.

![Dog cop meme](meme.jpg)

## Supported Platforms

The following platforms are supported:

- Ruby — [RubyGems](https://rubygems.org):
  - [x] [`Gemfile`](http://bundler.io/v1.15/man/gemfile.5.html)
  - [ ] [`*.gemspec`](http://guides.rubygems.org/specification-reference/) files (_not being used in Toptal projects_)
- Python — [PyPI](https://pypi.python.org):
  - [x] [Requirements files](https://pip.readthedocs.io/en/1.1/requirements.html) (eg: `requirements.txt`, `requirements-test.txt`...)
  - [x] [`Pipfile`](https://github.com/pypa/pipfile)
  - [ ] [`setup.py`](https://packaging.python.org/tutorials/distributing-packages/) (_not being used in Toptal projects_)
- Node.js — [NPM](https://www.npmjs.com):
  - [x] `package.json`
- Scala:
  - [x] [`build.sbt`](http://www.scala-sbt.org/1.x/docs/Library-Dependencies.html)
  - [x] [`project` folder](http://www.scala-sbt.org/1.0/docs/Directories.html) with `*.scala` or `*.sbt` files
- JVM (Java, Scala...):
  - [ ] [Ivy](http://ant.apache.org/ivy/history/2.0.0/ivyfile.html) (`*.ivy` files)
  - [ ] [Maven](https://maven.apache.org/pom.html) (`*.pom` files)
- iOS (Swift, Objective-C) — [CocoaPods](https://cocoapods.org):
  - [ ] [`Podfile`](https://guides.cocoapods.org/using/the-podfile.html)
- Elixir — [Hex](https://hex.pm):
  - [x] [`mix.exs`](https://hex.pm/docs/usage)

## System Requirements

You will need:

- Python 3.6 or better
- Pipenv (The official Python dependency manager, similar to npm or Bundler)

### Installing Pipenv

It's advisable to [install Pipenv locally](http://docs.python-guide.org/en/latest/dev/virtualenvs/#installing-pipenv),
but in most systems installing it system-wide should work just fine. If you're
using a homebrewed macOS:

```sh
$ pip3 install pipenv
```

Make sure your shell profile (eg: `~/.profile` or `~/.bash_profile`) exports the
following environment variables, otherwise Pipenv will not work:

```sh
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### The `GITHUB_TOKEN` environment variable

You need to have a valid
[GitHub personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)
with enough permissions to read the repositories you want.

This token needs to be exported to the `GITHUB_TOKEN` environment variable.

## Running License Cop

Once everything is set, run the `./license-cop` script. It will print
its usage instructions.

## Running Tests

We use [pytest](https://docs.pytest.org/en/latest/) to execute our automated
test suite, which is installed by Pipenv.

To run the entire test suite, just invoke the `./test.sh` script.

## Architecture and Domain

### Source Code Repository

Source code repositories, or simple, _repositories_, are file hierarchies that
stores and versions source code.

Currently, only [GitHub](https://github.com) repositories are supported, being
represented by instances of the [GithubRepository](app/github/repository.py)
class. If necessary, support for different version control platforms can be
easilly added.

### Package, Version and Dependency

Packages are binary artifacts. A project, when fully assembled, is ultimately a
package itself. Packages have versions (ex: `2.5.3`).

A package may depend on other packages. Package dependencies, or just
_dependencies_, describe the requirements that a package must be shipped with.

A package version is represented by the
[PackageVersion](app/package_version.py) class, and has the following data:

- _name_ (eg: `httparty`).
- _version number_ (eg: `2.5.3`).
- _runtime dependencies_ — dependencies required by production code.
- _development dependencies_ — dependencies required only for testing and local development.
- _licenses_ (eg: BSD and Apache 2.0).

A dependency has the following information, and it is represented by the
[Dependency](app/dependency.py) class:

- _package name_ (eg: `httparty`).
- _kind_ (runtime or development).
- _version requirements_ (eg: a version higher or equal
  than `2.0.3` but less than `2.1`).

Dependencies are resolved by a package manager, which will query and
download them from a package registry.

### Package Registry

Package registries are online hubs to store and share
package versions. Examples of registries are
[RubyGems](https://rubygems.org) and [PyPI](https://pypi.python.org/pypi).

The [`PackageRegistry`](app/package_registry.py) module is responsible for
interacting with the package registry API of the given platform, fetching
information about package versions, dependencies and licenses. For instance,
RubyGems provides a nice [REST API](http://guides.rubygems.org/rubygems-org-api/).

### Package Descriptor

A package descriptor is a set of one or several files that describe the
dependencies a project relies on. They are processed by the
package manager of a given platform.

For example, the Ruby platform has the `Gemfile` package descriptor, which
usually sits at the root of the project and is processed by the
[`bundler`](http://bundler.io) tool. This file
has a structure like this:

```ruby
source 'http://rubygems.org/'

gemspec

gem 'httparty', '~> 2.0.3'

group :test do
  gem 'rspec'
end

group :development do
  gem 'rake'
  gem 'rubocop'
end
```

Here it's being specified that [RubyGems](http://rubygems.org/) is the
package registry that should be used.

Parsing this file should result in a list of runtime
and development dependencies. Here `httparty` is a runtime dependency, and its
version should be higher or equal than `2.0.3` but less than `2.1`. Likewise,
`rspec`, `rake` and `rubocop` are all development dependencies, and any version
can be used, preferably the latest.

The [`PackageDescriptor`](app/package_descriptor.py) class has the following
data:

- _platform_ (eg: Python).
- _repository_ (eg: https://github.com/requests/requests).
- _paths on that repository_ (eg: `requirements.txt` and `requirements-test.txt`).
- _runtime dependencies_.
- _development dependencies_.

### Repository Matcher

The [`RepositoryMatcher`](app/repository_matcher.py) module is responsible for
browsing a repository's file structure, detecting package descriptor files for
a given platform and parsing them. The result is a list of dependencies.

It works as follows:

<pre>
let <i>P</i> be a platform
let <i>R</i> be a repository
let <i>T</i> be the file tree of <i>R</i>
for each file <i>F</i> from <i>T</i>:
    if <i>F</i> matches a format specified by <i>P</i>:
        then parse <i>F</i> for a list of runtime and development dependencies
</pre>

### Dependency Resolver and Resolution

Each package descriptor is fed to a
[`DependencyResolver`](app/dependency_resolver.py) instance, which will
query the package registry of the given platform in order to obtain
information about pacakge versions. It will then find a set of package versions
that match all dependency requirements specified in the package descriptor.

The result of this step is a tree, represented by the
[`DependencyResolution`](app/dependency_resolution.py) class.
This is an example:

```
+ pytest-mock:1.6.3 → MIT
⎮--= [runtime] mock:2.0.0 → BSD-2-Clause
⎮--+ [runtime] pytest:3.2.2 → MIT license
⎮  ⎮--= [runtime] colorama:0.3.9 → BSD
⎮  ⎮--= [runtime] ordereddict:1.1 → <no licenses found>
⎮  ⎮--= [runtime] argparse:1.4.0 → Python Software Foundation License
⎮  ⎮--• [runtime] setuptools:36.5.0 → MIT
⎮  ⎮--= [runtime] py:1.4.34 → MIT license
```

## Adding Support for a Platform

In order to support a platform, you need to do three things:

1. Implement the platform's [`PackageRegistry`](app/package_registry.py) class.
2. Implement the platform's [`RepositoryMatcher`](app/repository_matcher.py) class.
3. Register the platform.

### Implement the `PackageRegistry`

Suppose you want to support the `Foobar` platform. You would then create
a `FoobarPackageRegistry` class inside `app/platforms/foobar/package_registry.py`.

This class should extend [`PackageRegistry`](app/package_registry.py) and
implement all of its abstract methods:

```python
def _fetch_version(self, name, number)
def _fetch_latest_version(self, name)
```

These methods should each return an instance of
[`PackageVersion`](app/package_version.py).

The superclass already defines a `_session` attribute
that contains an instance of a
[`requests` session](http://docs.python-requests.org/en/master/user/advanced/#session-objects).
You can use this session to make HTTP requests to the platform's package registry.

Most package registry APIs are able to retrieve the license for a given package
version. Very often these licenses are not properly filled, or absent.
However, if the package registry is able to inform a GitHub repository for the
given version, we can leverage
[GitHub's license API](https://developer.github.com/v3/licenses/) to determine
the license.

To make this process as easy as possible, the superclass defines
the `_find_licenses_in_code_repository_urls` method, which receives a list of
(possible) urls, check if they reference valid GitHub repositories, and if they
do, retrieve their licenses.

```python
def _find_licenses_in_code_repository_urls(self, urls)
```

Also, please make sure you cover your implementation with tests using
[pytest](https://docs.pytest.org/en/latest/) and
[VCR](https://vcrpy.readthedocs.io/en/latest/). These tests should be placed
under `test/platforms/foobar/test_foobar_package_registry.py` (it's necessary
to include the platform name in the file name because of a pytest limitation).

### Implement the `RepositoryMatcher`

Likewise, you should create a `FoobarRepositoryMatcher` class inside
`app/platforms/foobar/repository_matcher.py`.

This class should extend [`RepositoryMatcher`](app/repository_matcher.py) and
implement all of its abstract methods. It should be initialized with a list
of unix shell-style wildcard patterns to be match in the repository's file tree.

Subclasses of `RepositoryMatcher` should pass to the super's `__init__`
block a list of patterns that will be matched against a repository. For example:

```python
class FoobarRepositoryMatcher(RepositoryMatcher):
    def __init__(self):
        super().__init__(['Foofile', '*.foospec'])
```

`FoobarRepositoryMatcher` should also override the `_fetch_package_descriptor`
method. This method receives the repository and a match object (
[`PackageDescriptorMatch`](app/repository_matcher.py)).

```python
def _fetch_package_descriptor(self, repository, match)
```

The match object will have a list of [`GitNode`](app/github/git_node.py)
instances that match one of the specified patterns.

You can then use the repository to fetch the contents of
the files you need. This method should return an instance of
[`PackageDescriptor`](app/package_descriptor.py).

Don't forget to cover your `FoobarRepositoryMatcher` with tests. They should
be placed in `test/platforms/foobar/test_foobar_repository_matcher.py`.

### Register the Platform

First, create a `app/platforms/foobar/__init__.py` file. Then build an instance
of [`Platform`](app/platform.py) as follows:

```python
from app.platforms.foobar.package_registry import *
from app.platforms.foobar.repository_matcher import *
from app.platform import *


INSTANCE = Platform('Foobar', FoobarRepositoryMatcher(), FoobarPackageRegistry())
```

Finally, just register this platform instance at the
[app initialization file](app/__init__.py), following the structure already
in place.
