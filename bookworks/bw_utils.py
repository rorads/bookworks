"""
Utility functions for bookworks.
"""

import os
import re
import tempfile
import subprocess
from typing import Tuple, Optional, Dict, Any

def epub_to_markdown(epub_path: str) -> str:
    """
    Convert an EPUB file to Markdown. This is primarily a wrapper around the pandoc command.
    However, it also handles some additional cleanup of the markdown output.

    """
    pass


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
    sanitized = re.sub(r'[\r\n\t/\\:*?"<>|]', '-', title)
    # Replace multiple hyphens with single hyphen
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens and spaces
    sanitized = sanitized.strip('- ')
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
    title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
    metadata['title'] = title_match.group(1) if title_match else "Untitled Document"
    
    # First, normalize line endings
    content = content.replace('\r\n', '\n')
    
    # Fix multi-line links by first finding all link patterns
    def clean_link(match):
        text = match.group(1)
        url = match.group(2)
        # Clean the link text by replacing newlines and multiple spaces with a single space
        cleaned_text = ' '.join(text.split())
        return f"[{cleaned_text}]({url})"
    
    # Fix links first - match [text](url) where text can contain newlines
    modified_links = re.sub(r'\[([\s\S]*?)\]\((.*?)\)', clean_link, content)
    
    # Add extra newline after paragraphs but not after headings or list items
    lines = modified_links.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:  # Empty line
            result.append('')
            continue
            
        # Check if this line starts a heading or list item
        is_special = line.strip().startswith(('#', '*', '-', '+'))
        # Check if next line exists and is empty
        next_is_empty = (i + 1 >= len(lines)) or not lines[i + 1].strip()
        
        if is_special or next_is_empty:
            result.append(line)
        else:
            result.append(line + '\n')
    
    modified_content = '\n'.join(result)
    
    return modified_content, metadata

def run_pandoc_command(input_file: str, output_file: str, options: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
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
    for key, value in options.get('metadata', {}).items():
        command.extend([f"--metadata={key}:{value}"])
    
    # Add other options
    if options.get('toc', False):
        command.extend(["--toc", "--toc-depth=3"])
    
    if options.get('epub_chapter_level'):
        command.extend([f"--epub-chapter-level={options['epub_chapter_level']}"])
    
    if options.get('standalone', False):
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

