#!/bin/bash
terminhtml 'treecomp file_trees/one file_trees/two | dunk' --cwd "$(realpath ..)" | terminrec -o source/_static/images/treecomp-recording.gif
