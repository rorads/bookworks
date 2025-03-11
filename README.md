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
- Docker support for containerized deployment
- Comprehensive test suite

## Requirements

### Local Development
- Python 3.10 or higher
- Poetry for dependency management
- Pandoc installed and available in PATH

### Docker
- Docker installed on your system
- No other dependencies needed

## Installation

### Using Poetry (Local Development)

1. Clone this repository:
```bash
git clone https://github.com/yourusername/md_publish.git
cd md_publish
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Ensure Pandoc is installed on your system. Installation instructions can be found at [pandoc.org](https://pandoc.org/installing.html).

### Using Docker

1. Clone this repository:
```bash
git clone https://github.com/yourusername/md_publish.git
cd md_publish
```

2. Build and run using Make:
```bash
make docker-rebuild
```

The application will be available at http://localhost:5001

## Docker Commands

The following Make commands are available for Docker management:

```bash
make help           # Show available commands
make docker-rebuild # Rebuild and restart the Docker container
make docker-stop    # Stop and remove the Docker container
make docker-logs    # View container logs in follow mode
make test          # Run the test suite
```

## Testing

The project includes a comprehensive test suite that covers both the command-line utility and the web interface. Tests are written using pytest and can be run using:

```bash
make test
```

### Test Coverage

The test suite includes:
- Web interface functionality tests
- Markdown processing tests
- File upload handling
- EPUB generation
- Error handling

To run tests manually or with specific options:

```bash
# Run with Poetry directly
poetry run pytest

# Run specific test file
poetry run pytest tests/test_app.py

# Run with verbose output
poetry run pytest -v
```

## Usage

Basic usage:
```bash
python md_publish.py input.md
```

### Command-line Options

- `input_file`: The Markdown file to process
- `--author`: Set custom author name (default: "Author Not Specified")
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