# Markdown Publisher

A command-line utility that processes Markdown files and converts them into properly formatted EPUB documents with enhanced readability and structure.

## Features

- Fixes broken Markdown links that span multiple lines
- Improves paragraph spacing for better readability
- Creates EPUB files with proper chapter structure based on level-2 headings
- Adds metadata (title, author, date) to the generated EPUB
- Generates a table of contents (optional)
- Supports custom author attribution
- Debug mode for troubleshooting

## Requirements

- Python 3.6 or higher
- Pandoc installed and available in PATH

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/md_publish.git
cd md_publish
```

2. Ensure Pandoc is installed on your system. Installation instructions can be found at [pandoc.org](https://pandoc.org/installing.html).

## Usage

Basic usage:
```bash
python md_publish.py input.md
```

### Command-line Options

- `input_file`: The Markdown file to process
- `--author`: Set custom author name (default: "Rory Scott")
- `--debug`: Keep the processed markdown file after EPUB creation
- `--no-toc`: Disable table of contents generation

### Examples

1. Create EPUB with default settings:
```bash
python md_publish.py document.md
```

2. Create EPUB with custom author:
```bash
python md_publish.py document.md --author "John Smith"
```

3. Create EPUB without table of contents:
```bash
python md_publish.py document.md --no-toc
```

4. Keep processed markdown file for debugging:
```bash
python md_publish.py document.md --debug
```

## How It Works

1. The utility reads the input Markdown file
2. Extracts the title from the first H1 heading (or uses filename if none found)
3. Fixes multi-line link formatting issues
4. Adjusts paragraph spacing for improved readability
5. Generates an EPUB file using Pandoc with:
   - Proper chapter structure
   - Metadata (title, author, date)
   - Table of contents (if enabled)
   - Consistent formatting

## Output

The script generates:
- An EPUB file named after the document title (spaces replaced with hyphens)
- A temporary processed markdown file (removed unless in debug mode)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 