import filecmp
import os
from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import List, Optional, Sequence, Set, Union

from treecomp.fs_utils import list_path_filter_by_matchers
from treecomp.ignore import parse_ignore_list_into_matcher
from treecomp.target import parse_target_list_into_matcher


@dataclass(frozen=True)
class FileDiff:
    path: Path
    exists_in_dir1: bool
    exists_in_dir2: bool
    line_diff: Optional[str] = None


@dataclass(frozen=True)
class FileDiffWithDirs:
    diff: FileDiff
    dir1: Path
    dir2: Path

    @property
    def dir_1_path(self) -> Path:
        return self.dir1 / self.diff.path

    @property
    def dir_2_path(self) -> Path:
        return self.dir2 / self.diff.path

    @property
    def diff_str(self) -> str:
        """
        Unified diff format output.
        """
        if self.diff.line_diff:
            return self.diff.line_diff
        else:
            # File exists in both directories but there is no line diff, must be a binary file.
            return _create_unified_diff_from_list(
                ["binary file, cannot compare lines"], str(self.dir_2_path)
            )


@dataclass(frozen=True)
class _FolderDiffResults:
    file_diffs: List[FileDiff]
    could_not_diff: List[Path]


@dataclass(frozen=True)
class FileTreeComparison:
    dir1: Path
    dir2: Path
    diffs: List[FileDiff]
    could_not_diff: List[Path]

    def __str__(self) -> str:
        return "\n".join(
            FileDiffWithDirs(diff=file_diff, dir1=self.dir1, dir2=self.dir2).diff_str
            for file_diff in self.diffs
        )

    def diff_for(self, path: Union[str, Path]) -> Optional[FileDiffWithDirs]:
        for diff in self.diffs:
            diff_with_dirs = FileDiffWithDirs(diff=diff, dir1=self.dir1, dir2=self.dir2)
            if Path(path) in [
                diff.path,
                diff_with_dirs.dir_1_path,
                diff_with_dirs.dir_2_path,
            ]:
                return diff_with_dirs
        return None


def diff_file_trees(
    dir1: Union[str, Path],
    dir2: Union[str, Path],
    ignore: Optional[Sequence[str]] = None,
    target: Optional[Sequence[str]] = None,
) -> FileTreeComparison:
    """
    Compare two folders recursively, returning diffs of files that have differing content
    """
    folder_diff_results = _diff_file_trees(
        dir1,
        dir2,
        ignore=ignore,
        target=target,
    )
    return FileTreeComparison(
        dir1=Path(dir1),
        dir2=Path(dir2),
        diffs=folder_diff_results.file_diffs,
        could_not_diff=folder_diff_results.could_not_diff,
    )


def _diff_file_trees(
    dir1: Union[str, Path],
    dir2: Union[str, Path],
    ignore: Optional[Sequence[str]] = None,
    target: Optional[Sequence[str]] = None,
    relative_root: Path = Path("."),
) -> _FolderDiffResults:
    file_diffs: List[FileDiff] = []
    could_not_diff: List[Path] = []
    left_only: Set[str] = set()
    right_only: Set[str] = set()
    common_files: Set[str] = set()
    dir1 = Path(dir1)
    dir2 = Path(dir2)
    ignore_matcher = parse_ignore_list_into_matcher(ignore)
    target_matcher = parse_target_list_into_matcher(target)

    def _get_files(dir: Path) -> Set[str]:
        return set(
            list_path_filter_by_matchers(
                dir,
                ignore_matcher,
                target_matcher,
                include_dirs=False,
                root=relative_root,
            )
        )

    def _get_dirs(dir: Path) -> Set[str]:
        return set(
            list_path_filter_by_matchers(
                dir,
                ignore_matcher,
                target_matcher,
                include_files=False,
                root=relative_root,
            )
        )

    left_files = _get_files(dir1)
    right_files = _get_files(dir2)

    if not dir1.exists():
        right_only = right_files
    elif not dir2.exists():
        left_only = left_files
    else:
        left_only = left_files - right_files
        right_only = right_files - left_files
        common_files = left_files & right_files

    # Handle files that are only in one of the directories
    if len(left_only) > 0:
        file_diffs.extend(
            [
                FileDiff(
                    path=relative_root / file,
                    exists_in_dir1=True,
                    exists_in_dir2=False,
                    line_diff=_create_unified_diff_of_file_removed(dir1 / file),
                )
                for file in left_only
                if (dir1 / file).is_file()
            ]
        )
    if len(right_only) > 0:
        file_diffs.extend(
            [
                FileDiff(
                    path=relative_root / file,
                    exists_in_dir1=False,
                    exists_in_dir2=True,
                    line_diff=_create_unified_diff_of_file_added(dir2 / file),
                )
                for file in right_only
                if (dir2 / file).is_file()
            ]
        )

    (_, mismatch, errors) = filecmp.cmpfiles(dir1, dir2, common_files, shallow=False)
    if len(mismatch) > 0:
        for file in mismatch:
            diff = _create_unified_diff_of_files(
                dir1 / file, dir2 / file, str(dir2 / file), str(dir2 / file)
            )
            file_diffs.append(
                FileDiff(
                    path=relative_root / file,
                    exists_in_dir1=True,
                    exists_in_dir2=True,
                    line_diff=diff,
                )
            )

    if len(errors) > 0:
        could_not_diff.extend([relative_root / file for file in errors])

    # Find all directories at this level in both trees
    all_dir_names: Set[str] = _get_dirs(dir1) | _get_dirs(dir2)

    for dir in all_dir_names:
        new_dir1 = os.path.join(dir1, dir)
        new_dir2 = os.path.join(dir2, dir)
        new_relative_root = relative_root / dir
        nested_result = _diff_file_trees(
            new_dir1,
            new_dir2,
            ignore=ignore,
            target=target,
            relative_root=new_relative_root,
        )
        file_diffs.extend(nested_result.file_diffs)
        could_not_diff.extend(nested_result.could_not_diff)

    return _FolderDiffResults(file_diffs=file_diffs, could_not_diff=could_not_diff)


def _create_unified_diff_of_files(
    file1: Path,
    file2: Path,
    file_1_name: Optional[str] = None,
    file_2_name: Optional[str] = None,
) -> Optional[str]:
    try:
        lines1 = file1.read_text().splitlines()
    except UnicodeDecodeError:
        return None
    try:
        lines2 = file2.read_text().splitlines()
    except UnicodeDecodeError:
        return None

    file_1_name = file_1_name or str(file1)
    file_2_name = file_2_name or str(file2)
    diff = unified_diff(
        lines1, lines2, fromfile=file_1_name, tofile=file_2_name, lineterm=""
    )
    return "\n".join(diff)


def _create_unified_diff_of_file_added(
    file: Path, file_name: Optional[str] = None
) -> Optional[str]:
    try:
        lines = file.read_text().splitlines()
    except UnicodeDecodeError:
        return None

    file_name = file_name or str(file)
    diff = unified_diff([], lines, fromfile=file_name, tofile=file_name, lineterm="")
    return "\n".join(diff)


def _create_unified_diff_of_file_removed(
    file: Path, file_name: Optional[str] = None
) -> Optional[str]:
    try:
        lines = file.read_text().splitlines()
    except UnicodeDecodeError:
        return None

    file_name = file_name or str(file)
    diff = unified_diff(lines, [], fromfile=file_name, tofile=file_name, lineterm="")
    return "\n".join(diff)


def _create_unified_diff_from_list(lines: List[str], file_name: str) -> str:
    diff = unified_diff([], lines, fromfile=file_name, tofile=file_name, lineterm="")
    return "\n".join(diff)
