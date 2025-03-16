"""Utility functions for bookworks.

This module replaces the older bw_utils.py and provides helper functions for processing markdown and running pandoc commands.
"""

import re
import tempfile
import subprocess
from typing import Tuple, Optional, Dict, Any


def sanitize_filename(title: str) -> str:
    """
    Sanitize a filename by removing or replacing problematic characters.

    Args:
        title: The filename to sanitize

    Returns:
        A sanitized filename safe for use in file systems
    """
    sanitized = re.sub(r'[\r\n\t/\\:*?"<>|]', "-", title)
    sanitized = re.sub(r"-+", "-", sanitized)
    sanitized = sanitized.strip("- ")
    return sanitized or "untitled"


def clean_markdown_content(content: str) -> Tuple[str, Dict[str, Any]]:
    """
    Clean and process markdown content, extracting metadata.

    Args:
        content: Raw markdown content

    Returns:
        Tuple containing (processed_content, metadata dictionary)
    """
    metadata = {}
    content = content.replace("\r\n", "\n")

    def clean_link(match: re.Match[str]) -> str:
        text = match.group(1)
        url = match.group(2)
        cleaned_text = " ".join(text.split())
        return f"[{cleaned_text}]({url})"

    modified_links = re.sub(r"\[([\s\S]*?)\]\((.*?)\)", clean_link, content)
    lines = modified_links.split("\n")
    result = []
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:
            result.append("")
            continue
        is_special = line.strip().startswith(("#", "*", "-", "+"))
        next_is_empty = (i + 1 >= len(lines)) or not lines[i + 1].strip()
        if is_special or next_is_empty:
            result.append(line)
        else:
            result.append(line + "\n")
    modified_content = "\n".join(result)
    title_match = re.search(r"^# (.*?)$", modified_content, re.MULTILINE)
    metadata["title"] = title_match.group(1) if title_match else "Untitled Document"
    return modified_content, metadata


def run_pandoc_command(
    input_file: str, output_file: str, options: Dict[str, Any]
) -> Tuple[bool, Optional[str]]:
    """
    Run pandoc to convert file formats with given options.

    Args:
        input_file: Path to the input file
        output_file: Path to the output file
        options: Dictionary containing pandoc options

    Returns:
        Tuple containing (success flag, error message if any)
    """
    command = ["pandoc", input_file, "-o", output_file]
    for key, value in options.get("metadata", {}).items():
        command.extend([f"--metadata={key}:{value}"])
    if options.get("toc", False):
        command.extend(["--toc", "--toc-depth=3"])
    if options.get("epub_chapter_level"):
        command.extend([f"--epub-chapter-level={options['epub_chapter_level']}"])
    if options.get("standalone", False):
        command.append("--standalone")
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return False, f"Pandoc error: {result.stderr}"
        return True, None
    except Exception as e:
        return False, f"Error running pandoc: {str(e)}"


def create_temp_workspace() -> tempfile.TemporaryDirectory:
    """
    Create a temporary directory for workspace.

    Returns:
        A TemporaryDirectory object
    """
    return tempfile.TemporaryDirectory()
