"""
This script cleans markdown files for better TTS reading.

It removes various markdown and HTML markup that would interfere with TTS reading,
while preserving the actual content and chapter structure.

It can also split long chapters into smaller chunks for better TTS processing.
"""

import re
import argparse
from pathlib import Path

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Clean markdown files for TTS reading and split into chapters."
)
parser.add_argument(
    "--max-chunk-size",
    type=int,
    default=0,
    help="Maximum size of each chunk in characters. Set to 0 to disable chunking (default), or try values like 5000-10000.",
)
parser.add_argument(
    "--min-chunk-size",
    type=int,
    default=1000,
    help="Minimum size for a chunk to be considered valid.",
)
args = parser.parse_args()

# Define the input and output directories
input_dir = Path("output/markdown")
output_dir = Path("output/clean-markdown-for-tts")
chapters_dir = Path("output/tts-ready-chapters")
chunked_chapters_dir = Path("output/tts-ready-chapters-chunks")

# Create the output directories if they don't exist
output_dir.mkdir(parents=True, exist_ok=True)
chapters_dir.mkdir(parents=True, exist_ok=True)

# Only create chunked chapters directory if chunking is enabled
if args.max_chunk_size > 0:
    chunked_chapters_dir.mkdir(parents=True, exist_ok=True)
    print(f"Chunking enabled with max chunk size: {args.max_chunk_size} characters")
else:
    print(
        "Chunking disabled. Use --max-chunk-size to enable (recommended values: 5000-10000)"
    )


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
    chapter_content, max_size=args.max_chunk_size, min_size=args.min_chunk_size
):
    """
    Split chapter content into smaller chunks based on paragraph and sentence boundaries.

    Args:
        chapter_content (str): The chapter content to split
        max_size (int): Maximum size of each chunk in characters
        min_size (int): Minimum size for a chunk to be considered valid

    Returns:
        list: A list of content chunks
    """
    # If chunking is disabled or content is already smaller than max_size, return it as a single chunk
    if max_size <= 0 or len(chapter_content) <= max_size:
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


# Process each markdown file
print(f"Looking for markdown files in {input_dir}")
md_files = list(input_dir.glob("*.md"))
print(f"Found {len(md_files)} markdown files")

# Initialize counters for summary
total_books = 0
total_chapters = 0
total_chunks = 0

for md_file in md_files:
    try:
        print(f"\nProcessing {md_file}...")
        total_books += 1

        # Read the markdown content
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Clean the markdown
        cleaned_content = clean_markdown_for_tts(content)

        # Create the output file path for the full cleaned content
        output_file = output_dir / md_file.name

        # Write the cleaned content
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_content)

        print(f"Cleaned {md_file.name} and saved to {output_file}")

        # Split the content into chapters
        book_title = md_file.stem
        chapters = split_by_chapters(cleaned_content, book_title)
        chapter_count = len(chapters)
        total_chapters += chapter_count
        print(f"Split {md_file.name} into {chapter_count} chapters")

        # Create a directory for this book's chapters
        book_chapter_dir = chapters_dir / book_title
        book_chapter_dir.mkdir(exist_ok=True)

        # Initialize book chunks counter
        book_chunks = 0

        # Save each chapter to a separate file
        for i, chapter in enumerate(chapters, 1):
            # Create a clean filename from the chapter title
            chapter_title = re.sub(r"[^\w\s-]", "", chapter["title"])
            chapter_title = re.sub(r"\s+", "_", chapter_title)
            chapter_filename = f"{i:02d}_{chapter_title[:50]}.md"

            # Create the chapter file path
            chapter_file = book_chapter_dir / chapter_filename

            # Write the chapter content
            with open(chapter_file, "w", encoding="utf-8") as f:
                f.write(chapter["content"])

            chapter_length = len(chapter["content"])
            print(f"  - Chapter {i}: {chapter['title']} ({chapter_length} chars)")

            # Skip chunking if disabled
            if args.max_chunk_size <= 0:
                continue

            # Process chunking if enabled
            # Split chapter into chunks
            chunks = chunk_chapter_content(chapter["content"])

            # Skip if only one chunk (same as original)
            if len(chunks) <= 1:
                continue

            # Create directory for chunked chapters if it doesn't exist
            book_chunked_chapter_dir = chunked_chapters_dir / book_title
            book_chunked_chapter_dir.mkdir(exist_ok=True)

            # Save each chunk to a separate file
            print(f"    - Splitting chapter {i} into {len(chunks)} chunks")
            for j, chunk_content in enumerate(chunks, 1):
                chunk_filename = f"{i:02d}_{j:02d}_{chapter_title[:40]}.md"
                chunk_file = book_chunked_chapter_dir / chunk_filename

                with open(chunk_file, "w", encoding="utf-8") as f:
                    f.write(chunk_content)

                print(f"      - Chunk {j}: {len(chunk_content)} chars")

            book_chunks += len(chunks)

        total_chunks += book_chunks

        # Print chunking info if enabled
        if args.max_chunk_size > 0 and book_chunks > 0:
            print(
                f"Created {book_chunks} chunks from {chapter_count} chapters for {book_title}"
            )

    except Exception as e:
        print(f"Error processing {md_file.name}: {e}")

# Print summary
print("\n" + "=" * 50)
print("SUMMARY:")
print(f"  - Processed {total_books} books")
print(f"  - Created {total_chapters} chapter files")
if args.max_chunk_size > 0 and total_chunks > 0:
    print(f"  - Created {total_chunks} chunk files")
print("=" * 50)

print(f"\nCleaned markdown files saved to {output_dir}")
print(f"TTS-ready chapter files saved to {chapters_dir}")

# Print chunked chapters info if enabled
if args.max_chunk_size > 0:
    print(f"TTS-ready chunked chapter files saved to {chunked_chapters_dir}")

# Print a small sample of one file for inspection
sample_files = list(output_dir.glob("*.md"))
if sample_files:
    sample_file = sample_files[0]
    print(f"\nSample of cleaned content from {sample_file.name}:")

    try:
        with open(sample_file, "r", encoding="utf-8") as f:
            sample_content = f.read(500)  # Read first 500 characters

        print("-" * 50)
        print(sample_content + "...")
        print("-" * 50)
    except Exception as e:
        print(f"Error reading sample: {e}")
