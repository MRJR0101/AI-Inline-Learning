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
