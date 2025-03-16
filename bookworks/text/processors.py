"""
Text processing utilities for bookworks.
"""

import re
from typing import Dict, Tuple, List

from ..core import ContentProcessor, ContentMetadata


class MarkdownCleaner(ContentProcessor):
    """Clean and process markdown content for various purposes."""

    def process(self, content: str) -> str:
        """
        Clean and process markdown content, fixing common issues.

        Args:
            content: Raw markdown content

        Returns:
            Processed content
        """
        content = self._normalize_line_endings(content)
        content = self._fix_multiline_links(content)
        content = self._fix_paragraph_spacing(content)
        return content

    def process_with_metadata(self, content: str) -> Tuple[str, ContentMetadata]:
        """
        Clean content and extract metadata.

        Args:
            content: Raw markdown content

        Returns:
            Tuple of (processed_content, metadata)
        """
        metadata = self._extract_metadata(content)
        processed = self.process(content)
        return processed, metadata

    def _normalize_line_endings(self, content: str) -> str:
        """Normalize line endings to \n."""
        return content.replace("\r\n", "\n")

    def _fix_multiline_links(self, content: str) -> str:
        """Fix multi-line links by cleaning up newlines in link text."""

        def clean_link(match: re.Match[str]) -> str:
            text = match.group(1)
            url = match.group(2)
            cleaned_text = " ".join(text.split())
            return f"[{cleaned_text}]({url})"

        return re.sub(r"\[([\s\S]*?)\]\((.*?)\)", clean_link, content)

    def _fix_paragraph_spacing(self, content: str) -> str:
        """Add proper spacing between paragraphs."""
        lines = content.split("\n")
        result = []

        for i, line in enumerate(lines):
            line = line.rstrip()
            if not line:
                result.append("")
                continue

            is_special = line.strip().startswith(("#", "*", "-", "+"))
            next_is_empty = (i + 1 >= len(lines)) or not lines[i + 1].strip()

            if is_special or next_is_empty:
                result.append(line)
            else:
                result.append(line + "\n")

        return "\n".join(result)

    def _extract_metadata(self, content: str) -> ContentMetadata:
        """Extract metadata from content."""
        metadata = ContentMetadata()
        title_match = re.search(r"^# (.*?)$", content, re.MULTILINE)
        metadata["title"] = title_match.group(1) if title_match else "Untitled Document"
        return metadata


class TTSPreprocessor(ContentProcessor):
    """Prepare markdown content for text-to-speech processing."""

    def process(self, content: str) -> str:
        """
        Clean markdown content to make it suitable for TTS reading.

        Args:
            content: Raw markdown content

        Returns:
            Cleaned content suitable for TTS
        """
        # Remove markdown ID references and HTML blocks
        content = re.sub(r"\[\]\{#[^}]+\}", "", content)
        content = re.sub(r"```\{=html\}[\s\S]*?```", "", content)

        # Remove section formatting and attributes
        content = re.sub(r"::: \{[^}]+\}", "", content)
        content = re.sub(r":::.*", "", content)
        content = re.sub(r"(#+ .*?) \{[^}]+\}", r"\1", content)

        # Remove images and special formatting
        content = re.sub(r"!\[\]\([^)]+\)", "", content)
        content = re.sub(r"\{\.x-ebookmaker-cover\}", "", content)
        content = re.sub(r"\{\#[^}]+\}", "", content)
        content = re.sub(r"\[.*?\]\{[^}]+\}", "", content)
        content = re.sub(r"lang=\"[^\"]+\"", "", content)

        # Convert links and remove HTML
        content = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", content)
        content = re.sub(r"<[^>]+>", "", content)
        content = re.sub(r"\{[^}]+\}", "", content)

        # Convert formatting to plain text
        content = re.sub(r"\*\*([^*]+)\*\*", r"\1", content)
        content = re.sub(r"\*([^*]+)\*", r"\1", content)
        content = re.sub(r"__([^_]+)__", r"\1", content)
        content = re.sub(r"_([^_]+)_", r"\1", content)

        # Clean up various markers and formatting
        content = re.sub(r"\[\^[^\]]+\]", "", content)
        content = re.sub(r"^\d+\.\s+", "", content, flags=re.MULTILINE)
        content = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", r"\1", content)
        content = re.sub(r"\\{2,}", "", content)

        # Remove Project Gutenberg boilerplate
        content = re.sub(
            r"START OF THE PROJECT GUTENBERG EBOOK.*", "", content, flags=re.IGNORECASE
        )
        content = re.sub(
            r"END OF THE PROJECT GUTENBERG EBOOK.*", "", content, flags=re.IGNORECASE
        )

        # Clean up whitespace
        content = re.sub(r"\\$", "", content, flags=re.MULTILINE)
        content = re.sub(r"  +", " ", content)
        content = re.sub(r"\n{3,}", "\n\n", content)

        return content.strip()


class ChapterSplitter:
    """Split content into chapters based on headers."""

    def split_chapters(self, content: str, book_title: str) -> List[Dict[str, str]]:
        """
        Split content into chapters using header patterns.

        Args:
            content: Markdown content to split
            book_title: Title of the book

        Returns:
            List of dictionaries containing chapter info
        """
        chapters: List[Dict[str, str]] = []
        lines = content.split("\n")
        current_chapter: List[str] = []
        current_title = ""

        for line in lines:
            if line.startswith("#"):  # Header found
                if current_chapter:  # Save previous chapter
                    chapters.append(
                        {
                            "title": current_title or "Untitled Chapter",
                            "content": "\n".join(current_chapter).strip(),
                        }
                    )
                    current_chapter = []
                current_title = line.lstrip("#").strip()
            current_chapter.append(line)

        # Add the last chapter
        if current_chapter:
            chapters.append(
                {
                    "title": current_title or "Untitled Chapter",
                    "content": "\n".join(current_chapter).strip(),
                }
            )

        # If no chapters were found, treat the entire content as one chapter
        if not chapters:
            chapters.append({"title": book_title, "content": content.strip()})

        return chapters
