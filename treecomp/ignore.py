from typing import Optional, Sequence

from treecomp.path_matcher import PathMatcher, parse_list_into_file_matcher

DEFAULT_IGNORES = (
    "RCS",
    "CVS",
    "tags",
    ".git",
    ".hg",
    ".bzr",
    "_darcs",
    "__pycache__",
    "node_modules",
    ".yarn",
)


def parse_ignore_list_into_matcher(
    ignore_list: Optional[Sequence[str]] = None,
) -> PathMatcher:
    all_ignores = [*DEFAULT_IGNORES, *(ignore_list or [])]
    matcher = parse_list_into_file_matcher(all_ignores)

    return matcher
