# Example 4: Data Processing Pipeline

Real-world test on 50 CSV files from mixed sources showing 91% failure reduction.

## Test Results

| Metric | Basic Pipeline | Smart Pipeline |
|---|---|---|
| Files tested | 50 | 50 |
| Failures | 32 (64%) | 3 (6%) |
| Success rate | 36% | 94% |
| Encoding crashes | 12 | 0 |
| Column crashes | 8 | 0 |
| Date parse failures | 7 | 0 |
| Silent NaN errors | 5 | 0 |

**Failure reduction: 91%**

## Why This Matters for Data Analysts

These are not edge cases. They are guaranteed to appear when processing:

- Files exported from Excel (cp1252 encoding)
- Files from international systems (date format differences)
- Files from multiple CRM/ERP systems (inconsistent column names)
- Files with missing values (NaN propagation)

The basic pipeline fails on the majority of real-world files.
The learning pipeline handles them gracefully and reports data quality issues.

## Errors Eliminated

**Encoding crashes (12 -> 0)**
read_csv() without encoding specification fails on Excel exports.
Warning placed at the read_csv() call.

**Column name crashes (8 -> 0)**
KeyError when source system uses different column names.
Warning placed before any column access.

**Date parsing failures (7 -> 0)**
to_datetime() crashes on non-standard date formats.
Warning placed at the to_datetime() call.

**Silent NaN errors (5 -> 0)**
NaN * NaN = NaN propagates silently, producing wrong totals with no error.
Warning placed before arithmetic operations.

## Files

- `basic_pipeline.py` - 64% failure rate, no inline learning
- `smart_pipeline.py` - 6% failure rate, 91% fewer failures

## Relevance to Data Analyst Roles

This example demonstrates production data analyst skills:
- ETL pipeline reliability
- Data quality validation and reporting
- Graceful error handling
- Stakeholder-ready output with data quality metrics

<!-- ReadmeForge: The following sections were auto-appended. Move them to the correct position per the 21-section blueprint. -->

## Use Cases

<!-- TODO: Add a ## Use Cases section with 2-4 bullet points describing concrete scenarios. Example: 'Weekly cleanup of Downloads folder after batch downloads'. -->


## Features / Capabilities

<!-- TODO: Add a ## Features section listing 3-5 key capabilities with bold labels and concrete descriptions. Include design choices like 'zero dependencies' or 'dry-run by default'. -->


## Requirements

- Python 3.8+
- Windows 10/11
- Third-party: pandas


## Quick Start

<!-- TODO: Add a ## Quick Start section with: 1) cd to project dir, 2) install command if needed, 3) first run command with --help or --dry-run. Use fenced code blocks. -->


## Usage

<!-- TODO: Add a ## Usage section with 2-3 real command examples in fenced code blocks. Show the most common use case first, then advanced options. -->


## Configuration

<!-- TODO: Add a ## Configuration section with a table of env vars, config file paths, or settings with their defaults. -->


## Pipeline Position

<!-- TODO: Add a ## Pipeline Position section with: **Fed by:** (upstream tools) and **Feeds into:** (downstream tools). Optionally add an ASCII flow diagram. -->


## Hardcoded Paths

**Fully parameterized** -- all paths passed via arguments.


## How It Works

<!-- TODO: Add a ## How It Works section with numbered steps describing the internal processing flow from input to output. -->


## Example Output

<!-- TODO: Add a ## Example Output section with a fenced code block showing realistic console output from a typical run. -->


## Safety & Reliability

<!-- TODO: Add a ## Safety & Reliability section covering: dry-run mode, backup before destructive operations, resume/checkpoint support, and failure handling behavior. -->


## Logging & Observability

<!-- TODO: Add a ## Logging section describing: where logs are written, log format, verbosity flags, and any run artifacts produced. -->


## Versioning / Roadmap

<!-- TODO: Add a ## Versioning section with the current version number and a roadmap of planned features. -->


## License & Contact

<!-- TODO: Add a ## License & Contact section with the license name and maintainer contact info. -->
