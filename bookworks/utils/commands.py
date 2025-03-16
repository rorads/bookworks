"""
Command execution utilities for bookworks.
"""

import subprocess
from typing import List, Dict, Any, Tuple, Optional

from ..core import ProcessingResult


def run_pandoc_command(
    input_file: str, output_file: str, options: Dict[str, Any]
) -> ProcessingResult:
    """
    Run a pandoc command with the given options.

    Args:
        input_file: Path to input file
        output_file: Path to output file
        options: Dictionary of pandoc options including metadata

    Returns:
        Tuple of (success, error_message)
    """
    command = ["pandoc", input_file, "-o", output_file]

    # Add metadata options
    for key, value in options.get("metadata", {}).items():
        command.extend([f"--metadata={key}:{value}"])

    # Add other options
    if options.get("toc", False):
        command.extend(["--toc", "--toc-depth=3"])

    if options.get("epub_chapter_level"):
        command.extend([f"--epub-chapter-level={options['epub_chapter_level']}"])

    if options.get("standalone", False):
        command.append("--standalone")

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return "", f"Pandoc error: {result.stderr}"
        return output_file, None
    except Exception as e:
        return "", f"Error running pandoc: {str(e)}"


def run_command(
    command: List[str], check: bool = True, capture_output: bool = True
) -> Tuple[int, Optional[str], Optional[str]]:
    """
    Run a shell command and return its output.

    Args:
        command: Command and arguments as list of strings
        check: Whether to raise an exception on non-zero return code
        capture_output: Whether to capture and return stdout/stderr

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command, check=check, capture_output=capture_output, text=True
        )
        return (
            result.returncode,
            result.stdout if capture_output else None,
            result.stderr if capture_output else None,
        )
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return e.returncode, e.stdout, e.stderr
