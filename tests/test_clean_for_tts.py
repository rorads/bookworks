import os
import subprocess
import pytest

from bookworks.bw_utils import clean_markdown_for_tts, split_by_chapters

SAMPLE_INPUT = """# Sample Book

## Chapter 1: A Very Long Chapter

This is a test. []{#test}
```{=html}
<div>HTML Content</div>
```
**Bold Text**
"""


def test_clean_markdown_for_tts():
    cleaned = clean_markdown_for_tts(SAMPLE_INPUT)
    # Assert that HTML blocks and markdown identifiers have been removed
    assert "```{=html}" not in cleaned
    assert "{#test}" not in cleaned
    # Bold formatting should be removed (converted to plain text)
    assert "**Bold Text**" not in cleaned
    # Check that the cleaned content does not contain HTML tags
    assert "<div>" not in cleaned


def test_split_by_chapters():
    cleaned = clean_markdown_for_tts(SAMPLE_INPUT)
    chapters = split_by_chapters(cleaned, "Sample Book")
    # Expect at least one chapter; if chapters are split, the first chapter title should contain 'Chapter 1'
    assert len(chapters) >= 1
    # Check that one of the chapters has a title containing 'Chapter 1'
    assert any("Chapter 1" in chapter["title"] for chapter in chapters)


# Integration test for the clean_for_tts.py script
@pytest.mark.integration
def test_clean_for_tts_integration(tmp_path):
    # Write sample input to a temporary file
    input_file = tmp_path / "sample.md"
    input_file.write_text(SAMPLE_INPUT, encoding="utf-8")

    # Run the clean_for_tts.py script using subprocess
    # Note: We assume the current working directory is the project root
    cmd = ["python", "-m", "bookworks.clean_for_tts", str(input_file)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check that the script ran successfully
    assert result.returncode == 0, (
        f"Script failed with output: {result.stdout}\nError: {result.stderr}"
    )

    # The output file should be created in output/tts-ready-markdown directory
    output_dir = os.path.abspath("output/tts-ready-markdown")
    # Determine expected output file name based on input file name
    expected_output_file = os.path.join(output_dir, "sample_tts.md")

    # Check that the output file exists
    assert os.path.exists(expected_output_file), (
        f"Expected output file {expected_output_file} not found."
    )

    # Optionally, check that the cleaned content does not contain unwanted substrings
    with open(expected_output_file, "r", encoding="utf-8") as f:
        cleaned_content = f.read()
    assert "```{=html}" not in cleaned_content
    assert "{#test}" not in cleaned_content
