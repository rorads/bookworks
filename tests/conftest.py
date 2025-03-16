"""
Test configuration and shared fixtures for bookworks.
"""

import tempfile
from pathlib import Path
from typing import Generator, Any
import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, Any, None]:
    """Provide a temporary directory that's cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_markdown() -> str:
    """Provide sample markdown content for testing."""
    return """# Sample Book

## Chapter 1: Introduction

This is a test chapter with some **bold** and *italic* text.
It also has a [link](http://example.com) and some `code`.

## Chapter 2: More Content

Another chapter with different formatting:
- List item 1
- List item 2

```{=html}
<div>Some HTML content</div>
```

[]{#some_id}
"""


@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"
