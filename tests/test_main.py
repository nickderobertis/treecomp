from enum import Enum
from typing import Final, List, Optional, Sequence

from tests.config import DIFF_IMAGE_NAME, FILE_TREE_ONE, FILE_TREE_TWO
from tests.dirutils import join_path_segments_into_str
from treecomp import diff_file_trees
from treecomp.main import FileDiff, FileTreeComparison

NUM_MAIN_DIRECTORY_DIFFS: Final[int] = 6
NUM_SUBDIRECTORY_DIFFS: Final[int] = 3
NUM_NON_TEXT_DIFFS: Final[int] = 3
ALL_DIFFS: Final[int] = NUM_MAIN_DIRECTORY_DIFFS + NUM_SUBDIRECTORY_DIFFS


class E2ETestFolder(str, Enum):
    MAIN = ""
    SUBDIRECTORY = "directory"


class E2ETestFile(str, Enum):
    A = "a.txt"
    B = "b.txt"
    C = "c.txt"
    D = join_path_segments_into_str([E2ETestFolder.SUBDIRECTORY.value, "d.txt"])
    E = join_path_segments_into_str([E2ETestFolder.SUBDIRECTORY.value, "e.txt"])
    F = join_path_segments_into_str([E2ETestFolder.SUBDIRECTORY.value, "f.txt"])
    IMAGE = DIFF_IMAGE_NAME
    ADDED_IMAGE = "image-two-only.png"
    REMOVED_IMAGE = "image-one-only.png"

    @property
    def folder(self) -> E2ETestFolder:
        return (
            E2ETestFolder.SUBDIRECTORY
            if self.value.startswith("directory")
            else E2ETestFolder.MAIN
        )

    def assert_diff_is_correct(self, diff: FileDiff) -> None:
        if self == E2ETestFile.A:
            _assert_a_diff_between_one_and_two_is_correct(diff)
        elif self == E2ETestFile.B:
            _assert_b_diff_between_one_and_two_is_correct(diff)
        elif self == E2ETestFile.C:
            _assert_c_diff_between_one_and_two_is_correct(diff)
        elif self == E2ETestFile.D:
            _assert_d_diff_between_one_and_two_is_correct(diff)
        elif self == E2ETestFile.E:
            _assert_e_diff_between_one_and_two_is_correct(diff)
        elif self == E2ETestFile.F:
            _assert_f_diff_between_one_and_two_is_correct(diff)
        elif self == E2ETestFile.IMAGE:
            _assert_image_diff_between_one_and_two_is_correct(diff)
        elif self == E2ETestFile.ADDED_IMAGE:
            _assert_image_added_between_one_and_two_is_correct(diff)
        elif self == E2ETestFile.REMOVED_IMAGE:
            _assert_image_removed_between_one_and_two_is_correct(diff)
        else:
            raise NotImplementedError(f"{self} has no diff assertion function")


MAIN_FOLDER_E2E_FILES: Final[List[E2ETestFile]] = [
    file for file in E2ETestFile if file.folder == E2ETestFolder.MAIN
]
SUBDIRECTORY_E2E_FILES: Final[List[E2ETestFile]] = [
    file for file in E2ETestFile if file.folder == E2ETestFolder.SUBDIRECTORY
]
ALL_E2E_FILES: Final[List[E2ETestFile]] = MAIN_FOLDER_E2E_FILES + SUBDIRECTORY_E2E_FILES


def test_diff_file_trees():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO)
    assert len(comp.diffs) == ALL_DIFFS
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    _assert_diffs_are_correct(comp)


def test_diff_file_trees_ignore_file():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["a.txt", "e.txt"])
    assert len(comp.diffs) == ALL_DIFFS - 2
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    _assert_diffs_are_correct(comp, exclude=(E2ETestFile.A, E2ETestFile.E))


def test_diff_file_trees_ignore_directory():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["directory"])
    assert len(comp.diffs) == NUM_MAIN_DIRECTORY_DIFFS
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    _assert_diffs_are_correct(comp, exclude=SUBDIRECTORY_E2E_FILES)


def test_diff_file_trees_ignore_glob_file_patterns():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["*.txt"])
    assert len(comp.diffs) == NUM_NON_TEXT_DIFFS

    img_diff = comp.diff_for(DIFF_IMAGE_NAME)
    _assert_image_diff_between_one_and_two_is_correct(img_diff)

    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO


def test_diff_file_trees_ignore_glob_folder_patterns():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["directory/*"])
    assert len(comp.diffs) == NUM_MAIN_DIRECTORY_DIFFS
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    _assert_diffs_are_correct(comp, exclude=SUBDIRECTORY_E2E_FILES)


def test_diff_file_trees_target_files():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, target=["a.txt"])
    assert len(comp.diffs) == 1
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    _assert_a_diff_between_one_and_two_is_correct(a_diff)

    assert a_diff.line_diff in str(comp)


def test_diff_file_trees_target_folders():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, target=["directory"])
    assert len(comp.diffs) == NUM_SUBDIRECTORY_DIFFS
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    _assert_diffs_are_correct(comp, exclude=MAIN_FOLDER_E2E_FILES)


def test_diff_file_trees_target_file_patterns():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, target=["a.*"])
    assert len(comp.diffs) == 1
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    _assert_a_diff_between_one_and_two_is_correct(a_diff)

    assert a_diff.line_diff in str(comp)


def test_diff_file_trees_target_folder_patterns():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, target=["directory/*"])
    assert len(comp.diffs) == NUM_SUBDIRECTORY_DIFFS
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    _assert_diffs_are_correct(comp, exclude=MAIN_FOLDER_E2E_FILES)


def test_diff_file_trees_ignore_with_negation():
    comp = diff_file_trees(
        FILE_TREE_ONE, FILE_TREE_TWO, ignore=["directory/", "!directory/"]
    )
    assert len(comp.diffs) == ALL_DIFFS
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    _assert_diffs_are_correct(comp)


def test_diff_file_trees_target_with_negation():
    comp = diff_file_trees(
        FILE_TREE_ONE, FILE_TREE_TWO, ignore=["directory/", "!directory/"]
    )
    assert len(comp.diffs) == ALL_DIFFS
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    _assert_diffs_are_correct(comp)


def _assert_diffs_are_correct(
    comp: FileTreeComparison, exclude: Sequence[E2ETestFile] = tuple()
):
    comp_str = str(comp)

    for e2e_file in ALL_E2E_FILES:
        diff = comp.diff_for(e2e_file.value)
        if e2e_file in exclude:
            assert diff is None
        else:
            e2e_file.assert_diff_is_correct(diff)
            assert diff.line_diff in comp_str


def _assert_a_diff_between_one_and_two_is_correct(diff: Optional[FileDiff]):
    assert diff is not None
    assert diff.exists_in_dir1 is True
    assert diff.exists_in_dir2 is True
    assert "@@ -1,2 +1,2 @@\n A\n-one\n+two" in diff.line_diff
    assert E2ETestFile.A.value in diff.line_diff


def _assert_b_diff_between_one_and_two_is_correct(diff: Optional[FileDiff]):
    assert diff is not None
    assert diff.exists_in_dir1 is True
    assert diff.exists_in_dir2 is False
    assert "@@ -1,2 +0,0 @@\n-B\n-one" in diff.line_diff
    assert E2ETestFile.B.value in diff.line_diff


def _assert_c_diff_between_one_and_two_is_correct(diff: Optional[FileDiff]):
    assert diff is not None
    assert diff.exists_in_dir1 is False
    assert diff.exists_in_dir2 is True
    assert "@@ -0,0 +1,2 @@\n+C\n+two" in diff.line_diff
    assert E2ETestFile.C.value in diff.line_diff


def _assert_d_diff_between_one_and_two_is_correct(diff: Optional[FileDiff]):
    assert diff is not None
    assert diff.exists_in_dir1 is True
    assert diff.exists_in_dir2 is True
    assert "@@ -1,2 +1,2 @@\n D\n-one\n+two" in diff.line_diff
    assert E2ETestFile.D.value in diff.line_diff


def _assert_e_diff_between_one_and_two_is_correct(diff: Optional[FileDiff]):
    assert diff is not None
    assert diff.exists_in_dir1 is True
    assert diff.exists_in_dir2 is False
    assert "@@ -1,2 +0,0 @@\n-E\n-one" in diff.line_diff
    assert E2ETestFile.E.value in diff.line_diff


def _assert_f_diff_between_one_and_two_is_correct(diff: Optional[FileDiff]):
    assert diff is not None
    assert diff.exists_in_dir1 is False
    assert diff.exists_in_dir2 is True
    assert "@@ -0,0 +1,2 @@\n+F\n+two" in diff.line_diff
    assert E2ETestFile.F.value in diff.line_diff


def _assert_image_diff_between_one_and_two_is_correct(diff: Optional[FileDiff]):
    assert diff is not None
    assert diff.exists_in_dir1 is True
    assert diff.exists_in_dir2 is True
    assert "Binary files" in diff.line_diff
    assert E2ETestFile.IMAGE.value in diff.line_diff


def _assert_image_removed_between_one_and_two_is_correct(
    diff: Optional[FileDiff],
):
    assert diff is not None
    assert diff.exists_in_dir1 is True
    assert diff.exists_in_dir2 is False
    assert "Binary files" in diff.line_diff
    assert E2ETestFile.REMOVED_IMAGE.value in diff.line_diff
    assert "one" in diff.line_diff


def _assert_image_added_between_one_and_two_is_correct(
    diff: Optional[FileDiff],
):
    assert diff is not None
    assert diff.exists_in_dir1 is False
    assert diff.exists_in_dir2 is True
    assert "Binary files" in diff.line_diff
    assert E2ETestFile.ADDED_IMAGE.value in diff.line_diff
    assert "two" in diff.line_diff
