# patterns/python/encoding.py
# Copy-paste ready inline learning warnings for Python encoding mistakes
# Add these to your code at the exact lines where encoding decisions happen

# -------------------------------------------------------------------
# FILE READ - CSV
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the Excel export encoding crash?
# MISTAKE: pd.read_csv() with no encoding crashed on files saved from Excel
# LESSON: Excel on Windows saves CSV as cp1252, not UTF-8
# RULE: Always try UTF-8 first, fallback to latin-1 if UnicodeDecodeError
#
# PATTERN:
# try:
#     df = pd.read_csv(filepath, encoding='utf-8')
# except UnicodeDecodeError:
#     df = pd.read_csv(filepath, encoding='latin-1')


# -------------------------------------------------------------------
# FILE READ - PLAIN TEXT
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the open() crash on non-ASCII text files?
# MISTAKE: open(filepath, 'r') without encoding - crashes on non-ASCII
# LESSON: Python's default encoding is platform-dependent on Windows
# RULE: Always specify encoding='utf-8' on open() for text files
#
# PATTERN:
# with open(filepath, 'r', encoding='utf-8') as f:
#     content = f.read()


# -------------------------------------------------------------------
# FILE WRITE
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the write crash on URLs with non-ASCII characters?
# MISTAKE: open(filepath, 'w') without encoding - crashed writing non-ASCII URLs
# LESSON: Windows default encoding is cp1252 which cannot encode all Unicode
# RULE: Always encoding='utf-8' on file write. No exceptions in this project.
#
# PATTERN:
# with open(filepath, 'w', encoding='utf-8') as f:
#     f.write(content)


# -------------------------------------------------------------------
# DETECT UNKNOWN ENCODING
# -------------------------------------------------------------------

# HEY CLAUDE: Remember processing binary files without detecting encoding first?
# MISTAKE: Assumed UTF-8 on binary content from unknown source - data corruption
# LESSON: Files from web scraping can have any encoding
# RULE: Use chardet to detect encoding before decoding unknown binary content
#
# PATTERN:
# import chardet
# detected = chardet.detect(raw_bytes)
# encoding = detected['encoding'] or 'utf-8'
# text = raw_bytes.decode(encoding, errors='replace')


# -------------------------------------------------------------------
# REQUESTS RESPONSE TEXT
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the garbled text from response.text without encoding?
# MISTAKE: Used response.text without checking response.encoding first
# LESSON: requests guesses encoding from headers - often wrong for non-UTF-8 sites
# RULE: Use response.content + explicit decode, or set response.encoding first
#
# PATTERN:
# response.encoding = 'utf-8'  # or detected encoding
# text = response.text
