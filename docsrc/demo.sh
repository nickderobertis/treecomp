treecomp file_trees/one file_trees/two | dunk
treecomp file_trees/one file_trees/two -f json | jq '.[].path'