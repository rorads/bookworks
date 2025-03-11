import re
import sys
import os
import subprocess
import datetime
import argparse

def process_markdown_file(input_file, author="Rory Scott", debug=False, toc=True):
    # Read the content of the input file
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Extract the title from the first h1 heading
    title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
    else:
        # Use the filename as title if no h1 heading is found
        title = os.path.splitext(os.path.basename(input_file))[0]
    
    # Get today's date in ISO format for publication date
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Fix broken links with multi-line link text
    def clean_link_text(match):
        # Get the text between the brackets, and clean it by replacing newlines and excess whitespace with single spaces
        link_text = match.group(1)
        cleaned_text = re.sub(r'\s+', ' ', link_text).strip()
        return f"([{cleaned_text}]("
    
    # Apply the link fixing, capturing everything between brackets even across multiple lines
    modified_links = re.sub(r'\(\[([\s\S]*?)\]\(', clean_link_text, content)
    
    # Add extra newline after paragraphs but not after headings
    modified_newlines = re.sub(r"([^\n])\n(?![\n#])", r"\1\n\n", modified_links)
    
    # Generate the output filenames
    base_name = os.path.splitext(input_file)[0]
    processed_md = f"{base_name}_processed.md"
    output_epub = f"{title.replace(' ', '-')}.epub"
    
    # Write the processed markdown to a new file
    with open(processed_md, 'w') as f:
        f.write(modified_newlines)
    
    print(f"Processed markdown saved to: {processed_md}")
    
    # Generate the EPUB using pandoc with TOC
    command = [
        "pandoc", 
        processed_md, 
        "-o", output_epub, 
        "--epub-chapter-level=2", 
        f"--metadata=title:{title}",
        f"--metadata=author:{author}",
        f"--metadata=date:{today_date}"
    ]
    
    # Add table of contents if requested
    if toc:
        command.append("--toc")
        command.append("--toc-depth=3")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"EPUB successfully created: {output_epub}")
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"Date: {today_date}")
        
        # Remove the processed markdown file unless debug mode is enabled
        if not debug and os.path.exists(processed_md):
            os.remove(processed_md)
            print(f"Removed temporary file: {processed_md}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating EPUB: {e}")
        print(f"Pandoc stdout: {e.stdout}")
        print(f"Pandoc stderr: {e.stderr}")

if __name__ == "__main__":
    # Set up argument parser with detailed help information
    parser = argparse.ArgumentParser(
        description="Process a Markdown file to fix formatting issues and create a properly formatted EPUB.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create EPUB with default author (Rory Scott)
  python fix_spacing.py document.md
  
  # Create EPUB with custom author
  python fix_spacing.py document.md --author "John Smith"
  
  # Create EPUB without table of contents
  python fix_spacing.py document.md --no-toc
  
  # Keep the processed markdown file for debugging
  python fix_spacing.py document.md --debug

Description:
  This script performs the following operations:
  1. Fixes broken Markdown links that span multiple lines
  2. Adds proper paragraph spacing to improve readability
  3. Creates an EPUB with chapters based on level-2 headings
  4. Adds metadata (title, author, date) to the EPUB
  5. Generates a table of contents for the EPUB (unless --no-toc is specified)

Requirements:
  - Python 3.6+
  - Pandoc installed and available in PATH
"""
    )
    
    parser.add_argument(
        "input_file", 
        nargs="?",  # Make input_file optional
        help="Input Markdown file to process"
    )
    
    parser.add_argument(
        "--author", 
        default="Rory Scott", 
        help="Author name for EPUB metadata (default: 'Rory Scott')"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Keep the processed markdown file after EPUB creation for debugging"
    )
    
    parser.add_argument(
        "--no-toc", 
        action="store_true",
        help="Disable table of contents generation in the EPUB"
    )
    
    # If no arguments were provided, print help and exit
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
    
    process_markdown_file(args.input_file, args.author, args.debug, not args.no_toc) 