from typing import Optional

from tests.config import FILE_TREE_ONE, FILE_TREE_TWO
from treecomp import diff_file_trees
from treecomp.main import FileDiffWithDirs


def test_diff_file_trees():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO)
    assert len(comp.diffs) == 6
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    _assert_a_diff_between_one_and_two_is_correct(a_diff)

    b_diff = comp.diff_for("b.txt")
    _assert_b_diff_between_one_and_two_is_correct(b_diff)

    c_diff = comp.diff_for("c.txt")
    _assert_c_diff_between_one_and_two_is_correct(c_diff)

    d_diff = comp.diff_for("directory/d.txt")
    _assert_d_diff_between_one_and_two_is_correct(d_diff)

    e_diff = comp.diff_for("directory/e.txt")
    _assert_e_diff_between_one_and_two_is_correct(e_diff)

    f_diff = comp.diff_for("directory/f.txt")
    _assert_f_diff_between_one_and_two_is_correct(f_diff)

    assert a_diff.diff.line_diff in str(comp)
    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)
    assert d_diff.diff.line_diff in str(comp)
    assert e_diff.diff.line_diff in str(comp)
    assert f_diff.diff.line_diff in str(comp)


def test_diff_file_trees_ignore_file():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["a.txt", "e.txt"])
    assert len(comp.diffs) == 4
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    assert a_diff is None

    b_diff = comp.diff_for("b.txt")
    _assert_b_diff_between_one_and_two_is_correct(b_diff)

    c_diff = comp.diff_for("c.txt")
    _assert_c_diff_between_one_and_two_is_correct(c_diff)

    d_diff = comp.diff_for("directory/d.txt")
    _assert_d_diff_between_one_and_two_is_correct(d_diff)

    e_diff = comp.diff_for("directory/e.txt")
    assert e_diff is None

    f_diff = comp.diff_for("directory/f.txt")
    _assert_f_diff_between_one_and_two_is_correct(f_diff)

    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)
    assert d_diff.diff.line_diff in str(comp)
    assert f_diff.diff.line_diff in str(comp)


def test_diff_file_trees_ignore_directory():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["directory"])
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

    d_diff = comp.diff_for("directory/d.txt")
    assert d_diff is None

    e_diff = comp.diff_for("directory/e.txt")
    assert e_diff is None

    f_diff = comp.diff_for("directory/f.txt")
    assert f_diff is None

    assert a_diff.diff.line_diff in str(comp)
    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)


def test_diff_file_trees_ignore_glob_file_patterns():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["*.txt"])
    assert len(comp.diffs) == 0
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO


def test_diff_file_trees_ignore_glob_folder_patterns():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, ignore=["directory/*"])
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

    d_diff = comp.diff_for("directory/d.txt")
    assert d_diff is None

    e_diff = comp.diff_for("directory/e.txt")
    assert e_diff is None

    f_diff = comp.diff_for("directory/f.txt")
    assert f_diff is None

    assert a_diff.diff.line_diff in str(comp)
    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)


def test_diff_file_trees_target_files():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, target=["a.txt"])
    assert len(comp.diffs) == 1
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    _assert_a_diff_between_one_and_two_is_correct(a_diff)

    assert a_diff.diff.line_diff in str(comp)


def test_diff_file_trees_target_folders():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, target=["directory"])
    assert len(comp.diffs) == 3
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    d_diff = comp.diff_for("directory/d.txt")
    _assert_d_diff_between_one_and_two_is_correct(d_diff)

    e_diff = comp.diff_for("directory/e.txt")
    _assert_e_diff_between_one_and_two_is_correct(e_diff)

    f_diff = comp.diff_for("directory/f.txt")
    _assert_f_diff_between_one_and_two_is_correct(f_diff)

    assert d_diff.diff.line_diff in str(comp)
    assert e_diff.diff.line_diff in str(comp)
    assert f_diff.diff.line_diff in str(comp)


def test_diff_file_trees_target_file_patterns():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, target=["a.*"])
    assert len(comp.diffs) == 1
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    _assert_a_diff_between_one_and_two_is_correct(a_diff)

    assert a_diff.diff.line_diff in str(comp)


def test_diff_file_trees_target_folder_patterns():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO, target=["directory/*"])
    assert len(comp.diffs) == 3
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    d_diff = comp.diff_for("directory/d.txt")
    _assert_d_diff_between_one_and_two_is_correct(d_diff)

    e_diff = comp.diff_for("directory/e.txt")
    _assert_e_diff_between_one_and_two_is_correct(e_diff)

    f_diff = comp.diff_for("directory/f.txt")
    _assert_f_diff_between_one_and_two_is_correct(f_diff)

    assert d_diff.diff.line_diff in str(comp)
    assert e_diff.diff.line_diff in str(comp)
    assert f_diff.diff.line_diff in str(comp)


def test_diff_file_trees_ignore_with_negation():
    comp = diff_file_trees(
        FILE_TREE_ONE, FILE_TREE_TWO, ignore=["directory/", "!directory/"]
    )
    assert len(comp.diffs) == 6
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    _assert_a_diff_between_one_and_two_is_correct(a_diff)

    b_diff = comp.diff_for("b.txt")
    _assert_b_diff_between_one_and_two_is_correct(b_diff)

    c_diff = comp.diff_for("c.txt")
    _assert_c_diff_between_one_and_two_is_correct(c_diff)

    d_diff = comp.diff_for("directory/d.txt")
    _assert_d_diff_between_one_and_two_is_correct(d_diff)

    e_diff = comp.diff_for("directory/e.txt")
    _assert_e_diff_between_one_and_two_is_correct(e_diff)

    f_diff = comp.diff_for("directory/f.txt")
    _assert_f_diff_between_one_and_two_is_correct(f_diff)

    assert a_diff.diff.line_diff in str(comp)
    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)
    assert d_diff.diff.line_diff in str(comp)
    assert e_diff.diff.line_diff in str(comp)
    assert f_diff.diff.line_diff in str(comp)


def test_diff_file_trees_target_with_negation():
    comp = diff_file_trees(
        FILE_TREE_ONE, FILE_TREE_TWO, ignore=["directory/", "!directory/"]
    )
    assert len(comp.diffs) == 6
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    _assert_a_diff_between_one_and_two_is_correct(a_diff)

    b_diff = comp.diff_for("b.txt")
    _assert_b_diff_between_one_and_two_is_correct(b_diff)

    c_diff = comp.diff_for("c.txt")
    _assert_c_diff_between_one_and_two_is_correct(c_diff)

    d_diff = comp.diff_for("directory/d.txt")
    _assert_d_diff_between_one_and_two_is_correct(d_diff)

    e_diff = comp.diff_for("directory/e.txt")
    _assert_e_diff_between_one_and_two_is_correct(e_diff)

    f_diff = comp.diff_for("directory/f.txt")
    _assert_f_diff_between_one_and_two_is_correct(f_diff)

    assert a_diff.diff.line_diff in str(comp)
    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)
    assert d_diff.diff.line_diff in str(comp)
    assert e_diff.diff.line_diff in str(comp)
    assert f_diff.diff.line_diff in str(comp)


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
    assert "@@ -1,2 +0,0 @@\n-B\n-one" in diff.diff.line_diff
    assert "b.txt" in diff.diff.line_diff


def _assert_c_diff_between_one_and_two_is_correct(diff: Optional[FileDiffWithDirs]):
    assert diff is not None
    assert diff.diff.exists_in_dir1 is False
    assert diff.diff.exists_in_dir2 is True
    assert "@@ -0,0 +1,2 @@\n+C\n+two" in diff.diff.line_diff
    assert "c.txt" in diff.diff.line_diff


def _assert_d_diff_between_one_and_two_is_correct(diff: Optional[FileDiffWithDirs]):
    assert diff is not None
    assert diff.diff.exists_in_dir1 is True
    assert diff.diff.exists_in_dir2 is True
    assert "@@ -1,2 +1,2 @@\n D\n-one\n+two" in diff.diff.line_diff
    assert "d.txt" in diff.diff.line_diff


def _assert_e_diff_between_one_and_two_is_correct(diff: Optional[FileDiffWithDirs]):
    assert diff is not None
    assert diff.diff.exists_in_dir1 is True
    assert diff.diff.exists_in_dir2 is False
    assert "@@ -1,2 +0,0 @@\n-E\n-one" in diff.diff.line_diff
    assert "e.txt" in diff.diff.line_diff


def _assert_f_diff_between_one_and_two_is_correct(diff: Optional[FileDiffWithDirs]):
    assert diff is not None
    assert diff.diff.exists_in_dir1 is False
    assert diff.diff.exists_in_dir2 is True
    assert "@@ -0,0 +1,2 @@\n+F\n+two" in diff.diff.line_diff
    assert "f.txt" in diff.diff.line_diff
