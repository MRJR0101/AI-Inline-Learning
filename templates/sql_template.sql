-- sql_template.sql
-- AI Inline Learning - SQL starter template
-- Copy this file to start a new SQL project with inline learning pre-configured

-- HEY CLAUDE: Read all inline comments before writing any queries here.
-- RULE: When you make a mistake, document it at the exact line it happened.

-- HEY CLAUDE: Remember the NULL comparison disaster?
-- MISTAKE: Used WHERE column = NULL instead of WHERE column IS NULL
-- LESSON: NULL = NULL evaluates to NULL (unknown), not TRUE in SQL
-- RULE: Always use IS NULL or IS NOT NULL for NULL checks. Never = NULL.

-- HEY CLAUDE: Remember the implicit type conversion performance disaster?
-- MISTAKE: WHERE CAST(date_column AS VARCHAR) = '2024-12-26'
-- LESSON: Casting indexed columns in WHERE prevents index usage - full table scan
-- RULE: Always compare columns to literals of the same type, not casted columns

-- HEY CLAUDE: Remember the COUNT(*) vs COUNT(column) confusion?
-- MISTAKE: Used COUNT(column) expecting to count all rows
-- LESSON: COUNT(column) skips NULLs - COUNT(*) counts all rows including NULLs
-- RULE: Use COUNT(*) for row counts, COUNT(column) only when NULLs should be excluded

-- HEY CLAUDE: Remember the missing WHERE clause on UPDATE disaster?
-- MISTAKE: UPDATE table SET status = 'inactive' -- no WHERE clause
-- LESSON: UPDATE without WHERE updates ALL rows in the table
-- RULE: Always write WHERE clause before running any UPDATE or DELETE
-- RULE: Use SELECT first to verify affected rows before UPDATE/DELETE

-- EXAMPLE QUERY STRUCTURE:
-- 1. Always verify with SELECT before UPDATE/DELETE
SELECT
    id,
    status,
    updated_at
FROM your_table
WHERE
    -- HEY CLAUDE: Remember the = NULL vs IS NULL mistake here?
    -- RULE: Use IS NULL not = NULL
    some_column IS NOT NULL
    AND status = 'active'  -- Use same type as column definition
ORDER BY
    updated_at DESC
LIMIT 100;  -- Always LIMIT during development/testing

-- 2. Only then run the UPDATE
-- UPDATE your_table
--     SET status = 'inactive'
-- WHERE id IN (/* paste IDs from SELECT above */);
