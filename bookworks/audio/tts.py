"""
Text-to-speech processing utilities for bookworks.
"""

import os
import re
from typing import List, Dict

from ..core import ProcessingResult
from ..text.processors import TTSPreprocessor, ChapterSplitter
from ..utils.filesystem import sanitize_filename


class TTSProcessor:
    """Process text content into audio using text-to-speech."""

    def __init__(self, output_dir: str):
        """
        Initialize TTSProcessor.

        Args:
            output_dir: Directory to save audio files
        """
        self.output_dir = output_dir
        self.preprocessor = TTSPreprocessor()
        self.chapter_splitter = ChapterSplitter()

    def process(self, content: str, book_title: str) -> ProcessingResult:
        """
        Process content into audio files.

        Args:
            content: Raw markdown content
            book_title: Title of the book

        Returns:
            ProcessingResult with status and output files
        """
        # Placeholder for actual TTS processing
        return "", None

    def prepare_content(self, content: str, book_title: str) -> List[Dict[str, str]]:
        """
        Clean content and split into chapters for TTS processing.

        Args:
            content: Raw markdown content
            book_title: Title of the book

        Returns:
            List of dictionaries containing chapter info and file paths
        """
        # Clean the content
        cleaned_content = self.preprocessor.process(content)

        # Split into chapters
        chapters = self.chapter_splitter.split_chapters(cleaned_content, book_title)

        # Skip first chapter if it's empty or just contains the book title
        if chapters and (
            not chapters[0]["content"].strip()
            or chapters[0]["content"].strip() == f"# {book_title}"
        ):
            chapters = chapters[1:]

        # Save chapters to files
        os.makedirs(self.output_dir, exist_ok=True)
        for i, chapter in enumerate(chapters, 1):
            # Extract chapter title, handling colons in titles
            chapter_title = chapter["title"]
            if ":" in chapter_title:
                chapter_title = chapter_title.split(":", 1)[1].strip()

            # Generate filename with special characters preserved but safe
            filename = sanitize_filename(chapter_title)
            if not filename:  # Fallback if title produces empty filename
                filename = f"chapter_{i}"

            # Add hyphens between words for better readability
            filename = re.sub(r"([a-z])([A-Z])", r"\1-\2", filename)
            filename = filename.replace(" ", "-")
            filename = filename.replace("_", "-")  # Convert underscores to hyphens

            # Save file path
            chapter["file_path"] = os.path.join(self.output_dir, f"{filename}.txt")

            # Save content to file
            with open(chapter["file_path"], "w") as f:
                f.write(chapter["content"])

        return chapters

    def process_chapters(self, chapters: List[Dict[str, str]]) -> ProcessingResult:
        """
        Process multiple chapters into audio files.

        Args:
            chapters: List of chapter info dictionaries

        Returns:
            ProcessingResult with status and output files
        """
        # Placeholder for actual TTS processing
        return "", None
