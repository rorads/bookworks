# Experimentation Methodology for AI-Enhanced TTS Preparation

## 1. Overview

This document outlines the methodology for experimenting with AI-enhanced text-to-speech (TTS) processing within the Bookworks project. The goal is to develop a robust pipeline that transforms raw book content into high-quality audio through AI-assisted processing.

## 2. Problem Statement

Current TTS engines require properly formatted text to produce natural-sounding audio. Our existing clean-markdown-for-tts.py script performs basic cleaning, but has several limitations:

1. Reliance on regex patterns that may miss complex formatting cases
2. Inability to understand context-dependent text structures
3. Limited handling of special content like dialogue, quotes, and parentheticals
4. No optimization for natural speech patterns and pauses
5. Inability to handle specialized vocabulary, acronyms, and numbers

By leveraging AI models (specifically GPT-4), we aim to develop a more sophisticated text preparation pipeline that addresses these limitations.

## 3. Experimentation Approach

### 3.1 Data Collection

- Sample chapters from various genres and writing styles (epubs / markdown found in `tests/test_data`)
- Content with different formatting challenges (dialogues, lists, tables, etc.)
- Books with specialized vocabulary or terminology
- Material with acronyms, numbers, and special characters

### 3.2 Processing Pipeline

1. **Input Stage**: Convert EPUB/PDF to raw markdown (using and maybe enhancing existing epub-to-markdown-for-tts.py)
2. **Baseline Cleaning**: Process with current clean-markdown-for-tts.py script
3. **AI Enhancement**: Apply GPT-4 processing with specialized prompts
4. **TTS Preparation**: Final formatting adjustments specific to the target TTS engine
5. **Audio Generation**: Convert to speech using selected TTS provider
6. **Analysis**: Evaluate quality using experiment_utils.py

### 3.3 AI-Enhancement Experiments

We will test different approaches with GPT-4:

1. **Prompt Engineering**:
   - Develop specialized prompts focused on TTS optimization
   - Test different instruction styles and specificity levels
   - Iterate based on output analysis

2. **Processing Strategies**:
   - Whole-chapter processing vs. segment-by-segment approach
   - Multi-pass processing (clean → enhance → optimize)
   - Context-aware processing with chapter/book information

3. **Model Parameters**:
   - Test different temperature and top_p settings
   - Evaluate impact of system prompts vs. user prompts
   - Compare cost/performance tradeoffs

> [!NOTE]
> We will be using the relatively new 'responses' api within the openai python client to interact with GPT-4. This is because we may want to analyse images and audio as well as text, and this api supports a streaming response format which we can use to stream the response to a file as it is generated.

## 4. Evaluation Metrics

We will assess the quality of AI-enhanced TTS preparation using:

### 4.1 Content Metrics
- Preservation of original meaning and information
- Correct handling of special text elements (quotes, lists, etc.)
- Proper formatting of numbers, dates, and specialized terms

### 4.2 Technical Metrics
- Processing time per chapter
- Token usage and cost
- Error rates and edge case handling

### 4.3 Comparison Methods
- Human evaluator ratings of audio samples
- Side-by-side comparisons of baseline vs. AI-enhanced outputs
- Automated analysis using experiment_utils.py for token counts, diffs, etc.

## 5. Experimental Design

### 5.1 Test Cases

Test data will include a blend of the following and can be expanded to include more diverse test cases as performance improves.

1. **Simple Narrative**: Fiction with straightforward prose
2. **Dialogue-Heavy**: Content with extensive character dialogue
3. **Technical Content**: Non-fiction with specialized terminology
4. **Mixed Formatting**: Content with lists, tables, and varied structure
5. **Edge Cases**: Content with unusual formatting, languages, or symbols

### 5.2 Control Variables

For each test case, maintain:
- Consistent base markdown content
- Same TTS engine and voice settings
- Equivalent content length when possible

### 5.3 Workflow

For each experiment:
1. Document specific AI enhancement approach
2. Process test cases through the pipeline
3. Generate audio samples
4. Analyze outputs using experiment_utils.py
5. Document findings and iterate

## 6. Implementation Path

### 6.1 Phase 1: Proof of Concept
- Develop initial AI enhancement prompts
- Test on limited sample content
- Evaluate basic quality improvements

### 6.2 Phase 2: Refinement
- Optimize prompts based on Phase 1
- Expand test cases
- Develop metrics for systematic evaluation

### 6.3 Phase 3: Integration
- Implement best approach into production code
- Create user interface for AI enhancement options
- Develop cost-effective processing pipeline

### 6.4 Phase 4: Production
- Release feature as part of Bookworks
- Monitor performance and gather user feedback
- Iterate based on real-world usage

## 7. Tooling and Infrastructure

### 7.1 Experiment Utilities

Enhance experiment_utils.py to support:
- Sampling content from different processing stages
- Calculating quality metrics for TTS preparation
- Generating diffs to visualize AI enhancements
- Estimating cost and performance metrics

### 7.2 Data Management

- Maintain a repository of test cases
- Track processing results across experiments
- Version control prompts and parameters

### 7.3 Processing Environment

- Set up consistent API access for GPT-4 (using the responses api)
- Establish baseline TTS generation environment
- Ensure repeatable experiment conditions

## 8. Initial Experiments

### Experiment 1: Basic Prompt Engineering

**Objective**: Determine optimal instruction format for GPT-4 text enhancement

**Variables**:
- Prompt specificity (general vs. detailed instructions)
- Examples inclusion (zero-shot vs. few-shot)
- System vs. user prompt placement

**Measurement**: Compare output quality using experiment_utils.py

### Experiment 2: Processing Granularity

**Objective**: Determine optimal chunk size for processing

**Variables**:
- Full chapter processing
- Paragraph-level processing
- Section-based processing (by headings)

**Measurement**: Token efficiency, output consistency, processing time

### Experiment 3: Multi-pass Processing

**Objective**: Evaluate benefits of staged enhancement

**Variables**:
- Single comprehensive prompt
- Two-stage: cleanup then enhancement
- Three-stage: cleanup, enhancement, and TTS optimization

**Measurement**: Quality improvements vs. cost and complexity

---
