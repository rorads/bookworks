import re
import sys
import os
import subprocess
import datetime
import argparse
import tempfile

def sanitize_filename(title):
    # Remove or replace characters that could cause issues in filenames
    # Replace newlines and other problematic characters with hyphens
    sanitized = re.sub(r'[\r\n\t/\\:*?"<>|]', '-', title)
    # Replace multiple hyphens with single hyphen
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens and spaces
    sanitized = sanitized.strip('- ')
    return sanitized or "untitled"

def process_markdown_content(content, author="Author Not Specified", debug=False, toc=True):
    # Extract the title from the first h1 heading
    title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Untitled Document"
    
    # Get today's date in ISO format for publication date
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Fix broken links with multi-line link text
    def clean_link_text(match):
        link_text = match.group(1)
        cleaned_text = re.sub(r'\s+', ' ', link_text).strip()
        return f"([{cleaned_text}]("
    
    # Apply the link fixing
    modified_links = re.sub(r'\(\[([\s\S]*?)\]\(', clean_link_text, content)
    
    # Add extra newline after paragraphs but not after headings
    modified_newlines = re.sub(r"([^\n])\n(?![\n#])", r"\1\n\n", modified_links)
    
    # Sanitize the title for use in filename
    safe_title = sanitize_filename(title)
    output_epub = f"{safe_title}.epub"
    
    # Create processed markdown file with a predictable name in debug mode
    if debug:
        processed_md = f"{safe_title}_processed.md"
        with open(processed_md, 'w') as f:
            f.write(modified_newlines)
    else:
        # Use temporary file in non-debug mode
        with tempfile.NamedTemporaryFile(mode='w', suffix='_processed.md', delete=False) as temp_md:
            temp_md.write(modified_newlines)
            processed_md = temp_md.name
    
    # Generate the EPUB using pandoc
    command = [
        "pandoc", 
        processed_md, 
        "-o", output_epub, 
        "--epub-chapter-level=2", 
        f"--metadata=title:{title}",
        f"--metadata=author:{author}",
        f"--metadata=date:{today_date}"
    ]
    
    if toc:
        command.extend(["--toc", "--toc-depth=3"])
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if not debug:
            os.remove(processed_md)
        return output_epub, None
    except subprocess.CalledProcessError as e:
        error_msg = f"Error: {e.stderr}"
        if os.path.exists(processed_md):
            os.remove(processed_md)
        if os.path.exists(output_epub):
            os.remove(output_epub)
        return None, error_msg

def process_markdown_file(input_file, author="Author Not Specified", debug=False, toc=True):
    try:
        with open(input_file, 'r') as f:
            content = f.read()
        return process_markdown_content(content, author, debug, toc)
    except FileNotFoundError:
        return None, f"Error: File '{input_file}' not found."

if __name__ == "__main__":
    # Original CLI code remains unchanged
    parser = argparse.ArgumentParser(
        description="Process a Markdown file to fix formatting issues and create a properly formatted EPUB.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create EPUB with default author (Author Not Specified)
  python fix_spacing.py document.md
  
  # Create EPUB with custom author
  python fix_spacing.py document.md --author "John Smith"
  
  # Create EPUB without table of contents
  python fix_spacing.py document.md --no-toc
  
  # Keep the processed markdown file for debugging
  python fix_spacing.py document.md --debug
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
        print(error)
        sys.exit(1)
    print(f"EPUB successfully created: {output_file}") 