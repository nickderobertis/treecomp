from typing import Optional, Sequence

from treecomp.path_matcher import PathMatcher, parse_list_into_file_matcher


def parse_target_list_into_matcher(
    target_list: Optional[Sequence[str]] = None,
) -> PathMatcher:
    # If no target list is passed, then we want to match everything.
    if not target_list:
        return lambda match_path, folder: True

    matcher = parse_list_into_file_matcher(target_list)
    return matcher
