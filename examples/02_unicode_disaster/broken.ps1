# PowerShell script that fails due to Unicode characters
# This is the BEFORE version that AI kept making

Write-Host "Starting file processing →"
Write-Host "Step 1: Loading data ✓"
Write-Host "Step 2: Processing files ✓"
Write-Host "Step 3: Generating report →"

# Create output file
$outputFile = "report→summary✓.txt"
"Processing complete" | Out-File $outputFile

Write-Host "All tasks complete ✓"

# ERROR: Script fails with encoding issues on many Windows systems
# The → and ✓ characters cause "missing terminator" errors
# AI made this mistake repeatedly until inline learning was added
