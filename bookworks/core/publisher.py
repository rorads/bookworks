"""NEW FILE: bookworks/core/publisher.py

Convert Markdown files to EPUB format with enhanced formatting and structure.

This module replaces the old md_publish.py and uses utility functions from the new
bookworks/utils/helpers.py module.
"""

import os
import datetime
from typing import Tuple, Optional

from bookworks.utils.helpers import (
    sanitize_filename,
    clean_markdown_content,
    run_pandoc_command,
    create_temp_workspace,
)

UPLOAD_FOLDER = os.path.abspath("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def process_markdown_content(
    content: str,
    author: str = "Author Not Specified",
    debug: bool = False,
    toc: bool = True,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Process markdown content and convert it to EPUB format.

    Args:
        content: The markdown content to process
        author: The author name to include in the metadata
        debug: Whether to keep intermediate files for debugging
        toc: Whether to include a table of contents

    Returns:
        Tuple containing (output_file_path, error_message).
        If successful, error_message will be None.
    """
    try:
        modified_content, metadata = clean_markdown_content(content)
        title = metadata.get("title", "Untitled Document")
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        with create_temp_workspace() as temp_dir:
            safe_title = sanitize_filename(title)
            processed_md = os.path.join(temp_dir, f"{safe_title}_processed.md")
            with open(processed_md, "w") as f:
                f.write(modified_content)
            output_epub = os.path.join(temp_dir, f"{safe_title}.epub")
            pandoc_options = {
                "metadata": {"title": title, "author": author, "date": today_date},
                "epub_chapter_level": 2,
                "toc": toc,
                "standalone": True,
            }
            success, error = run_pandoc_command(
                processed_md, output_epub, pandoc_options
            )
            if not success:
                return None, error
            final_output = os.path.join(UPLOAD_FOLDER, f"{safe_title}.epub")
            os.rename(output_epub, final_output)
            if debug:
                debug_md = os.path.join(UPLOAD_FOLDER, f"{safe_title}_processed.md")
                os.rename(processed_md, debug_md)
            return final_output, None
    except Exception as e:
        return None, f"Error processing markdown: {str(e)}"


def process_markdown_file(
    filepath: str,
    author: str = "Author Not Specified",
    debug: bool = False,
    toc: bool = True,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Process a markdown file and convert it to EPUB format.

    Args:
        filepath: Path to the markdown file
        author: The author name to include in the metadata
        debug: Whether to keep intermediate files for debugging
        toc: Whether to include a table of contents

    Returns:
        Tuple containing (output_file_path, error_message).
        If successful, error_message will be None.
    """
    try:
        if not os.path.exists(filepath):
            return None, f"File not found: {filepath}"
        with open(filepath, "r") as f:
            content = f.read()
        return process_markdown_content(content, author, debug, toc)
    except Exception as e:
        return None, f"Error processing file: {str(e)}"
