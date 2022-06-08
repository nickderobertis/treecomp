import filecmp
import os
from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import List, Optional, Sequence, Set, Union


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
    include_default_ignores: bool = True,
) -> FileTreeComparison:
    """
    Compare two folders recursively, returning diffs of files that have differing content
    """
    folder_diff_results = _diff_file_trees(
        dir1, dir2, ignore=ignore, include_default_ignores=include_default_ignores
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
    include_default_ignores: bool = True,
    relative_root: Path = Path("."),
) -> _FolderDiffResults:
    file_diffs: List[FileDiff] = []
    could_not_diff: List[Path] = []
    left_only: List[str] = []
    right_only: List[str] = []
    funny_files: List[str] = []
    common_files: List[str] = []
    dir1 = Path(dir1)
    dir2 = Path(dir2)
    use_ignore = list(ignore) if ignore is not None else []
    if include_default_ignores:
        use_ignore.extend(filecmp.DEFAULT_IGNORES)
    if not dir1.exists():
        right_only = os.listdir(dir2)
    elif not dir2.exists():
        left_only = os.listdir(dir1)
    else:
        dirs_cmp = filecmp.dircmp(dir1, dir2, ignore=use_ignore)
        left_only = dirs_cmp.left_only
        right_only = dirs_cmp.right_only
        funny_files = dirs_cmp.funny_files
        common_files = dirs_cmp.common_files

    # Handle files that are only in one of the directories
    if len(left_only) > 0:
        file_diffs.extend(
            [
                FileDiff(
                    path=relative_root / file,
                    exists_in_dir1=True,
                    exists_in_dir2=False,
                    line_diff=_create_unified_diff_of_file_added(dir1 / file),
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

    # Handle files that are in both directories, but could not be diffed
    if len(funny_files) > 0:
        could_not_diff.extend([relative_root / file for file in funny_files])

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
    all_dir_names: Set[str] = set(_get_names_of_dirs_directly_in_dir(dir1, use_ignore))
    all_dir_names.update(_get_names_of_dirs_directly_in_dir(dir2, use_ignore))

    for dir in all_dir_names:
        new_dir1 = os.path.join(dir1, dir)
        new_dir2 = os.path.join(dir2, dir)
        new_relative_root = relative_root / dir
        nested_result = _diff_file_trees(
            new_dir1,
            new_dir2,
            ignore=ignore,
            include_default_ignores=include_default_ignores,
            relative_root=new_relative_root,
        )
        file_diffs.extend(nested_result.file_diffs)
        could_not_diff.extend(nested_result.could_not_diff)

    return _FolderDiffResults(file_diffs=file_diffs, could_not_diff=could_not_diff)


def _get_names_of_dirs_directly_in_dir(
    dir: Union[str, Path], ignore: Sequence[str] = tuple()
) -> List[str]:
    if not Path(dir).exists():
        return []
    # TODO: support globs and other more complicated ignore patterns like gitignore
    #  May also be necessary to update the logic that is passing ignore to dircmp
    return [
        name
        for name in os.listdir(dir)
        if name not in ignore and os.path.isdir(os.path.join(dir, name))
    ]


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


def _create_unified_diff_from_list(lines: List[str], file_name: str) -> str:
    diff = unified_diff([], lines, fromfile=file_name, tofile=file_name, lineterm="")
    return "\n".join(diff)
