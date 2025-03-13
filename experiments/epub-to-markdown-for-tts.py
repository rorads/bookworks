"""
This is an experimentation to test the feasibility of using a TTS model to read an epub file.

At the outset, it's possible to convert the epub to markdown using pandoc. However, the 
markdown it produces contains a lot of formatting markup which, when read out loud, would 
be redundant and jarring.

So, the next step is to try to clean up the markdown to remove the formatting markup.
"""

import os
import subprocess
from pathlib import Path
import glob

# Define the directory containing epub files
epub_dir = Path("tests/test_data/epub/")

# Create a dictionary to store the markdown content
epub_to_markdown = {}

# Check if the directory exists
if epub_dir.exists():
    # Find all epub files in the directory
    epub_files = glob.glob(str(epub_dir / "*.epub"))
    
    for epub_file in epub_files:
        epub_path = Path(epub_file)
        # Create a temporary output file path for the markdown
        output_md_path = f"temp_{epub_path.stem}.md"
        
        try:
            # Run pandoc to convert epub to markdown
            result = subprocess.run(
                ["pandoc", epub_file, "-o", output_md_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Read the generated markdown file
            with open(output_md_path, "r", encoding="utf-8") as md_file:
                markdown_content = md_file.read()
            
            # Store in dictionary
            epub_to_markdown[epub_path.name] = markdown_content
            
            # Clean up the temporary file
            os.remove(output_md_path)
            
        except subprocess.CalledProcessError as e:
            print(f"Error converting {epub_file}: {e}")
            epub_to_markdown[epub_path.name] = f"Error: {e.stderr}"
        except Exception as e:
            print(f"Unexpected error with {epub_file}: {e}")
            epub_to_markdown[epub_path.name] = f"Error: {str(e)}"
else:
    print(f"Directory {epub_dir} does not exist")

# Display the number of epub files processed
print(f"Processed {len(epub_to_markdown)} epub files")

# Create a directory to save the markdown files
output_dir = Path("output/markdown")
output_dir.mkdir(parents=True, exist_ok=True)

# Save each markdown file to the output directory
for epub_name, markdown_content in epub_to_markdown.items():
    # Create filename from the epub name (without .epub extension)
    filename = Path(epub_name).stem + ".md"
    output_path = output_dir / filename
    
    try:
        # Write the markdown content to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Saved markdown for {epub_name} to {output_path}")
    except Exception as e:
        print(f"Error saving {epub_name} to file: {e}")

print(f"Markdown files saved to {output_dir}")

