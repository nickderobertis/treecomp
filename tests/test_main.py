from typing import Optional

from tests.config import FILE_TREE_ONE, FILE_TREE_TWO
from treecomp import diff_file_trees
from treecomp.main import FileDiffWithDirs


def test_diff_file_trees():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO)
    assert len(comp.diffs) == 3
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    _assert_a_diff_between_one_and_two_is_correct(a_diff)

    b_diff = comp.diff_for("b.txt")
    _assert_b_diff_between_one_and_two_is_correct(b_diff)

    c_diff = comp.diff_for("c.txt")
    _assert_c_diff_between_one_and_two_is_correct(c_diff)

    assert a_diff.diff.line_diff in str(comp)
    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)


def test_diff_file_tress_ignore_file():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["a.txt"])
    assert len(comp.diffs) == 2
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    assert a_diff is None

    b_diff = comp.diff_for("b.txt")
    _assert_b_diff_between_one_and_two_is_correct(b_diff)

    c_diff = comp.diff_for("c.txt")
    _assert_c_diff_between_one_and_two_is_correct(c_diff)

    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)


def _assert_a_diff_between_one_and_two_is_correct(diff: Optional[FileDiffWithDirs]):
    assert diff is not None
    assert diff.diff.exists_in_dir1 is True
    assert diff.diff.exists_in_dir2 is True
    assert "@@ -1,2 +1,2 @@\n A\n-one\n+two" in diff.diff.line_diff
    assert "a.txt" in diff.diff.line_diff


def _assert_b_diff_between_one_and_two_is_correct(diff: Optional[FileDiffWithDirs]):
    assert diff is not None
    assert diff.diff.exists_in_dir1 is True
    assert diff.diff.exists_in_dir2 is False
    assert "@@ -0,0 +1,2 @@\n+B\n+one" in diff.diff.line_diff
    assert "b.txt" in diff.diff.line_diff


def _assert_c_diff_between_one_and_two_is_correct(diff: Optional[FileDiffWithDirs]):
    assert diff is not None
    assert diff.diff.exists_in_dir1 is False
    assert diff.diff.exists_in_dir2 is True
    assert "@@ -0,0 +1,2 @@\n+C\n+two" in diff.diff.line_diff
    assert "c.txt" in diff.diff.line_diff
