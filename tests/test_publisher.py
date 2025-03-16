"""
Tests for the markdown to epub conversion functionality.
"""

import pytest
import os
import shutil
from bookworks.utils.helpers import sanitize_filename
from bookworks.core.publisher import (
    process_markdown_content,
    process_markdown_file,
    UPLOAD_FOLDER,
)


@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup test environment and cleanup after each test"""
    # Setup
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    yield

    # Cleanup
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def test_sanitize_filename():
    """Test filename sanitization function"""
    # Test basic sanitization
    assert sanitize_filename("Hello World") == "Hello World"

    # Test problematic characters
    assert sanitize_filename("file/with\\bad:chars?*") == "file-with-bad-chars"

    # Test multiple hyphens
    assert sanitize_filename("multiple---hyphens") == "multiple-hyphens"

    # Test leading/trailing spaces and hyphens
    assert sanitize_filename(" - test - ") == "test"

    # Test empty or invalid input
    assert sanitize_filename("") == "untitled"
    assert sanitize_filename("   ") == "untitled"
    assert sanitize_filename("---") == "untitled"


def test_process_markdown_content_basic():
    """Test basic markdown to epub conversion"""
    content = """# Test Title
This is a paragraph.
Another line in the same paragraph.

## Section
* List item 1
* List item 2"""

    output_file, error = process_markdown_content(content, author="Test Author")
    assert error is None
    assert output_file.endswith(".epub")
    assert os.path.exists(output_file)
    os.remove(output_file)


def test_process_markdown_content_links():
    """Test markdown processing with multi-line links"""
    content = """# Link Test
[This is a
multi-line
link](https://example.com)"""

    output_file, error = process_markdown_content(content)
    assert error is None
    assert output_file.endswith(".epub")
    assert os.path.exists(output_file)
    os.remove(output_file)


def test_process_markdown_content_no_title():
    """Test processing markdown without a title"""
    content = "Just some content\nwithout a title"
    output_file, error = process_markdown_content(content)
    assert error is None
    assert output_file == os.path.join(UPLOAD_FOLDER, "Untitled Document.epub")
    assert os.path.exists(output_file)
    os.remove(output_file)


def test_process_markdown_content_with_options():
    """Test epub conversion with different options"""
    content = """# Test Options
## Section 1
Content 1
## Section 2
Content 2"""

    # Test with TOC disabled
    output_file, error = process_markdown_content(content, toc=False)
    assert error is None
    assert os.path.exists(output_file)
    os.remove(output_file)

    # Test with debug mode
    output_file, error = process_markdown_content(content, debug=True)
    assert error is None
    assert os.path.exists(output_file)

    # Get the directory of the output file
    output_dir = os.path.dirname(os.path.abspath(output_file))
    base_name = os.path.splitext(os.path.basename(output_file))[0]
    md_file = os.path.join(output_dir, f"{base_name}_processed.md")

    # In debug mode, the processed markdown file should exist
    assert os.path.exists(md_file)

    # Clean up
    os.remove(output_file)
    os.remove(md_file)


@pytest.fixture
def temp_markdown_file(tmp_path):
    """Create a temporary markdown file for testing"""
    content = """# Temp Test
This is a test file.
## Section
* Item 1
* Item 2"""
    file_path = tmp_path / "test.md"
    file_path.write_text(content)
    return str(file_path)


def test_process_markdown_file(temp_markdown_file):
    """Test processing a markdown file to epub"""
    output_file, error = process_markdown_file(temp_markdown_file, author="Test Author")
    assert error is None
    assert output_file.endswith(".epub")
    assert os.path.exists(output_file)
    os.remove(output_file)


def test_process_markdown_file_not_found():
    """Test processing a non-existent file"""
    output_file, error = process_markdown_file("nonexistent.md")
    assert error is not None
    assert output_file is None
