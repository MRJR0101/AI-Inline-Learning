# Example 2: The Unicode Disaster

## The Problem

AI coding assistants repeatedly used Unicode characters (→ ✓) in PowerShell scripts, causing encoding errors on Windows systems.

## What Went Wrong

```powershell
Write-Host "Processing complete ✓"
$file = "report→summary.txt"
```

**Error:** "The string is missing the terminator: ""

**Root Cause:** Windows console encoding varies (cp437, cp850, UTF-8). Unicode characters like → and ✓ aren't supported in many encodings.

## How AI Inline Learning Solved It

Added explicit warning at decision point:

```powershell
# HEY CLAUDE: Slow down! Remember the Unicode disaster?
# MISTAKE: Used → and ✓ in PowerShell on 2024-12-26
# LESSON: Encoding breaks - "missing terminator" errors
# RULE: ASCII-only in PowerShell. Always. Use -> and [OK] instead.
```

## Results

- **Before:** AI made Unicode mistake in 8 out of 10 PowerShell scripts
- **After:** AI makes Unicode mistake in 0 out of 10 scripts
- **Improvement:** 100% elimination of this specific error

## Files

- `broken.ps1` - Original code that fails
- `fixed.ps1` - Code with inline learning comments

## Real-World Impact

This was a production bug discovered on 2024-12-26. After adding the inline learning comment, Claude (and other AI assistants) stopped making this mistake across all subsequent PowerShell scripts in the project.

**Key Insight:** One comment at the exact failure point prevents hundreds of future errors.

<!-- ReadmeForge: The following sections were auto-appended. Move them to the correct position per the 21-section blueprint. -->

## Features / Capabilities

<!-- TODO: Add a ## Features section listing 3-5 key capabilities with bold labels and concrete descriptions. Include design choices like 'zero dependencies' or 'dry-run by default'. -->


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
