from pathlib import Path
from typing import Optional

import typer

from treecomp import diff_file_trees

cli = typer.Typer()


@cli.command()
def cli_diff_file_trees(
    dir1: Path = typer.Argument(..., help="Path to the first directory to compare."),
    dir2: Path = typer.Argument(..., help="Path to the second directory to compare."),
    ignore: Optional[str] = typer.Option(
        None,
        "-i",
        "--ignore",
        help="Comma-separated paths to ignore. .gitignore-style syntax is supported.",
    ),
    target: Optional[str] = typer.Option(
        None,
        "-t",
        "--target",
        help="Comma-separated paths to target. .gitignore-style syntax is supported.",
    ),
):
    """
    Compare two directories and print a unified diff
    """
    comparison = diff_file_trees(
        dir1,
        dir2,
        ignore=ignore.split(",") if ignore else None,
        target=target.split(",") if target else None,
    )
    print(comparison)


if __name__ == "__main__":
    cli()
