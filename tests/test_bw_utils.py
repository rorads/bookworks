"""
Tests for the bookworks utility functions.
"""

import os
from bookworks.bw_utils import (
    sanitize_filename,
    clean_markdown_content,
    run_pandoc_command,
    create_temp_workspace,
)


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


def test_clean_markdown_content():
    """Test markdown content cleaning and metadata extraction"""
    # Test with title and normal content
    content = """# Test Title
This is a paragraph.
Another line in same paragraph.

## Section
* List item 1
* List item 2"""

    cleaned, metadata = clean_markdown_content(content)
    assert metadata["title"] == "Test Title"

    # Split the cleaned content into lines for easier testing
    lines = cleaned.split("\n")

    # Check that title is preserved
    assert lines[0] == "# Test Title"

    # Check that paragraphs are properly separated
    paragraph_idx = lines.index("This is a paragraph.")
    assert lines[paragraph_idx + 1] == ""
    assert lines[paragraph_idx + 2] == "Another line in same paragraph."

    # Check that sections are properly separated
    section_idx = lines.index("## Section")
    assert lines[section_idx - 1] == ""

    # Check that list items are properly formatted
    list_start_idx = lines.index("* List item 1")
    assert lines[list_start_idx + 1] == "* List item 2"

    # Test with multi-line links
    content = """# Link Test
[This is a
multi-line
link](https://example.com)"""

    cleaned, metadata = clean_markdown_content(content)
    assert metadata["title"] == "Link Test"
    assert "[This is a multi-line link](https://example.com)" in cleaned

    # Test without title
    content = "Just some content\nwithout a title"
    cleaned, metadata = clean_markdown_content(content)
    assert metadata["title"] == "Untitled Document"
    assert "Just some content\n\nwithout a title" in cleaned


def test_run_pandoc_command(tmp_path):
    """Test pandoc command execution"""
    # Create a test markdown file
    input_file = tmp_path / "test.md"
    input_file.write_text("# Test\nContent")

    output_file = tmp_path / "test.epub"

    options = {
        "metadata": {"title": "Test", "author": "Test Author", "date": "2024-03-12"},
        "epub_chapter_level": 2,
        "toc": True,
        "standalone": True,
    }

    success, error = run_pandoc_command(str(input_file), str(output_file), options)
    assert success
    assert error is None
    assert output_file.exists()

    # Test with invalid input file
    success, error = run_pandoc_command("nonexistent.md", str(output_file), options)
    assert not success
    assert error is not None


def test_create_temp_workspace():
    """Test temporary workspace creation"""
    with create_temp_workspace() as temp_dir:
        assert os.path.exists(temp_dir)
        # Create a test file in the workspace
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        assert os.path.exists(test_file)

    # After the context manager exits, the directory should be cleaned up
    assert not os.path.exists(temp_dir)
