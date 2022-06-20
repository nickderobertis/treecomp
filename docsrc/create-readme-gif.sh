#!/bin/bash
terminhtml "$(<demo.sh)" --cwd "$(realpath ..)" | terminrec -o source/_static/images/treecomp-recording.gif
