# patterns/python/data_quality.py
# Copy-paste ready inline learning warnings for pandas data quality mistakes
# Add these at the exact lines where data transformations happen

# -------------------------------------------------------------------
# NULL / NaN HANDLING
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the silent NaN arithmetic disaster?
# MISTAKE: price * quantity = NaN when either column had missing values
# LESSON: pandas NaN arithmetic propagates silently - no error, wrong totals
# RULE: Fill or drop NaN before any arithmetic. Document your business rule.
# CONTEXT: Missing price/quantity = 0 revenue in this project
#
# PATTERN:
# df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
# df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
# df['revenue'] = df['price'] * df['quantity']


# -------------------------------------------------------------------
# COLUMN VALIDATION
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the KeyError crash on different source schemas?
# MISTAKE: Accessed df['date'] directly - crashed when column was named 'Date'
# LESSON: Real CSV files have inconsistent headers from different systems/exports
# RULE: Always validate required columns exist before any column access
#
# PATTERN:
# required = ['date', 'price', 'quantity']
# missing = [c for c in required if c not in df.columns]
# if missing:
#     raise ValueError(f'Missing columns: {missing}. Found: {list(df.columns)}')


# -------------------------------------------------------------------
# DATE PARSING
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the to_datetime crash on international date formats?
# MISTAKE: pd.to_datetime(df['date']) crashed on "27-Dec-2024" format
# LESSON: Date formats vary by country and system - not always ISO 8601
# RULE: Always use errors='coerce' - converts bad dates to NaT not exceptions
# RULE: Log how many NaT values resulted so data quality issues are visible
#
# PATTERN:
# df['date'] = pd.to_datetime(df['date'], errors='coerce')
# bad = df['date'].isna().sum()
# if bad > 0:
#     print(f'Warning: {bad} rows have unparseable dates')


# -------------------------------------------------------------------
# TYPE COERCION
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the string columns breaking sum() and mean()?
# MISTAKE: CSV parser read numeric columns as strings - sum() returned string concat
# LESSON: CSV files sometimes quote numbers, making pandas read them as strings
# RULE: Always convert to numeric explicitly with pd.to_numeric(errors='coerce')
#
# PATTERN:
# df['amount'] = pd.to_numeric(df['amount'], errors='coerce')


# -------------------------------------------------------------------
# DUPLICATE DETECTION
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the inflated row counts from duplicate records?
# MISTAKE: Processed dataframe without checking for duplicates first
# LESSON: Real data sources often contain duplicate records from retries/exports
# RULE: Always check and handle duplicates before aggregation or analysis
#
# PATTERN:
# dupes = df.duplicated(subset=['id']).sum()
# if dupes > 0:
#     print(f'Warning: {dupes} duplicate rows found - dropping')
#     df = df.drop_duplicates(subset=['id'], keep='first')
