"""
CLI utility for analyzing experimental text processing outputs.

This tool helps AI agents analyze and compare text processing results by sampling
chapters from the output directory and providing detailed metrics.

Key features:
- Sample chapters from each output subdirectory
- Analyze content metrics (tokens, words, reading time)
- Extract representative excerpts (beginning, middle, end)
- Compare different versions of processed text
- Output formatted analysis to stdout or files
- Support JSON output for programmatic consumption

Example usage:
  python experiment_utils.py --samples 3 --excerpt-size 1000
  python experiment_utils.py --dir output/tts-ready-chapters --format json
  python experiment_utils.py --compare output/clean-markdown-for-tts output/enhanced-markdown
"""

import argparse
from pathlib import Path
import random
import re
from typing import List, Dict, Tuple, Optional, Union, Callable, Any
import tiktoken
import difflib
from dataclasses import dataclass
import json
import sys
from collections import defaultdict

# --- Data Models ---

@dataclass
class TextSample:
    """Represents a sample of text with detailed metrics."""
    file_path: Path
    first_excerpt: str
    middle_excerpt: str
    last_excerpt: str
    total_tokens: int
    word_count: int
    reading_time_minutes: float
    
@dataclass
class DiffAnalysis:
    """Analysis of differences between two text versions."""
    additions: int
    deletions: int
    changes: int
    diff_text: str
    improvement_score: float  # Heuristic measure of improvement

# --- File System Utilities ---

def get_output_directories(root_dir: Path = Path("output")) -> List[Path]:
    """Get all subdirectories in the output directory."""
    
def get_chapter_files(directory: Path, file_pattern: str = "*.md") -> List[Path]:
    """Get all chapter files in a directory matching the given pattern."""
    
def sample_chapters(directories: List[Path], 
                   samples_per_dir: int = 5, 
                   seed: Optional[int] = None) -> Dict[Path, List[Path]]:
    """Sample a specific number of chapters from each directory."""

def find_corresponding_files(file_path: Path, target_dir: Path) -> Optional[Path]:
    """Find corresponding file in another directory based on name similarity."""

# --- Text Analysis Utilities ---

def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """Count the number of tokens in the text using tiktoken."""
    
def estimate_word_count(text: str) -> int:
    """Estimate the number of words in the text."""
    
def estimate_reading_time(word_count: int, wpm: int = 200) -> float:
    """Estimate reading time in minutes based on word count and reading speed."""
    
def extract_text_excerpts(text: str, 
                         first_n: int = 2000, 
                         middle_n: int = 2000, 
                         last_n: int = 2000,
                         by_words: bool = False) -> Tuple[str, str, str]:
    """Extract the first, middle, and last n characters or words from the text."""

def truncation_summary(text: str, 
                      model_name: str = "gpt-4", 
                      max_tokens: int = 8000) -> Dict[str, Any]:
    """Check if text exceeds model token limits and by how much."""

# --- Comparison Utilities ---

def generate_diff(original_text: str, enhanced_text: str) -> str:
    """Generate a unified diff between original and enhanced text."""
    
def analyze_diff(diff: str) -> DiffAnalysis:
    """Analyze a diff to count additions, deletions, and changes."""

# --- Formatting Utilities ---

def format_sample_output(sample: TextSample, excerpt_size: int = 2000) -> str:
    """Format a text sample for display in the terminal."""
    
def format_diff_output(diff_analysis: DiffAnalysis) -> str:
    """Format diff analysis for display in the terminal."""

def output_json(data: Any) -> str:
    """Convert data to formatted JSON string."""

# --- Analysis Functions ---

def analyze_chapter(file_path: Path, 
                   excerpt_size: int = 2000,
                   by_words: bool = False,
                   model_name: str = "gpt-4") -> TextSample:
    """Analyze a single chapter file."""
    
def compare_chapter_versions(original_path: Path, 
                            enhanced_path: Path) -> DiffAnalysis:
    """Compare original and enhanced versions of a chapter."""
    
def batch_analyze_samples(sample_dict: Dict[Path, List[Path]], 
                         excerpt_size: int = 2000,
                         by_words: bool = False,
                         model_name: str = "gpt-4") -> Dict[Path, List[TextSample]]:
    """Analyze multiple chapter samples from multiple directories."""
    
def batch_compare_directories(source_dir: Path, 
                             target_dir: Path,
                             samples: int = 5) -> List[DiffAnalysis]:
    """Compare samples of files from two directories."""

# --- CLI Argument Handling ---

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze and compare text processing outputs."
    )
    parser.add_argument("--dir", type=str, default="output",
                        help="Root directory to analyze (default: output)")
    parser.add_argument("--samples", type=int, default=5,
                        help="Number of samples per directory (default: 5)")
    parser.add_argument("--excerpt-size", type=int, default=2000,
                        help="Size of text excerpts in characters (default: 2000)")
    parser.add_argument("--by-words", action="store_true",
                        help="Measure excerpt size in words instead of characters")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--model", type=str, default="gpt-4",
                        help="Model name for token counting (default: gpt-4)")
    parser.add_argument("--compare", type=str, nargs=2, metavar=('DIR1', 'DIR2'),
                        help="Compare files between two directories")
    parser.add_argument("--format", type=str, choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--output", type=str, help="Output file (default: stdout)")
    return parser.parse_args()

# --- Main Function ---

def main() -> None:
    """Main entry point for the CLI utility."""
    args = parse_arguments()
    
    # Handle directory comparison mode
    if args.compare:
        source_dir = Path(args.compare[0])
        target_dir = Path(args.compare[1])
        results = batch_compare_directories(source_dir, target_dir, args.samples)
        
        # Format and output results
        if args.format == "json":
            output = output_json(results)
        else:
            output = "\n\n".join(format_diff_output(r) for r in results)
    
    # Handle single directory analysis mode
    else:
        root_dir = Path(args.dir)
        directories = [root_dir] if root_dir.is_dir() else get_output_directories(root_dir)
        samples = sample_chapters(directories, args.samples, args.seed)
        results = batch_analyze_samples(samples, args.excerpt_size, args.by_words, args.model)
        
        # Format and output results
        if args.format == "json":
            output = output_json(results)
        else:
            output_parts = []
            for dir_path, samples in results.items():
                output_parts.append(f"\n{'=' * 80}\nDirectory: {dir_path}\n{'=' * 80}")
                for sample in samples:
                    output_parts.append(format_sample_output(sample, args.excerpt_size))
            output = "\n\n".join(output_parts)
    
    # Output the results
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
    else:
        print(output)

if __name__ == "__main__":
    main()


