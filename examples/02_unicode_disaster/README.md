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
