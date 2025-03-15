# Minimal Changes for Chapter Chunking

Based on our experiment, here are the minimal changes needed to modify `clean-markdown-for-tts.py` to add chapter chunking functionality:

## 1. Add Chunking Parameters

```python
# Add these parameters at the top of the file
chunked_chapters_dir = Path("output/tts-ready-chapters-chunks")
MAX_CHUNK_SIZE = 5000  # Maximum characters per chunk
MIN_CHUNK_SIZE = 1000  # Minimum characters for a chunk to be considered valid

# Add this to directory creation section
chunked_chapters_dir.mkdir(parents=True, exist_ok=True)
```

## 2. Add the Chunking Function

```python
def chunk_chapter_content(chapter_content, max_size=MAX_CHUNK_SIZE, min_size=MIN_CHUNK_SIZE):
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

## 3. Modify the Main Processing Loop

Add these lines where chapters are processed:

```python
# Add after creating the regular chapter directory
book_chunked_chapter_dir = chunked_chapters_dir / book_title
book_chunked_chapter_dir.mkdir(exist_ok=True)

# Add a counter for reporting
total_chunks = 0

# After saving the regular chapter file, add:
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

# Update the final print statement
print(f"Split {len(chapters)} chapters from {md_file.name} into {total_chunks} total chunks")
```

## 4. Add Final Output Messages

```python
print(f"TTS-ready chunked chapter files saved to {chunked_chapters_dir}")

# Optionally add statistics about the chunked files
total_files = len(list(chunked_chapters_dir.glob("**/*.md")))
print(f"Total chunked files created: {total_files}")
```

These changes preserve all the existing functionality while adding chapter chunking with minimal modifications to the original script. 