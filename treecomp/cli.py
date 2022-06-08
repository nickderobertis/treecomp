from pathlib import Path
from typing import List, Optional

import typer

from treecomp import diff_file_trees

cli = typer.Typer()


@cli.command()
def cli_diff_file_trees(
    dir1: Path = typer.Argument(..., help="Path to the first directory to compare."),
    dir2: Path = typer.Argument(..., help="Path to the second directory to compare."),
    ignore: Optional[List[str]] = typer.Option(
        None,
        "-i",
        "--ignore",
        help="Paths to ignore. The flag can be passed multiple times to exclude multiple paths.",
    ),
    exclude_default_ignores: bool = typer.Option(
        False,
        "-e",
        "--exclude-default-ignores",
        help="Exclude default ignores.",
        show_default=False,
    ),
):
    """
    Compare two directories and print a unified diff
    """
    comparison = diff_file_trees(
        dir1, dir2, ignore=ignore, include_default_ignores=not exclude_default_ignores
    )
    print(comparison)


if __name__ == "__main__":
    cli()
