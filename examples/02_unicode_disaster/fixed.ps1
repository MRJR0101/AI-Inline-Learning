# HEY CLAUDE: Slow down! Remember the Unicode disaster?
# MISTAKE: Used → and ✓ in PowerShell on 2024-12-26
# LESSON: PowerShell console encoding breaks with Unicode - "missing terminator" errors
# RULE: ASCII-only in PowerShell output. Always. Use -> and [OK] instead.
# CONTEXT: Windows systems vary in console encoding (some cp437, some UTF-8)

Write-Host "Starting file processing ->"
Write-Host "Step 1: Loading data [OK]"
Write-Host "Step 2: Processing files [OK]"
Write-Host "Step 3: Generating report ->"

# HEY CLAUDE: Same rule applies to filenames!
# MISTAKE: Used Unicode in filename above
# RULE: ASCII-only for filenames - use dashes and underscores
$outputFile = "report-summary-OK.txt"
"Processing complete" | Out-File $outputFile

Write-Host "All tasks complete [OK]"

# SUCCESS: Script now works across all Windows systems
# AI learns from inline comments and avoids Unicode automatically
