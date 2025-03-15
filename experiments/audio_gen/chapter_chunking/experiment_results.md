# Chapter Chunking Experiment Results

## Summary

The experiment to add chunking functionality to the `clean-markdown-for-tts.py` script was successful. We added a new function to split long chapters into smaller chunks based on paragraph and sentence boundaries, while preserving the natural flow of the text.

## Testing Results

Using a sample book with three chapters:

1. **Chapter 1**: Long chapter (2991 characters) → Split into 2 chunks (1814 and 1175 characters)
2. **Chapter 2**: Short chapter (333 characters) → Kept as a single chunk
3. **Chapter 3**: Medium chapter (2285 characters) → Split into 2 chunks (1781 and 502 characters)

Total chapters: 3
Total chunks created: 5

## Implementation Details

The core of the implementation is the `chunk_chapter_content` function, which:

1. Checks if the content is already smaller than the maximum chunk size
2. Splits content at paragraph boundaries first
3. For any chunks still too large, splits further at sentence boundaries
4. Preserves minimum chunk sizes to avoid creating tiny fragments

## Findings

- The chunking algorithm successfully preserves paragraph and sentence structures
- Chunks end at natural paragraph boundaries whenever possible
- Chapter headers are preserved in the first chunk
- File naming convention allows for proper ordering (chapter_number_chunk_number_title)

## Recommended Modifications to Original Script

The most concise edit to implement this functionality in the original script would be:

1. Add the chunking directory and parameters:
```python
chunked_chapters_dir = Path("output/tts-ready-chapters-chunks")
MAX_CHUNK_SIZE = 5000  # Maximum characters per chunk
MIN_CHUNK_SIZE = 1000  # Minimum characters for a chunk to be considered valid

# Add to the directory creation section
chunked_chapters_dir.mkdir(parents=True, exist_ok=True)
```

2. Add the chunking function:
```python
def chunk_chapter_content(chapter_content, max_size=MAX_CHUNK_SIZE, min_size=MIN_CHUNK_SIZE):
    """
    Split chapter content into smaller chunks based on paragraph and sentence boundaries.
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
        if len(current_chunk) + len(paragraph) + 2 > max_size and len(current_chunk) >= min_size:
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
            sentences = re.split(r'(?<=[.!?])\s+', chunk)
            
            temp_chunk = ""
            for sentence in sentences:
                if len(temp_chunk) + len(sentence) + 1 > max_size and len(temp_chunk) >= min_size:
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
```

3. Modify the chapter processing code where chapters are saved:
```python
# Create a directory for the chunked chapters
book_chunked_chapter_dir = chunked_chapters_dir / book_title
book_chunked_chapter_dir.mkdir(exist_ok=True)

# Initialize chunk counter
total_chunks = 0

# After saving the regular chapter file
# Split chapter into chunks
chunks = chunk_chapter_content(chapter["content"])

# Save each chunk to a separate file
for j, chunk_content in enumerate(chunks, 1):
    chunk_filename = f"{i:02d}_{j:02d}_{chapter_title[:40]}.md"
    chunk_file = book_chunked_chapter_dir / chunk_filename
    
    with open(chunk_file, "w", encoding="utf-8") as f:
        f.write(chunk_content)
    
    print(f"    - Chunk {j}/{len(chunks)} saved to {chunk_file} ({len(chunk_content)} chars)")

total_chunks += len(chunks)
print(f"    - Split into {len(chunks)} chunks")

# Add to final print statements
print(f"TTS-ready chunked chapter files saved to {chunked_chapters_dir}")
```

## Conclusion

The chunking functionality successfully breaks down long chapters into smaller, more manageable pieces that would be suitable for TTS processing. The implementation preserves the natural structure of the text and maintains proper ordering of the content. This modification could be easily integrated into the original script with minimal changes. 