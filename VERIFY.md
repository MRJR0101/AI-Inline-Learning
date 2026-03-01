# Verification: AI-Inline-Learning

## Purpose

Verify that repository patterns and examples for AI Inline Learning are discoverable and runnable from a clean checkout. The goal is to confirm that inline warning markers, comparison docs, and example pipelines are all accessible through reproducible commands.

This verification does not test an application runtime service. It validates the documentation pattern workflow itself: locate warning markers, run example scripts, and confirm expected educational outputs.

## Prerequisites

- Python 3.8+
- Packages used by examples: `beautifulsoup4`, `pandas`, `requests`
- `rg` (ripgrep) for marker inspection

## Verification Steps

### Step 1: Marker Discovery

Run:

```bash
rg -n "HEY [A-Z]" patterns examples
```

Verify that marker lines are returned from both `patterns/` and `examples/`.

### Step 2: Example Execution

Run:

```bash
python examples/04_data_processing/basic_pipeline.py
python examples/04_data_processing/smart_pipeline.py
```

Verify both scripts execute and produce comparable pipeline output so the improved flow can be reviewed.

### Step 3: Documentation Access

Open and review:

- `docs/COMPARISON.md`
- `README.md`

Verify both files reflect the current approach and command references.

## Expected Output

```text
patterns/python/encoding.py:<line>: # HEY CLAUDE: ...
examples/02_unicode_disaster/fixed.ps1:<line>: # HEY CLAUDE: ...
[INFO] basic pipeline completed
[INFO] smart pipeline completed
```

## Status

- Last Verified: 2026-02-20
- Verified By: Codex Automated Audit
- Result: PENDING MANUAL CONFIRMATION
