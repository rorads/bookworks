"""
Core functionality for bookworks.

This module contains base types, interfaces, and core functionality used throughout the package.
"""

from typing import Protocol, Dict, Any, Optional, TypeVar

T = TypeVar("T")


class ContentProcessor(Protocol):
    """Base protocol for content processors."""

    def process(self, content: str) -> str:
        """Process the content according to the processor's rules."""
        ...


class ContentMetadata(Dict[str, Any]):
    """Type for content metadata."""

    pass


# Common type aliases
FilePath = str
ProcessingResult = tuple[str, Optional[str]]  # (content, error)
