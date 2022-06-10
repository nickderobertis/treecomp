% treecomp documentation master file, created by
%   copier-pypi-sphinx-flexlate.
%   You can adapt this file completely to your liking, but it should at least
%   contain the root `toctree` directive.

# Welcome to treecomp documentation!

```{terminhtml}
---
cwd: ..
---
treecomp tests/input_files/file_trees/one tests/input_files/file_trees/two | dunk
```

```{include} ../../README.md
```

For more information on getting started, take a look at the tutorial and examples.

## Tutorial and Examples

Ignore files with comma-separated gitignore-style syntax:

```{terminhtml}
---
cwd: ..
---
treecomp tests/input_files/file_trees/one tests/input_files/file_trees/two -i directory,*.png | dunk
```

Target files with the same comma-separated gitignore-style syntax:

```{terminhtml}
---
cwd: ..
---
treecomp tests/input_files/file_trees/one tests/input_files/file_trees/two -t *.txt,diff-image.png | dunk
```

Output to JSON for use with `jq` and other tools:

```{terminhtml}
---
cwd: ..
---
treecomp tests/input_files/file_trees/one tests/input_files/file_trees/two -f json | jq '.[].path'
```

```{toctree}

tutorial
auto_examples/index
```

## API Documentation

```{eval-rst}
.. toctree:: api/modules
   :maxdepth: 3
```

## Indices

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
