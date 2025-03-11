"""
Convert Markdown files to EPUB format with enhanced formatting and structure.
"""

import os
import tempfile
import subprocess
from typing import Tuple, Optional

def process_markdown_content(content: str, author: str = "Author Not Specified") -> Tuple[str, Optional[str]]:
    """
    Process markdown content and convert it to EPUB format.
    
    Args:
        content: The markdown content to process
        author: The author name to include in the metadata
        
    Returns:
        Tuple containing (output_file_path, error_message)
        If successful, error_message will be None
    """
    try:
        # Create a temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary input file
            input_file = os.path.join(temp_dir, "input.md")
            with open(input_file, "w") as f:
                f.write(content)
            
            # Extract title from first H1 heading or use default
            title = "Untitled"
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            
            # Create output filename
            output_file = os.path.join(temp_dir, f"{title.replace(' ', '-')}.epub")
            
            # Run pandoc command
            cmd = [
                "pandoc",
                input_file,
                "-o", output_file,
                "--metadata", f"title={title}",
                "--metadata", f"author={author}",
                "--toc",
                "--standalone"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return None, f"Pandoc error: {result.stderr}"
            
            # Move the file to a more permanent location
            final_output = os.path.join("uploads", os.path.basename(output_file))
            os.rename(output_file, final_output)
            
            return final_output, None
            
    except Exception as e:
        return None, f"Error processing markdown: {str(e)}"

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert Markdown to EPUB with enhanced formatting")
    parser.add_argument("input_file", help="The markdown file to process")
    parser.add_argument("--author", default="Author Not Specified", help="Set the author name")
    parser.add_argument("--debug", action="store_true", help="Keep temporary files")
    parser.add_argument("--no-toc", action="store_true", help="Disable table of contents")
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, "r") as f:
            content = f.read()
        
        output_file, error = process_markdown_content(content, args.author)
        if error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
        print(f"Successfully created: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1) 