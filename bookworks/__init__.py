"""
Bookworks: A library for processing and converting books for various formats.
"""

from .text.processors import MarkdownCleaner, TTSPreprocessor, ChapterSplitter
from .audio.tts import TTSProcessor
from .utils.filesystem import sanitize_filename, create_temp_workspace
from .utils.commands import run_pandoc_command

__version__ = "0.1.0"

__all__ = [
    "MarkdownCleaner",
    "TTSPreprocessor",
    "ChapterSplitter",
    "TTSProcessor",
    "sanitize_filename",
    "create_temp_workspace",
    "run_pandoc_command",
]
