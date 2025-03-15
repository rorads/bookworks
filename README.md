# Bookworks

A versatile suite of tools for converting and transforming books between different formats. Currently supports:
- Converting Markdown to EPUB with enhanced formatting
- Text preparation for audiobook generation (TTS integration coming soon)

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

### Audiobook Generation
- Convert markdown content into high-quality audio segments
- Clean and prepare text for Text-to-Speech (TTS) processing
- Intelligent chapter chunking for optimal TTS performance
- Chapter-based audio generation
- Metadata embedding in audio files

**Note:** Actual TTS audio generation and GPT-enhanced text preparation are planned but not yet implemented. Currently, the project focuses on text preparation for TTS systems.

### Development Features
- Docker support for containerized deployment
- Comprehensive test suite
- Pre-commit hooks for code quality
- Type checking with mypy
- Linting with ruff
- Easy to extend with new conversion tools

## Requirements

### Local Development
- Python 3.10 or higher
- uv for dependency management
- Pandoc installed and available in PATH

### Docker
- Docker installed on your system
- No other dependencies needed

## Installation

### Using uv (Local Development)

1. Clone this repository:
```bash
git clone https://github.com/rorads/bookworks.git
cd bookworks
```

2. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies using uv:
```bash
uv sync
```

4. Ensure Pandoc is installed on your system. Installation instructions can be found at [pandoc.org](https://pandoc.org/installing.html).

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

## Development Workflow

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality. Install them after cloning the repository:

```bash
uv pip install pre-commit
pre-commit install
```

### Type Checking

Type checking is performed with mypy. Configuration is in mypy.ini:

```bash
uv run mypy .
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
- Text-to-Speech preparation tests
- File upload handling
- EPUB generation
- Error handling

To run tests manually or with specific options:

```bash
# Run with uv directly
uv run -m pytest

# Run specific test file
uv run -m pytest tests/test_app.py

# Run with verbose output
uv run -m pytest -v
```

## Usage

### Markdown to EPUB Conversion

Basic usage:
```bash
uv run python -m bookworks.md_publish input.md
```

#### Command-line Options

- `input_file`: The Markdown file to process
- `--author`: Set custom author name (default: "Author Not Specified")
- `--debug`: Keep the processed markdown file after EPUB creation
- `--no-toc`: Disable table of contents generation

#### Examples

1. Create EPUB with default settings:
```bash
uv run python -m bookworks.md_publish document.md
```

2. Create EPUB with custom author:
```bash
uv run python -m bookworks.md_publish document.md --author "John Smith"
```

3. Create EPUB without table of contents:
```bash
uv run python -m bookworks.md_publish document.md --no-toc
```

4. Keep processed markdown file for debugging:
```bash
uv run python -m bookworks.md_publish document.md --debug
```

### Audiobook Generation

The project includes tools to prepare markdown content for Text-to-Speech processing.

Basic usage:
```bash
uv run python -m bookworks.clean_for_tts input.md
```

#### Command-line Options

- `input_file`: The Markdown file to process
- `--output-dir`: Directory to store processed files (default: "./output")
- `--chunk-size`: Maximum size of chapter chunks in characters (default: 4000)
- `--debug`: Enable debug output

#### Examples

1. Clean markdown for TTS with default settings:
```bash
uv run python -m bookworks.clean_for_tts document.md
```

2. Clean markdown with custom output directory:
```bash
uv run python -m bookworks.clean_for_tts document.md --output-dir "./tts-ready"
```

3. Clean markdown with custom chunk size:
```bash
uv run python -m bookworks.clean_for_tts document.md --chunk-size 5000
```

## Experimentation Framework

The project includes an experimentation framework specifically designed for developing with AI coding agents:

### Agent-Driven Development
- The .cursor directory contains rules to guide AI agents in their development work
- Rules provide guidance on code style, testing, and experimental methodology
- Examples include use-tools-for-nice-python, experimentation_approach, and do-not-write-prose-in-code

### Experiment Structure
- Each experiment is organized in a dated directory (e.g., `experiments/audio_gen/2025-03-14_chapter-chunking/`)
- Experiments include a STATUS.yaml file tracking progress
- Documentation includes experiment_plan.md and experiment_results.md

### Running Experiments
To run an experiment:

```bash
cd experiments/audio_gen/[experiment-folder]
uv run python [experiment-script].py
```

Results are typically stored in the `output` directory of each experiment.

## License

This project is licensed under the GNU General Public License v3.0.

## Author

Created and maintained by Rory Scott. 