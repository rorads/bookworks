"""
Convert Markdown files to EPUB format with enhanced formatting and structure.
"""

import sys
import os
import datetime
import argparse
from typing import Tuple, Optional

from bookworks.bw_utils import (
    sanitize_filename,
    clean_markdown_content,
    run_pandoc_command,
    create_temp_workspace
)

# Define uploads directory relative to the module
UPLOAD_FOLDER = os.path.abspath('uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_markdown_content(content: str, author: str = "Author Not Specified", debug: bool = False, toc: bool = True) -> Tuple[Optional[str], Optional[str]]:
    """
    Process markdown content and convert it to EPUB format.
    
    Args:
        content: The markdown content to process
        author: The author name to include in the metadata
        debug: Whether to keep intermediate files for debugging
        toc: Whether to include a table of contents
        
    Returns:
        Tuple containing (output_file_path, error_message)
        If successful, error_message will be None
    """
    try:
        # Clean and process the markdown content
        modified_content, metadata = clean_markdown_content(content)
        title = metadata['title']
        
        # Get today's date in ISO format for publication date
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create a temporary directory for processing
        with create_temp_workspace() as temp_dir:
            # Sanitize the title for use in filename
            safe_title = sanitize_filename(title)
            
            # Create processed markdown file
            processed_md = os.path.join(temp_dir, f"{safe_title}_processed.md")
            with open(processed_md, 'w') as f:
                f.write(modified_content)
            
            # Create output filename
            output_epub = os.path.join(temp_dir, f"{safe_title}.epub")
            
            # Configure pandoc options
            pandoc_options = {
                'metadata': {
                    'title': title,
                    'author': author,
                    'date': today_date
                },
                'epub_chapter_level': 2,
                'toc': toc,
                'standalone': True
            }
            
            # Generate the EPUB using pandoc
            success, error = run_pandoc_command(processed_md, output_epub, pandoc_options)
            if not success:
                return None, error
            
            # Move the file to a more permanent location
            final_output = os.path.join(UPLOAD_FOLDER, f"{safe_title}.epub")
            os.rename(output_epub, final_output)
            
            # If in debug mode, save the processed markdown
            if debug:
                debug_md = os.path.join(UPLOAD_FOLDER, f"{safe_title}_processed.md")
                os.rename(processed_md, debug_md)
            
            return final_output, None
            
    except Exception as e:
        return None, f"Error processing markdown: {str(e)}"

def process_markdown_file(filepath: str, author: str = "Author Not Specified", debug: bool = False, toc: bool = True) -> Tuple[Optional[str], Optional[str]]:
    """
    Process a markdown file and convert it to EPUB format.
    
    Args:
        filepath: Path to the markdown file
        author: The author name to include in the metadata
        debug: Whether to keep intermediate files for debugging
        toc: Whether to include a table of contents
        
    Returns:
        Tuple containing (output_file_path, error_message)
        If successful, error_message will be None
    """
    try:
        if not os.path.exists(filepath):
            return None, f"File not found: {filepath}"
            
        with open(filepath, "r") as f:
            content = f.read()
            
        return process_markdown_content(content, author, debug, toc)
        
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a Markdown file to fix formatting issues and create a properly formatted EPUB.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create EPUB with default author (Author Not Specified)
  python -m bookworks.md_publish document.md
  
  # Create EPUB with custom author
  python -m bookworks.md_publish document.md --author "John Smith"
  
  # Create EPUB without table of contents
  python -m bookworks.md_publish document.md --no-toc
  
  # Keep the processed markdown file for debugging
  python -m bookworks.md_publish document.md --debug
"""
    )
    
    parser.add_argument("input_file", nargs="?", help="Input Markdown file to process")
    parser.add_argument("--author", default="Author Not Specified", help="Author name for EPUB metadata")
    parser.add_argument("--debug", action="store_true", help="Keep the processed markdown file")
    parser.add_argument("--no-toc", action="store_true", help="Disable table of contents generation")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    if not args.input_file:
        parser.print_help()
        sys.exit(1)
    
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)
    
    output_file, error = process_markdown_file(args.input_file, args.author, args.debug, not args.no_toc)
    if error:
        print(error, file=sys.stderr)
        sys.exit(1)
    print(f"Successfully created: {output_file}") 