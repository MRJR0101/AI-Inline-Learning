# Example 1: Basic Before/After

The simplest demonstration of the AI Inline Learning pattern.

## What This Shows

Four common mistakes AI assistants make repeatedly without inline warnings:

1. No request timeout - scripts hang on dead servers
2. No User-Agent header - gets blocked as a bot
3. No HTTP error check - silently processes 404 pages as valid content
4. No file encoding - crashes on non-ASCII content on Windows

## The Fix

Each warning is placed at the exact line where the mistake happens.
Future AI sessions read the warning and apply the correct behavior automatically.

## Files

- `before.py` - Code without inline learning (makes all four mistakes)
- `after.py` - Code with inline learning comments (avoids all four)

## Pattern Used

```python
# HEY CLAUDE: [Attention grabber]
# MISTAKE: [What went wrong and when]
# LESSON: [Why it happened]
# RULE: [What to do instead]
```

## Key Insight

The warnings are not in a separate log file or external document.
They live at the exact decision point where the error would occur.
AI cannot miss them because it reads the code top to bottom.

<!-- ReadmeForge: The following sections were auto-appended. Move them to the correct position per the 21-section blueprint. -->

## Features / Capabilities

<!-- TODO: Add a ## Features section listing 3-5 key capabilities with bold labels and concrete descriptions. Include design choices like 'zero dependencies' or 'dry-run by default'. -->


## Requirements

- Python 3.8+
- Windows 10/11
- Third-party: bs4, requests


## Quick Start

<!-- TODO: Add a ## Quick Start section with: 1) cd to project dir, 2) install command if needed, 3) first run command with --help or --dry-run. Use fenced code blocks. -->


## Usage

<!-- TODO: Add a ## Usage section with 2-3 real command examples in fenced code blocks. Show the most common use case first, then advanced options. -->


## Configuration

<!-- TODO: Add a ## Configuration section with a table of env vars, config file paths, or settings with their defaults. -->


## Input / Output

<!-- TODO: Add a ## Input / Output section describing: what files/formats the tool expects, and what files it creates with their locations. -->


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


## Troubleshooting / FAQ

<!-- TODO: Add a ## Troubleshooting section with Problem/Fix pairs for the most common errors. Include known limitations. -->


## Versioning / Roadmap

<!-- TODO: Add a ## Versioning section with the current version number and a roadmap of planned features. -->


## License & Contact

<!-- TODO: Add a ## License & Contact section with the license name and maintainer contact info. -->
