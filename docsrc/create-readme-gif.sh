#!/bin/bash
GIF_PATH=source/_static/images/treecomp-recording.gif
terminhtml "$(<demo.sh)" --cwd "$(realpath ..)" | terminrec -o $GIF_PATH
gifsicle --optimize $GIF_PATH -o $GIF_PATH