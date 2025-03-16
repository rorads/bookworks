"""
Filesystem utilities for bookworks.
"""

import re
import tempfile
from pathlib import Path


def sanitize_filename(filename: str) -> str:
    """
    Convert a string into a safe filename.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    # Remove multiple underscores
    filename = re.sub(r"_+", "_", filename)
    # Limit length and remove trailing periods
    filename = filename[:255].rstrip(".")
    return filename


def create_temp_workspace() -> Path:
    """
    Create a temporary workspace directory.

    Returns:
        Path to the temporary directory
    """
    return Path(tempfile.mkdtemp(prefix="bookworks_"))


def run_pandoc_command(input_file: Path, output_file: Path, format_args: str) -> None:
    """
    Run a pandoc command to convert between formats.

    Args:
        input_file: Path to input file
        output_file: Path to output file
        format_args: Additional format arguments for pandoc
    """
    # TODO: Implement pandoc command execution
    pass
