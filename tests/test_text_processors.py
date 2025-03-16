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
    processor = TTSPreprocessor()
    assert processor is not None


def test_tts_preprocessor_empty_content():
    """Test preprocessing empty content."""
    processor = TTSPreprocessor()
    result = processor.process("")
    assert result == ""


def test_chapter_splitter_initialization():
    """Test that ChapterSplitter can be initialized."""
    splitter = ChapterSplitter()
    assert splitter is not None


def test_chapter_splitter_empty_content():
    """Test splitting empty content."""
    splitter = ChapterSplitter()
    result = splitter.split_chapters("", "Empty Book")
    assert len(result) == 1
    assert result[0]["title"] == "Empty Book"
    assert result[0]["content"] == ""


def test_markdown_cleaner_basic():
    """Test basic markdown cleaning."""
    cleaner = MarkdownCleaner()
    content = "Line 1\r\nLine 2\n\nLine 3"
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
    """Test cleaning of multi-line links."""
    cleaner = MarkdownCleaner()
    content = "[Multi\nLine\nLink](http://example.com)"
    result = cleaner.process(content)
    assert "[Multi Line Link](http://example.com)" == result


def test_tts_preprocessor_formatting():
    """Test TTS preprocessing of markdown formatting."""
    processor = TTSPreprocessor()
    content = (
        "**Bold** and *italic* text with `code` and "
        "[link](http://example.com) and []{#id}"
    )
    result = processor.process(content)
    assert result == "Bold and italic text with code and link and"


def test_tts_preprocessor_html():
    """Test TTS preprocessing of HTML content."""
    processor = TTSPreprocessor()
    content = """```{=html}
<div>Some HTML content</div>
```
Regular text"""
    result = processor.process(content)
    assert "Some HTML content" not in result
    assert "Regular text" in result


def test_chapter_splitter():
    """Test chapter splitting functionality."""
    splitter = ChapterSplitter()
    content = """# Book Title

## Chapter 1

Content 1

## Chapter 2

Content 2"""
    result = splitter.split_chapters(content, "Book Title")
    assert len(result) == 2
    assert result[0]["title"] == "Chapter 1"
    assert "Content 1" in result[0]["content"]
    assert result[1]["title"] == "Chapter 2"
    assert "Content 2" in result[1]["content"]


def test_chapter_splitter_no_chapters():
    """Test chapter splitting with no chapter markers."""
    splitter = ChapterSplitter()
    content = "Just some content\nwithout chapters"
    result = splitter.split_chapters(content, "Book Title")
    assert len(result) == 1
    assert result[0]["title"] == "Book Title"
    assert "Just some content" in result[0]["content"]
