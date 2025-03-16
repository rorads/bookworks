"""
Tests for audio processing functionality.
"""

from pathlib import Path

from bookworks.audio.tts import TTSProcessor


def test_tts_processor_initialization():
    """Test that TTSProcessor can be initialized."""
    processor = TTSProcessor()
    assert processor is not None


def test_tts_process_empty_content():
    """Test processing empty content."""
    processor = TTSProcessor()
    result = processor.process("")
    assert result == ""


def test_tts_processor_prepare_content(temp_dir, sample_markdown):
    """Test preparation of content for TTS processing."""
    processor = TTSProcessor()
    results = processor.prepare_content(sample_markdown, "Sample Book", temp_dir)

    assert len(results) == 2
    assert all(isinstance(r["file_path"], str) for r in results)
    assert all(isinstance(r["word_count"], int) for r in results)
    assert all(Path(r["file_path"]).exists() for r in results)


def test_tts_processor_chapter_naming(temp_dir):
    """Test chapter file naming and organization."""
    processor = TTSProcessor()
    content = """# Test Book

## Chapter 1: Special/Characters?

Some content here.

## Chapter 2: More*Content!

More content here."""

    results = processor.prepare_content(content, "Test Book", temp_dir)

    assert len(results) == 2
    assert "Special-Characters" in results[0]["file_path"]
    assert "More-Content" in results[1]["file_path"]
    assert all(r["file_path"].startswith(str(temp_dir)) for r in results)


def test_tts_processor_content_cleaning(temp_dir):
    """Test that content is properly cleaned in output files."""
    processor = TTSProcessor()
    content = """# Test Book

## Chapter 1

**Bold** and *italic* with [link](http://example.com)
and ```{=html}<div>HTML</div>```"""

    results = processor.prepare_content(content, "Test Book", temp_dir)

    with open(results[0]["file_path"], "r") as f:
        processed_content = f.read()

    assert "Bold and italic with link" in processed_content
    assert "<div>" not in processed_content
    assert "**" not in processed_content
    assert "*" not in processed_content


def test_tts_processor_empty_content(temp_dir):
    """Test handling of empty or minimal content."""
    processor = TTSProcessor()
    content = "# Test Book\n\nJust a title"

    results = processor.prepare_content(content, "Test Book", temp_dir)

    assert len(results) == 1
    assert results[0]["title"] == "Test Book"
    assert "Just a title" in Path(results[0]["file_path"]).read_text()
