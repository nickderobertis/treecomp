import os
from typing import Sequence


def join_path_segments_into_str(segments: Sequence[str]) -> str:
    return os.path.sep.join(segments)
