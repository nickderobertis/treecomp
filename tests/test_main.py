from tests.config import FILE_TREE_ONE, FILE_TREE_TWO
from treecomp import diff_file_trees


def test_diff_file_trees():
    comp = diff_file_trees(FILE_TREE_ONE, FILE_TREE_TWO)
    assert len(comp.diffs) == 3
    assert len(comp.could_not_diff) == 0
    assert comp.dir1 == FILE_TREE_ONE
    assert comp.dir2 == FILE_TREE_TWO

    a_diff = comp.diff_for("a.txt")
    assert a_diff is not None
    assert a_diff.diff.exists_in_dir1 is True
    assert a_diff.diff.exists_in_dir2 is True
    assert "@@ -1,2 +1,2 @@\n A\n-one\n+two" in a_diff.diff.line_diff
    assert "a.txt" in a_diff.diff.line_diff

    b_diff = comp.diff_for("b.txt")
    assert b_diff is not None
    assert b_diff.diff.exists_in_dir1 is True
    assert b_diff.diff.exists_in_dir2 is False
    assert "@@ -0,0 +1,2 @@\n+B\n+one" in b_diff.diff.line_diff
    assert "b.txt" in b_diff.diff.line_diff

    c_diff = comp.diff_for("c.txt")
    assert c_diff is not None
    assert c_diff.diff.exists_in_dir1 is False
    assert c_diff.diff.exists_in_dir2 is True
    assert "@@ -0,0 +1,2 @@\n+C\n+two" in c_diff.diff.line_diff
    assert "c.txt" in c_diff.diff.line_diff

    assert a_diff.diff.line_diff in str(comp)
    assert b_diff.diff.line_diff in str(comp)
    assert c_diff.diff.line_diff in str(comp)

