# License Cop

A nifty script that fetches the licenses for all your third-party libraries.

![Dog cop meme](meme.jpg)

## System requirements

You will need:

- Python 3.6 or better
- Pipenv (The official Python dependency manager, similar to npm or Bundler)

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
