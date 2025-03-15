# Chapter Chunking Experiment

## Aim
To modify the existing `clean-markdown-for-tts.py` script to add functionality for splitting long chapters into smaller, more manageable chunks for better TTS processing.

## Approach
1. Add a new function to split chapter content into smaller chunks based on:
   - Maximum character count per chunk
   - Natural paragraph boundaries to maintain readability
   - Proper sentence boundaries to avoid cutting mid-sentence

2. Modify the existing script workflow to apply this chunking after chapters have been identified and before they are written to files.

3. Create a configurable chunk size parameter that can be adjusted as needed.

## Files to Create/Modify

### Modified Script
- `experiments/audio_gen/chapter_chunking/clean-markdown-for-tts-chunked.py`: A modified version of the original script with chunking functionality added

### Result Files for Testing
- We'll use the existing output directory structure, but add a "-chunks" suffix to directories to distinguish:
  - `output/tts-ready-chapters-chunks/{book_title}/{chapter_number}_{chunk_number}_{title}.md`

## Modification Approach
The most concise modification will involve:

1. Adding a new `chunk_chapter_content` function to split chapter content
2. Updating the chapter saving part of the script to use this function
3. Adding a configurable parameter for chunk size

## Success Measures
- Successfully split chapters into smaller chunks that respect paragraph and sentence boundaries
- Maintain the readability and flow of the narrative
- Generate files with reasonable naming that preserves the original ordering
- Files should not exceed the specified maximum size

## Testing Plan
- Run the modified script on sample markdown files
- Verify that chapters are properly split
- Inspect the resulting chunk files for proper content boundaries

This approach will allow for minimal changes to the existing codebase while adding the required functionality. 