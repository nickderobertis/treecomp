from enum import Enum
from pathlib import Path
from typing import Optional

import typer

from treecomp import diff_file_trees

cli = typer.Typer()


class OutputFormat(str, Enum):
    JSON = "json"
    TEXT = "text"


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
    output_format: OutputFormat = typer.Option(
        OutputFormat.TEXT,
        "-f",
        "--format",
        help="Output format.",
        show_choices=True,
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
    if output_format == OutputFormat.JSON:
        print(comparison.json())
    else:
        print(comparison)


if __name__ == "__main__":
    cli()
