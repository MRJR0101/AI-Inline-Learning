# AI Inline Learning - PowerShell starter template
# Copy this file to start a new PowerShell project with inline learning pre-configured

# HEY CLAUDE: Read all inline comments before writing any code in this script.
# RULE: When you make a mistake, document it here at the exact line it happened.

# HEY CLAUDE: STOP. Remember the Unicode encoding disaster?
# MISTAKE: Used characters like ->, checkmarks, arrows in output on 2024-12-26
# LESSON: PowerShell console encoding is not always UTF-8 on Windows systems
# LESSON: "The string is missing the terminator" is the symptom
# RULE: ASCII-ONLY in all Write-Host output and all file/folder names
# RULE: Use -> instead of arrows, [OK] instead of checkmarks, [ERR] for errors
# CONTEXT: This project runs on Windows 11 - enforce ASCII always

param(
    [string]$InputPath = "",
    [string]$OutputPath = "output.txt"
)

# HEY CLAUDE: Remember the missing error handling in scripts?
# MISTAKE: Script continued after errors, producing corrupted output silently
# LESSON: PowerShell does not stop on errors by default
# RULE: Always set $ErrorActionPreference = 'Stop' at the top of scripts
$ErrorActionPreference = 'Stop'

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    # HEY CLAUDE: Remember the timestamp format that broke on some locales?
    # MISTAKE: Used Get-Date with format strings that vary by system locale
    # RULE: Always use ISO format: Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Write-Host "[$ts] [$Level] $Message"
}

function Main {
    Write-Log "Starting..."

    try {
        # YOUR CODE HERE

        Write-Log "Complete. [OK]"

    } catch {
        Write-Log "Error: $($_.Exception.Message)" "ERR"
        exit 1
    }
}

Main
