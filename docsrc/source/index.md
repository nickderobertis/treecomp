% treecomp documentation master file, created by
%   copier-pypi-sphinx-flexlate.
%   You can adapt this file completely to your liking, but it should at least
%   contain the root `toctree` directive.

# Welcome to treecomp documentation!

```{terminhtml}
---
cwd: ..
---
treecomp file_trees/one file_trees/two | dunk
```

```{include} ../../README.md
```

For more information on getting started, take a look at the examples.

## Examples

### CLI

Ignore files with comma-separated [`.gitignore`-style syntax](https://git-scm.com/docs/gitignore#_pattern_format):

```{terminhtml}
---
cwd: ..
---
treecomp file_trees/one file_trees/two -i code,*.png | dunk
```

Target files with the same comma-separated [`.gitignore`-style syntax](https://git-scm.com/docs/gitignore#_pattern_format):

```{terminhtml}
---
cwd: ..
---
treecomp file_trees/one file_trees/two -t *.py,image-two-only.png | dunk
```

Output to JSON for use with [`jq`](https://stedolan.github.io/jq/) and other tools. Here, we select 
the relative path of all the files that differ:

```{terminhtml}
---
cwd: ..
---
treecomp file_trees/one file_trees/two -f json | jq '.[].path'
```

We could also use `jq` to select the files that differ and exist 
in the left directory (use `right` to to do same with right directory):

```{terminhtml}
---
cwd: ..
---
treecomp file_trees/one file_trees/two -f json | jq '.[] | select(.left) | .path'
treecomp file_trees/one file_trees/two -f json | jq '.[] | select(.right) | .path'
```

There are fancier operations you can do with `jq`, such as determining 
which folders have diffs:

```{terminhtml}
---
cwd: ..
---
treecomp file_trees/one file_trees/two -f json | jq -s '.[] | map(select(.left).path | split("/")) | map(.[:-1]) | map("./" +  (. | join("/"))) | unique'
```

You can even use `jq` to select the diffs you want and then pipe the 
diffs back to `dunk` for display, here again selecting only diffs 
that exist in the left directory:

```{terminhtml}
---
cwd: ..
---
treecomp file_trees/one file_trees/two -f json | jq -sr '.[] | map(select(.left).diff) | join("\n")' | dunk
```

### Python API

You can also use `treecomp` as a Python module, with a very similar API:

```python
import treecomp

comp = treecomp.diff_file_trees(
    "file_trees/one", 
    "file_trees/two", 
    ignore=["subdir"], 
    target=["*.py"]
)
print(len(comp), "diffs in total")
for diff in comp:
    if diff.left:
        print("Files with diffs that exist in left:")
        print(diff.path)
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
