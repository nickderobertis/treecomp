import os
from pathlib import Path
from typing import List, Union, cast

from treecomp.path_matcher import PathMatcher


def list_path_filter_by_matchers(
    dir: Union[str, Path],
    ignore_matcher: PathMatcher,
    target_matcher: PathMatcher,
    include_files: bool = True,
    include_dirs: bool = True,
    root: Path = Path("."),
) -> List[str]:
    dir = Path(dir)
    if not dir.exists():
        return []
    if not include_files and not include_dirs:
        raise ValueError("must either include files or include dirs")
    orig_dir_root = _get_orig_root_from_dir_and_relative_path_within_dir(dir, root)
    out: List[str] = []
    for name in os.listdir(dir):
        name = cast(str, name)
        match_path = root / name
        real_path = dir / name
        if not include_dirs and real_path.is_dir():
            continue
        if not include_files and real_path.is_file():
            continue
        if target_matcher(match_path, orig_dir_root) and not ignore_matcher(
            match_path, orig_dir_root
        ):
            out.append(name)

    return out


def _get_orig_root_from_dir_and_relative_path_within_dir(
    dir: Path, relative_within_dir: Path
) -> Path:
    """
    Return the original root from a directory and a relative path within that directory.
    """
    orig_root = dir
    for _ in relative_within_dir.parts:
        orig_root = orig_root.parent
    return orig_root
