"""
Convert Markdown (or EPUB) files to TTS-ready markdown.

This script cleans the markdown to remove extraneous formatting and creates a version
that is optimized for TTS reading.
"""

import sys
import os
import argparse
from bookworks.bw_utils import (
    clean_markdown_for_tts,
    split_by_chapters,
    epub_to_markdown,
)  # Added import for epub_to_markdown
from typing import Optional

# Define output directory
OUTPUT_DIR = os.path.abspath("output/tts-ready-markdown")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def process_file(
    input_file: str,
    book_title: Optional[str] = None,
    split_chapters: bool = False,
    max_chars: int = 3000,
):
    # Check if file is EPUB and convert to markdown if needed
    file_ext = os.path.splitext(input_file)[1].lower()
    if file_ext == ".epub":
        # Use the epub_to_markdown function from bw_utils
        try:
            content = epub_to_markdown(input_file)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to convert EPUB to markdown: {str(e)}")
    else:
        # Read the input file (assuming it's markdown)
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

    # Clean the markdown for TTS reading
    cleaned = clean_markdown_for_tts(content)

    # Get book title from filename if not provided
    if not book_title:
        book_title = os.path.splitext(os.path.basename(input_file))[0]
    safe_title = book_title.replace(" ", "_")

    # If splitting by chapters is enabled
    if split_chapters:
        chapters = split_by_chapters(cleaned, book_title)
        output_files = []

        for i, chapter in enumerate(chapters):
            chapter_title = chapter["title"]
            chapter_content = chapter["content"]

            # Split chapter content into chunks of max_chars
            if max_chars > 0:
                chunks = []
                current_chunk = ""
                for paragraph in chapter_content.split("\n\n"):
                    # If adding this paragraph would exceed max_chars, start a new chunk
                    if len(current_chunk) + len(paragraph) > max_chars:
                        if current_chunk:  # Only add non-empty chunks
                            chunks.append(current_chunk)
                        current_chunk = paragraph
                    else:
                        if current_chunk:
                            current_chunk += "\n\n" + paragraph
                        else:
                            current_chunk = paragraph

                # Add the last chunk if it exists
                if current_chunk:
                    chunks.append(current_chunk)

                # Write each chunk to a separate file
                for j, chunk in enumerate(chunks):
                    chunk_filename = f"{safe_title}_ch{i + 1}_part{j + 1}_tts.md"
                    chunk_path = os.path.join(OUTPUT_DIR, chunk_filename)
                    with open(chunk_path, "w", encoding="utf-8") as f:
                        f.write(f"# {chapter_title} (Part {j + 1})\n\n{chunk}")
                    output_files.append(chunk_path)
            else:
                # Write the whole chapter to a single file
                chapter_filename = f"{safe_title}_ch{i + 1}_tts.md"
                chapter_path = os.path.join(OUTPUT_DIR, chapter_filename)
                with open(chapter_path, "w", encoding="utf-8") as f:
                    f.write(chapter_content)
                output_files.append(chapter_path)

        return output_files
    else:
        # Output a single cleaned file
        output_path = os.path.join(OUTPUT_DIR, f"{safe_title}_tts.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        return [output_path]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean a Markdown (or EPUB) file for TTS reading."
    )
    parser.add_argument("input_file", help="Input Markdown (or EPUB) file")
    parser.add_argument(
        "--book-title", help="Optional book title (default taken from filename)"
    )
    parser.add_argument(
        "--split-chapters", action="store_true", help="Split output by chapters"
    )
    parser.add_argument(
        "--max-chars", type=int, default=3000, help="Maximum characters per output file"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    output_paths = process_file(
        args.input_file, args.book_title, args.split_chapters, args.max_chars
    )
    if len(output_paths) == 1:
        print(f"Successfully created TTS-ready markdown: {output_paths[0]}")
    else:
        print(
            f"Successfully created {len(output_paths)} TTS-ready markdown files in {OUTPUT_DIR}"
        )
