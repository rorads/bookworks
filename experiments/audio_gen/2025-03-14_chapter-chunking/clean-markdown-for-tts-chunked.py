"""
This script cleans markdown files for better TTS reading and splits chapters into smaller chunks.

It removes various markdown and HTML markup that would interfere with TTS reading,
while preserving the actual content and chapter structure.
"""

import re
from pathlib import Path

# Define the input and output directories
input_dir = Path("output/markdown")
output_dir = Path("output/clean-markdown-for-tts")
chapters_dir = Path("output/tts-ready-chapters")
chunked_chapters_dir = Path("output/tts-ready-chapters-chunks")

# For testing purposes - explicitly set the file to process
test_file = Path("../../../output/markdown/sample_book.md")

# Configure chunking parameters
MAX_CHUNK_SIZE = 2000  # Maximum characters per chunk - reduced for testing
MIN_CHUNK_SIZE = (
    500  # Minimum characters for a chunk to be considered valid - reduced for testing
)

# Create the output directories if they don't exist
output_dir.mkdir(parents=True, exist_ok=True)
chapters_dir.mkdir(parents=True, exist_ok=True)
chunked_chapters_dir.mkdir(parents=True, exist_ok=True)


def clean_markdown_for_tts(content):
    """
    Clean markdown content to make it suitable for TTS reading.

    Args:
        content (str): The markdown content to clean

    Returns:
        str: The cleaned content
    """
    # Remove markdown ID references like []{#title_page.xhtml}
    content = re.sub(r"\[\]\{#[^}]+\}", "", content)

    # Remove HTML blocks
    content = re.sub(r"```\{=html\}[\s\S]*?```", "", content)

    # Remove section formatting
    content = re.sub(r"::: \{[^}]+\}", "", content)
    content = re.sub(r":::.*", "", content)

    # Clean up headings - keep the heading text but remove attributes
    content = re.sub(r"(#+ .*?) \{[^}]+\}", r"\1", content)

    # Remove image references
    content = re.sub(r"!\[\]\([^)]+\)", "", content)
    content = re.sub(r"\{\.x-ebookmaker-cover\}", "", content)

    # Remove HTML IDs in brackets
    content = re.sub(r"\{\#[^}]+\}", "", content)

    # Remove attributes in square brackets
    content = re.sub(r"\[.*?\]\{[^}]+\}", "", content)

    # Clean up inline ID references
    content = re.sub(r"\{\#[^\}]+\}", "", content)

    # Remove language attributes
    content = re.sub(r'lang="[^"]+"', "", content)

    # Convert links to just their display text (removing URLs)
    content = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", content)

    # Remove HTML tags
    content = re.sub(r"<[^>]+>", "", content)

    # Remove any remaining attributes within curly braces
    content = re.sub(r"\{[^}]+\}", "", content)

    # Convert formatting to plain text (bold, italic, etc.)
    content = re.sub(r"\*\*([^*]+)\*\*", r"\1", content)  # Bold
    content = re.sub(r"\*([^*]+)\*", r"\1", content)  # Italic
    content = re.sub(r"__([^_]+)__", r"\1", content)  # Bold (alt)
    content = re.sub(r"_([^_]+)_", r"\1", content)  # Italic (alt)

    # Remove reference-style links
    content = re.sub(r"\[\^[^\]]+\]", "", content)

    # Clean up navigation numbers/bullets at the beginning of lines
    content = re.sub(r"^\d+\.\s+", "", content, flags=re.MULTILINE)

    # Remove backslashes that are used for escaping
    content = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", r"\1", content)

    # Clean up any remaining square brackets with content
    content = re.sub(r"\[([^\]]+)\](\{[^}]+\})?", r"\1", content)

    # Remove multiple backslashes (like \\)
    content = re.sub(r"\\{2,}", "", content)

    # Remove eBook markers
    content = re.sub(
        r"START OF THE PROJECT GUTENBERG EBOOK.*", "", content, flags=re.IGNORECASE
    )
    content = re.sub(
        r"END OF THE PROJECT GUTENBERG EBOOK.*", "", content, flags=re.IGNORECASE
    )

    # Fix multiple backslashes issue
    content = content.replace("\\", "")

    # Fix line endings issues from pandoc conversion
    content = re.sub(r"\\$", "", content, flags=re.MULTILINE)

    # Fix double spaces
    content = re.sub(r"  +", " ", content)

    # Remove excessive blank lines (more than 2 in a row)
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Remove Project Gutenberg boilerplate at beginning
    content = re.sub(r"^.*?(?=\n\n\w+)", "", content, flags=re.DOTALL)

    return content.strip()


def split_by_chapters(content, book_title):
    """
    Split the markdown content into chapters based on header patterns.

    Args:
        content (str): The markdown content to split
        book_title (str): The title of the book

    Returns:
        list: A list of dictionaries with chapter titles and content
    """
    # Pattern to identify chapter headers (# or ## followed by text)
    chapter_pattern = re.compile(r"^#{1,2}\s+(.*?)$", re.MULTILINE)

    # Find all chapter headers
    chapter_matches = list(chapter_pattern.finditer(content))

    # If no chapters found, return the whole content as one chapter
    if not chapter_matches:
        return [{"title": book_title, "content": content}]

    chapters = []

    # Process each chapter
    for i, match in enumerate(chapter_matches):
        chapter_start = match.start()
        chapter_title = match.group(1).strip()

        # Determine where this chapter ends (at the next chapter or end of content)
        if i < len(chapter_matches) - 1:
            chapter_end = chapter_matches[i + 1].start()
        else:
            chapter_end = len(content)

        # Extract chapter content
        chapter_content = content[chapter_start:chapter_end].strip()

        chapters.append({"title": chapter_title, "content": chapter_content})

    return chapters


def chunk_chapter_content(
    chapter_content, max_size=MAX_CHUNK_SIZE, min_size=MIN_CHUNK_SIZE
):
    """
    Split chapter content into smaller chunks based on paragraph and sentence boundaries.

    Args:
        chapter_content (str): The chapter content to split
        max_size (int): Maximum size of each chunk in characters
        min_size (int): Minimum size for a chunk to be valid

    Returns:
        list: A list of content chunks
    """
    # If the content is already smaller than max_size, return it as a single chunk
    if len(chapter_content) <= max_size:
        return [chapter_content]

    # Split content into paragraphs (double newlines)
    paragraphs = re.split(r"\n\n+", chapter_content)

    chunks = []
    current_chunk = ""

    # Process each paragraph
    for paragraph in paragraphs:
        # If adding this paragraph would exceed max_size and we already have content
        if (
            len(current_chunk) + len(paragraph) + 2 > max_size
            and len(current_chunk) >= min_size
        ):
            # Add current chunk to chunks list
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            # Add paragraph to current chunk
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph

    # Add the final chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.strip())

    # If any chunk is still too large, split it further at sentence boundaries
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > max_size:
            # Try to split at sentence boundaries
            sentences = re.split(r"(?<=[.!?])\s+", chunk)

            temp_chunk = ""
            for sentence in sentences:
                if (
                    len(temp_chunk) + len(sentence) + 1 > max_size
                    and len(temp_chunk) >= min_size
                ):
                    final_chunks.append(temp_chunk.strip())
                    temp_chunk = sentence
                else:
                    if temp_chunk:
                        temp_chunk += " " + sentence
                    else:
                        temp_chunk = sentence

            if temp_chunk:
                final_chunks.append(temp_chunk.strip())
        else:
            final_chunks.append(chunk)

    return final_chunks


# Process the test file directly
try:
    print(f"Processing test file: {test_file}")

    # Read the markdown content
    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean the markdown
    cleaned_content = clean_markdown_for_tts(content)

    # Create the output file path for the full cleaned content
    output_file = output_dir / test_file.name

    # Write the cleaned content
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

    print(f"Cleaned {test_file.name} and saved to {output_file}")

    # Split the content into chapters
    book_title = test_file.stem
    chapters = split_by_chapters(cleaned_content, book_title)

    # Create directories for this book's chapters
    book_chapter_dir = chapters_dir / book_title
    book_chapter_dir.mkdir(exist_ok=True)

    book_chunked_chapter_dir = chunked_chapters_dir / book_title
    book_chunked_chapter_dir.mkdir(exist_ok=True)

    # Stats for reporting
    total_chunks = 0

    # Save each chapter to a separate file and create chunks for long chapters
    for i, chapter in enumerate(chapters, 1):
        # Create a clean filename from the chapter title
        chapter_title = re.sub(r"[^\w\s-]", "", chapter["title"])
        chapter_title = re.sub(r"\s+", "_", chapter_title)
        chapter_filename = f"{i:02d}_{chapter_title[:50]}.md"

        # Create the chapter file path and save regular chapter
        chapter_file = book_chapter_dir / chapter_filename
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(chapter["content"])

        print(f"  - Chapter {i}: {chapter['title']} saved to {chapter_file}")
        print(f"    - Chapter length: {len(chapter['content'])} characters")

        # Split chapter into chunks
        chunks = chunk_chapter_content(chapter["content"])

        # Save each chunk to a separate file
        for j, chunk_content in enumerate(chunks, 1):
            chunk_filename = f"{i:02d}_{j:02d}_{chapter_title[:40]}.md"
            chunk_file = book_chunked_chapter_dir / chunk_filename

            with open(chunk_file, "w", encoding="utf-8") as f:
                f.write(chunk_content)

            print(
                f"    - Chunk {j}/{len(chunks)} saved to {chunk_file} ({len(chunk_content)} chars)"
            )

        total_chunks += len(chunks)
        print(f"    - Split into {len(chunks)} chunks")

    print(
        f"Split {len(chapters)} chapters from {test_file.name} into {total_chunks} total chunks"
    )

except Exception as e:
    print(f"Error processing {test_file.name}: {e}")

print(f"Cleaned markdown files saved to {output_dir}")
print(f"TTS-ready chapter files saved to {chapters_dir}")
print(f"TTS-ready chunked chapter files saved to {chunked_chapters_dir}")

# Print a small sample of one chunked file for inspection
sample_files = list(chunked_chapters_dir.glob(f"{book_title}/*.md"))
if sample_files:
    sample_file = sample_files[0]
    print(f"\nSample of chunked content from {sample_file.name}:")

    try:
        with open(sample_file, "r", encoding="utf-8") as f:
            sample_content = f.read(500)  # Read first 500 characters

        print("-" * 50)
        print(sample_content + "...")
        print("-" * 50)

        # Print chunking statistics
        total_files = len(list(chunked_chapters_dir.glob(f"{book_title}/*.md")))
        print(f"Total chunked files created: {total_files}")

    except Exception as e:
        print(f"Error reading sample: {e}")
