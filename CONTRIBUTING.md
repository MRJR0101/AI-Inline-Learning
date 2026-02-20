# Contributing to AI Inline Learning

Thank you for your interest in contributing. This project grows through shared
lessons from real AI coding sessions.

## What We Need Most

**New patterns** - Real mistakes your AI assistant made repeatedly, documented
in the HEY/MISTAKE/LESSON/RULE format.

**New language coverage** - We have Python, PowerShell, JavaScript, and SQL.
Ruby, Go, Rust, Bash, and others are welcome.

**Metrics data** - If you track your own error reduction, share the results.

## How to Contribute a Pattern

### Format

Every inline learning comment follows this structure:

```
# HEY [AI_NAME]: [Attention grabber - make it memorable]
# MISTAKE: [Specific error that occurred, with date if possible]
# LESSON: [Root cause - why did it happen]
# RULE: [Actionable rule - what to do instead]
# CONTEXT: [Optional - when/where this applies in your project]
```

### Requirements

- Must be a real mistake you observed, not a theoretical one
- Must have happened at least twice before you added the warning
- Placed at the exact line where the mistake would occur
- No Unicode characters in comments (ASCII only for portability)
- Include a before/after code example if possible

### File Placement

Add patterns to the appropriate file in `patterns/`:

```
patterns/
  python/
    encoding.py       - File I/O and text encoding
    data_quality.py   - pandas and data handling
    web_scraping.py   - requests, BeautifulSoup, Selenium
  powershell/
    encoding.ps1      - Console and file encoding
  javascript/
    type_coercion.js  - == vs ===, typeof, falsy values
  sql/
    nulls.sql         - NULL handling
    performance.sql   - Query performance
```

If your pattern does not fit an existing file, create a new one.

## Submitting a Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b pattern/python-async-errors`
3. Add your pattern with a clear comment header
4. Update the relevant README if adding a new file
5. Submit a pull request with a description of what mistake it prevents

## Submitting Error Reduction Data

If you track your own sessions, add rows to `metrics/results.csv`:

```
session_date,project,ai_tool,error_type,occurred,description
2024-12-15,MyProject,Claude,your_error_type,True,Description of what happened
2024-12-16,MyProject,Claude,your_error_type,False,Warning prevented recurrence
```

Then open an issue or pull request with your aggregated results.

## Code of Conduct

- Be specific - vague warnings do not help
- Be honest - only submit real observed mistakes
- Be concise - 3-5 lines per warning maximum
- No promotional content, links to paid tools, or spam

## Questions

Open an issue on GitHub or connect on LinkedIn:
linkedin.com/in/michael-rawls-jr
