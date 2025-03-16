"""
Tests for text processing functionality.
"""

from bookworks.text.processors import MarkdownCleaner, TTSPreprocessor, ChapterSplitter


def test_markdown_cleaner_initialization():
    """Test that MarkdownCleaner can be initialized."""
    cleaner = MarkdownCleaner()
    assert cleaner is not None


def test_markdown_cleaner_empty_content():
    """Test cleaning empty content."""
    cleaner = MarkdownCleaner()
    result = cleaner.process("")
    assert result == ""


def test_tts_preprocessor_initialization():
    """Test that TTSPreprocessor can be initialized."""
    preprocessor = TTSPreprocessor()
    assert preprocessor is not None


def test_tts_preprocessor_empty_content():
    """Test preprocessing empty content."""
    preprocessor = TTSPreprocessor()
    result = preprocessor.process("")
    assert result == ""


def test_chapter_splitter_initialization():
    """Test that ChapterSplitter can be initialized."""
    splitter = ChapterSplitter()
    assert splitter is not None


def test_chapter_splitter_empty_content():
    """Test splitting empty content."""
    splitter = ChapterSplitter()
    result = splitter.split_chapters("", "Test Book")
    assert len(result) == 1
    assert result[0]["title"] == "Test Book"
    assert result[0]["content"] == ""


def test_markdown_cleaner_basic():
    """Test basic markdown cleaning functionality."""
    cleaner = MarkdownCleaner()
    content = "Line 1\r\nLine 2\r\n\r\nLine 3"
    result = cleaner.process(content)
    assert "\r\n" not in result
    assert "Line 1\nLine 2\n\nLine 3" == result


def test_markdown_cleaner_with_metadata():
    """Test markdown cleaning with metadata extraction."""
    cleaner = MarkdownCleaner()
    content = "# My Title\n\nSome content"
    result, metadata = cleaner.process_with_metadata(content)
    assert metadata["title"] == "My Title"
    assert "Some content" in result


def test_markdown_cleaner_multiline_links():
    """Test cleaning of multiline links."""
    cleaner = MarkdownCleaner()
    content = "[Multi\nline\nlink](http://example.com)"
    result = cleaner.process(content)
    assert "[Multi line link](http://example.com)" == result


def test_tts_preprocessor_formatting():
    """Test TTS preprocessing of markdown formatting."""
    processor = TTSPreprocessor()
    content = (
        "**Bold** and *italic* text with `code` and "
        "[link](http://example.com) and []{#id}"
    )
    result = processor.process(content)
    assert "Bold and italic text with code and link and " == result


def test_tts_preprocessor_html():
    """Test TTS preprocessing of HTML content."""
    processor = TTSPreprocessor()
    content = "Normal text\n```{=html}\n<div>HTML content</div>\n```\nMore text"
    result = processor.process(content)
    assert "Normal text\nMore text" == result.strip()


def test_chapter_splitter(sample_markdown):
    """Test splitting content into chapters."""
    splitter = ChapterSplitter()
    chapters = splitter.split_chapters(sample_markdown, "Sample Book")

    assert len(chapters) == 2
    assert chapters[0]["title"] == "Chapter 1: Introduction"
    assert "bold" in chapters[0]["content"].lower()
    assert chapters[1]["title"] == "Chapter 2: More Content"
    assert "list item" in chapters[1]["content"].lower()


def test_chapter_splitter_no_chapters():
    """Test chapter splitting with content that has no chapter markers."""
    splitter = ChapterSplitter()
    content = "Just some content\nwithout any chapters"
    chapters = splitter.split_chapters(content, "Test Book")

    assert len(chapters) == 1
    assert chapters[0]["title"] == "Test Book"
    assert chapters[0]["content"] == content
