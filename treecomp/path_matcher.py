import os
from pathlib import Path
from typing import Callable, Optional, Sequence, Union

from pathspec import PathSpec

PathMatcher = Callable[[Union[str, Path], Path], bool]


def parse_list_into_file_matcher(
    pattern_list: Optional[Sequence[str]] = None,
) -> PathMatcher:
    spec = PathSpec.from_lines("gitwildmatch", pattern_list or [])

    def matcher(match_path: Union[str, Path], containing_folder: Path) -> bool:
        """
        Adjust the base_matcher from pathspec gitwildmatch so that when
        a directory is passed, it will check if any files in the directory meet
        the pattern. If any file is matched in the directory, the directory will be
        matched.
        """
        real_path = containing_folder / match_path
        if real_path.is_file():
            return spec.match_file(str(match_path))
        if not real_path.exists():
            # Path does not exist, return False
            return False

        # Path is a directory, recursively check if any files in the directory meet the pattern
        def _recursive_matcher(path: Path) -> bool:
            for file in path.iterdir():
                if file.is_file():
                    path_to_match = os.path.relpath(file, containing_folder)
                    if spec.match_file(path_to_match):
                        return True
                elif file.is_dir():
                    if _recursive_matcher(file):
                        return True
            return False

        return _recursive_matcher(real_path)

    return matcher
