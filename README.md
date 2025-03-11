# Bookworks

A versatile suite of tools for converting and transforming books between different formats. Currently supports:
- Converting Markdown to EPUB with enhanced formatting
- (Coming Soon) Generating audiobooks from Markdown content

## Features

### Markdown to EPUB Conversion
- Browser-based interface for easy file conversion
- Command-line interface for automation and scripting
- Fixes broken Markdown links that span multiple lines
- Improves paragraph spacing for better readability
- Creates EPUB files with proper chapter structure based on level-2 headings
- Adds metadata (title, author, date) to the generated EPUB
- Generates a table of contents (optional)
- Supports custom author attribution
- Debug mode for troubleshooting

### Audiobook Generation (Coming Soon)
- Convert markdown content into high-quality audio segments
- Support for different voices and reading styles
- Chapter-based audio generation
- Metadata embedding in audio files

### Development Features
- Docker support for containerized deployment
- Comprehensive test suite
- Easy to extend with new conversion tools

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
git clone https://github.com/rorads/bookworks.git
cd bookworks
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Ensure Pandoc is installed on your system. Installation instructions can be found at [pandoc.org](https://pandoc.org/installing.html).

### Using Docker

1. Clone this repository:
```bash
git clone https://github.com/rorads/bookworks.git
cd bookworks
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

The project includes a comprehensive test suite that covers both the command-line utilities and the web interface. Tests are written using pytest and can be run using:

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

### Markdown to EPUB Conversion

Basic usage:
```bash
python -m bookworks.md_publish input.md
```

#### Command-line Options

- `input_file`: The Markdown file to process
- `--author`: Set custom author name (default: "Author Not Specified")
- `--debug`: Keep the processed markdown file after EPUB creation
- `--no-toc`: Disable table of contents generation

#### Examples

1. Create EPUB with default settings:
```bash
python -m bookworks.md_publish document.md
```

2. Create EPUB with custom author:
```bash
python -m bookworks.md_publish document.md --author "John Smith"
```

3. Create EPUB without table of contents:
```bash
python -m bookworks.md_publish document.md --no-toc
```

4. Keep processed markdown file for debugging:
```bash
python -m bookworks.md_publish document.md --debug
```

### Audiobook Generation

Coming soon! This feature will allow you to convert markdown content into high-quality audio segments.

## License

This project is licensed under the GNU General Public License v3.0.

## Author

Created and maintained by Rory Scott. 