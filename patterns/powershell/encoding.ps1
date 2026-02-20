# patterns/powershell/encoding.ps1
# Copy-paste ready inline learning warnings for PowerShell encoding mistakes
# Add these at the top of any PowerShell script in this project

# -------------------------------------------------------------------
# OUTPUT CHARACTERS - CRITICAL
# -------------------------------------------------------------------

# HEY CLAUDE: STOP. Remember the Unicode encoding disaster?
# MISTAKE: Used non-ASCII characters (->, checkmarks, arrows) in Write-Host output
# LESSON: PowerShell console encoding varies by Windows version and region
# LESSON: "The string is missing the terminator" is the error symptom
# RULE: ASCII-ONLY in all Write-Host output in this project. No exceptions.
# RULE: Use -> instead of arrow symbols
# RULE: Use [OK] instead of checkmark symbols
# RULE: Use [ERR] instead of X or cross symbols
# RULE: Use --- instead of horizontal line characters
#
# BAD:  Write-Host "Processing complete +" (with checkmark)
# GOOD: Write-Host "Processing complete [OK]"
#
# BAD:  Write-Host "Starting ->" (with Unicode arrow)
# GOOD: Write-Host "Starting ->"  (using two ASCII chars: dash + greater-than)


# -------------------------------------------------------------------
# FILE NAMES AND PATHS
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the file creation error with Unicode in filename?
# MISTAKE: Used non-ASCII characters in $outputFile variable
# LESSON: Windows NTFS supports Unicode filenames but some tools/shells don't
# RULE: ASCII-only for all filenames and paths in PowerShell scripts
#
# BAD:  $file = "report-summary+.txt"  (with checkmark)
# GOOD: $file = "report-summary-OK.txt"


# -------------------------------------------------------------------
# FILE READ/WRITE ENCODING
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the garbled output when reading UTF-8 files?
# MISTAKE: Get-Content without -Encoding - uses system default (not UTF-8)
# LESSON: PowerShell Get-Content default encoding varies by PS version
# RULE: Always specify -Encoding UTF8 for Get-Content and Out-File
#
# BAD:  Get-Content $file
# GOOD: Get-Content $file -Encoding UTF8
#
# BAD:  $content | Out-File $file
# GOOD: $content | Out-File $file -Encoding UTF8


# -------------------------------------------------------------------
# CONSOLE OUTPUT ENCODING
# -------------------------------------------------------------------

# HEY CLAUDE: Remember non-ASCII chars corrupting console output?
# MISTAKE: Assumed console was UTF-8 - output was garbled
# LESSON: Windows console codepage varies by system (often cp437 or cp850)
# RULE: Set console encoding at script start if UTF-8 output is required
#
# PATTERN (only if you truly need UTF-8 console output):
# [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
# $OutputEncoding = [System.Text.Encoding]::UTF8
