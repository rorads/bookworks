"""
Tests for audio processing functionality.
"""

import pytest
from pathlib import Path

from bookworks.audio.tts import TTSProcessor


def test_tts_processor_initialization(tmp_path):
    """Test that TTSProcessor can be initialized."""
    processor = TTSProcessor(str(tmp_path))
    assert processor is not None


def test_tts_process_empty_content(tmp_path):
    """Test processing empty content."""
    processor = TTSProcessor(str(tmp_path))
    output_file, error = processor.process("", "Empty Book")
    assert output_file == ""
    assert error is None


def test_tts_processor_prepare_content(tmp_path, sample_markdown):
    """Test preparation of content for TTS processing."""
    processor = TTSProcessor(str(tmp_path))
    chapters = processor.prepare_content(sample_markdown, "Sample Book")
    assert len(chapters) > 0
    assert all("file_path" in chapter for chapter in chapters)
    assert all(Path(chapter["file_path"]).exists() for chapter in chapters)


def test_tts_processor_chapter_naming(tmp_path):
    """Test chapter file naming and organization."""
    processor = TTSProcessor(str(tmp_path))
    content = """# Test Book

## Chapter 1: Special/Characters

Some content.

## Chapter 2: Normal Name

More content.
"""
    chapters = processor.prepare_content(content, "Test Book")
    assert len(chapters) == 2
    assert "Special-Characters" in chapters[0]["file_path"]
    assert "Normal-Name" in chapters[1]["file_path"]


def test_tts_processor_content_cleaning(tmp_path):
    """Test that content is properly cleaned in output files."""
    processor = TTSProcessor(str(tmp_path))
    content = """# Test Book

## Chapter 1

**Bold** and *italic* text.
[Link](http://example.com)
```{=html}
<div>HTML content</div>
```
[]{#some_id}
"""
    chapters = processor.prepare_content(content, "Test Book")
    assert len(chapters) == 1
    with open(chapters[0]["file_path"]) as f:
        cleaned = f.read()
    assert "**" not in cleaned
    assert "*" not in cleaned
    assert "[Link]" not in cleaned
    assert "<div>" not in cleaned
    assert "#some_id" not in cleaned


def test_tts_processor_empty_content(tmp_path):
    """Test handling of empty or minimal content."""
    processor = TTSProcessor(str(tmp_path))
    content = "# Test Book\n\n"
    chapters = processor.prepare_content(content, "Test Book")
    assert len(chapters) == 0  # Should skip empty content


@pytest.fixture
def sample_markdown():
    """Sample markdown content for testing."""
    return """# Sample Book

## Chapter 1: Introduction

This is a test chapter with some **bold** and *italic* text.
It also includes different formatting:
- List item 1
- List item 2

```{=html}
<div>Some HTML content</div>
```

[]{#some_id}
"""
