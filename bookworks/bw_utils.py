"""
Utility functions for bookworks.
"""

import re
import tempfile
import subprocess
import os
from typing import Tuple, Optional, Dict, Any


def epub_to_markdown(epub_path: str) -> str:
    """
    Convert an EPUB file to Markdown. This is primarily a wrapper around the pandoc command.
    However, it also handles some additional cleanup of the markdown output.

    """
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_md_file:
        temp_md_path = temp_md_file.name

    try:
        cmd = [
            "pandoc",
            epub_path,
            "-f",
            "epub",
            "-t",
            "markdown",
            "-o",
            temp_md_path,
            "--wrap=none",
        ]
        subprocess.run(cmd, check=True)
        with open(temp_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        os.unlink(temp_md_path)  # Delete the temporary file
        return content
    except Exception as e:
        if os.path.exists(temp_md_path):
            os.unlink(temp_md_path)
        raise RuntimeError(f"Failed to convert EPUB to markdown: {str(e)}")


def sanitize_filename(title: str) -> str:
    """
    Sanitize a filename by removing or replacing problematic characters.

    Args:
        title: The filename to sanitize

    Returns:
        A sanitized filename safe for use in file systems
    """
    # Remove or replace characters that could cause issues in filenames
    # Replace newlines and other problematic characters with hyphens
    sanitized = re.sub(r'[\r\n\t/\\:*?"<>|]', "-", title)
    # Replace multiple hyphens with single hyphen
    sanitized = re.sub(r"-+", "-", sanitized)
    # Remove leading/trailing hyphens and spaces
    sanitized = sanitized.strip("- ")
    return sanitized or "untitled"


def clean_markdown_content(content: str) -> Tuple[str, Dict[str, Any]]:
    """
    Clean and process markdown content, extracting metadata and fixing common issues.

    Args:
        content: Raw markdown content

    Returns:
        Tuple containing (processed_content, metadata_dict)
    """
    metadata = {}

    # Extract the title from the first h1 heading
    title_match = re.search(r"^# (.*?)$", content, re.MULTILINE)
    metadata["title"] = title_match.group(1) if title_match else "Untitled Document"

    # First, normalize line endings
    content = content.replace("\r\n", "\n")

    # Fix multi-line links by first finding all link patterns
    def clean_link(match):
        text = match.group(1)
        url = match.group(2)
        # Clean the link text by replacing newlines and multiple spaces with a single space
        cleaned_text = " ".join(text.split())
        return f"[{cleaned_text}]({url})"

    # Fix links first - match [text](url) where text can contain newlines
    modified_links = re.sub(r"\[([\s\S]*?)\]\((.*?)\)", clean_link, content)

    # Add extra newline after paragraphs but not after headings or list items
    lines = modified_links.split("\n")
    result = []

    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:  # Empty line
            result.append("")
            continue

        # Check if this line starts a heading or list item
        is_special = line.strip().startswith(("#", "*", "-", "+"))
        # Check if next line exists and is empty
        next_is_empty = (i + 1 >= len(lines)) or not lines[i + 1].strip()

        if is_special or next_is_empty:
            result.append(line)
        else:
            result.append(line + "\n")

    modified_content = "\n".join(result)

    return modified_content, metadata


def run_pandoc_command(
    input_file: str, output_file: str, options: Dict[str, Any]
) -> Tuple[bool, Optional[str]]:
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
            return False, f"Pandoc error: {result.stderr}"
        return True, None
    except Exception as e:
        return False, f"Error running pandoc: {str(e)}"


def create_temp_workspace() -> tempfile.TemporaryDirectory:
    """
    Create a temporary workspace directory for processing files.

    Returns:
        TemporaryDirectory object that will clean up automatically
    """
    return tempfile.TemporaryDirectory()


def clean_markdown_for_tts(content: str) -> str:
    """Clean markdown content to make it suitable for TTS reading.

    This function should remove extra markdown/HTML markup (e.g. markdown ID references,
    HTML blocks, extra attributes, and formatting markers) as tested in our experiments.

    Args:
        content (str): The raw markdown content.

    Returns:
        str: The cleaned, TTS-ready markdown content.
    """
    # Remove markdown ID references like []{#title_page.xhtml}
    content = re.sub(r"\[\]\{#[^}]+\}", "", content)

    # Remove HTML blocks (e.g., blocks like ```{=html} ... ```)
    content = re.sub(r"```\{=html\}[\s\S]*?```", "", content)

    # Remove section formatting (e.g. ::: {attributes} etc.)
    content = re.sub(r"::: \{[^}]+\}", "", content)
    content = re.sub(r":::.*", "", content)

    # Clean up headings by stripping out attributes (keeping the heading text)
    content = re.sub(r"(#+ .*?) \{[^}]+\}", r"\1", content)

    # Remove image references as in the experiments
    content = re.sub(r"!\[\]\([^)]+\)", "", content)
    content = re.sub(r"\{\.x-ebookmaker-cover\}", "", content)

    # Remove HTML IDs in brackets and inline IDs (e.g. {#id})
    content = re.sub(r"\{\#[^}]+\}", "", content)

    # Remove attributes in square brackets (e.g. [text]{...})
    content = re.sub(r"\[.*?\]\{[^}]+\}", "", content)

    # Remove language attributes
    content = re.sub(r"lang=\"[^\"]+\"", "", content)

    # Convert links to only display text (strip the URL)
    content = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", content)

    # Remove HTML tags entirely
    content = re.sub(r"<[^>]+>", "", content)

    # Remove any remaining attributes within curly braces
    content = re.sub(r"\{[^}]+\}", "", content)

    # Convert formatting (like **bold**, *italic*, __bold__, _italic_) to plain text
    content = re.sub(r"\*\*([^*]+)\*\*", r"\1", content)
    content = re.sub(r"\*([^*]+)\*", r"\1", content)
    content = re.sub(r"__([^_]+)__", r"\1", content)
    content = re.sub(r"_([^_]+)_", r"\1", content)

    # Remove reference-style links (e.g. [^something])
    content = re.sub(r"\[\^[^\]]+\]", "", content)

    # Clean up navigation markers (e.g. numbers or bullets at line starts)
    content = re.sub(r"^\d+\.\s+", "", content, flags=re.MULTILINE)

    # Remove backslashes used for escaping
    content = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", r"\1", content)

    # Remove multiple backslashes (like \\\\)
    content = re.sub(r"\\{2,}", "", content)

    # Remove Project Gutenberg boilerplate markers
    content = re.sub(
        r"START OF THE PROJECT GUTENBERG EBOOK.*", "", content, flags=re.IGNORECASE
    )
    content = re.sub(
        r"END OF THE PROJECT GUTENBERG EBOOK.*", "", content, flags=re.IGNORECASE
    )

    # Clean up excessive blank lines and extra spaces
    content = re.sub(r"\\$", "", content, flags=re.MULTILINE)
    content = re.sub(r"  +", " ", content)
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip()


def split_by_chapters(content: str, book_title: str) -> list:
    """Split cleaned markdown content into chapters using header patterns.
    Returns a list of dictionaries in the form:
    [{"title": chapter_title, "content": chapter_content}, ...]
    """
    chapter_pattern = re.compile(r"^#{1,2}\s+(.*?)$", re.MULTILINE)
    chapter_matches = list(chapter_pattern.finditer(content))
    if not chapter_matches:
        return [{"title": book_title, "content": content}]
    chapters = []
    for i, match in enumerate(chapter_matches):
        chapter_start = match.start()
        chapter_title = match.group(1).strip()
        chapter_end = (
            chapter_matches[i + 1].start()
            if i < len(chapter_matches) - 1
            else len(content)
        )
        chapter_content = content[chapter_start:chapter_end].strip()
        chapters.append({"title": chapter_title, "content": chapter_content})
    return chapters
