

[![](https://codecov.io/gh/nickderobertis/treecomp/branch/main/graph/badge.svg)](https://codecov.io/gh/nickderobertis/treecomp)
[![PyPI](https://img.shields.io/pypi/v/treecomp)](https://pypi.org/project/treecomp/)
![PyPI - License](https://img.shields.io/pypi/l/treecomp)
[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/treecomp/)
![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)
![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)
![Tests Run on Windows Python Versions](https://img.shields.io/badge/Tests%20Windows%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)
[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/treecomp/)


#  treecomp

## Overview

A CLI and Python API to recursively compare directory trees and output a unified diff. 
Supports ignoring and targeting file and folder patterns with 
[`.gitignore`-style syntax](https://git-scm.com/docs/gitignore#_pattern_format).
Plays well with other tools: pipe output to [`dunk`](https://github.com/darrenburns/dunk) for pretty diffs and use 
`-f json` to output to JSON for use with [`jq`](https://stedolan.github.io/jq/) and other tools.

## Getting Started

The recommended way to install `treecomp` is with [`pipx`](https://github.com/pypa/pipx),
though it can also be installed with `pip`.

```
pipx install flexlate
```

Or, if you don't have/don't want to install `pipx`:

```
pip install flexlate
```

The unidiff output from this tool is best viewed using [`dunk`](https://github.com/darrenburns/dunk), 
which can also be installed via `pipx`/`pip`.

```shell
pipx install dunk
```

Compare two file trees recursively and output unified diffs.

```shell
treecomp my_folder_1 my_folder_2 | dunk
```

It supports ignoring and targeting patterns with 
[`.gitignore`-style syntax.](https://git-scm.com/docs/gitignore#_pattern_format) 
It also has a strongly-typed Python API.

See 
[examples in the documentation.](
https://nickderobertis.github.io/treecomp/index.html#examples
)

## Development Status

This project is currently in early-stage development. There may be
breaking changes often. While the major version is 0, minor version
upgrades will often have breaking changes.

## Developing

First ensure that you have `pipx` installed, if not, install it with `pip install pipx`.

Then clone the repo and run `npm install` and `pipenv sync`. Run `pipenv shell`
to use the virtual environment. Make your changes and then run `nox` to run formatting,
linting, and tests.

Develop documentation by running `nox -s docs` to start up a dev server.

To run tests only, run `nox -s test`. You can pass additional arguments to pytest
by adding them after `--`, e.g. `nox -s test -- -k test_something`.

## Author

Created by Nick DeRobertis. MIT License.

## Links

See the
[documentation here.](
https://nickderobertis.github.io/treecomp/
)
