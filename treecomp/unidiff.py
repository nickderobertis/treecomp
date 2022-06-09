from difflib import unified_diff
from pathlib import Path
from typing import List, Optional


def _create_unified_diff_of_files(
    file1: Path,
    file2: Path,
    file_1_name: Optional[str] = None,
    file_2_name: Optional[str] = None,
) -> str:
    file_1_name = file_1_name or str(file1)
    file_2_name = file_2_name or str(file2)

    try:
        lines1 = file1.read_text().splitlines()
    except UnicodeDecodeError:
        return _create_unified_diff_of_binary_files(file_1_name, file_2_name)
    try:
        lines2 = file2.read_text().splitlines()
    except UnicodeDecodeError:
        return _create_unified_diff_of_binary_files(file_1_name, file_2_name)

    diff = unified_diff(
        lines1, lines2, fromfile=file_1_name, tofile=file_2_name, lineterm=""
    )
    return "\n".join(diff)


def _create_unified_diff_of_binary_files(
    file_1_name: str,
    file_2_name: str,
) -> str:
    return f"Binary files {file_1_name} and {file_2_name} differ"


def _create_unified_diff_of_file_added(
    file: Path, file_name: Optional[str] = None
) -> str:
    file_name = file_name or str(file)

    try:
        lines = file.read_text().splitlines()
    except UnicodeDecodeError:
        return _create_unified_diff_of_binary_files(file_name, file_name)

    diff = unified_diff([], lines, fromfile=file_name, tofile=file_name, lineterm="")
    return "\n".join(diff)


def _create_unified_diff_of_file_removed(
    file: Path, file_name: Optional[str] = None
) -> str:
    file_name = file_name or str(file)

    try:
        lines = file.read_text().splitlines()
    except UnicodeDecodeError:
        return _create_unified_diff_of_binary_files(file_name, file_name)

    diff = unified_diff(lines, [], fromfile=file_name, tofile=file_name, lineterm="")
    return "\n".join(diff)


def _create_unified_diff_from_list(lines: List[str], file_name: str) -> str:
    diff = unified_diff([], lines, fromfile=file_name, tofile=file_name, lineterm="")
    return "\n".join(diff)
