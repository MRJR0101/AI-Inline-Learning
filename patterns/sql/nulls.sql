-- patterns/sql/nulls.sql
-- Copy-paste ready inline learning warnings for SQL NULL handling mistakes
-- Add these as comments at the exact lines where NULL comparisons happen

-- -------------------------------------------------------------------
-- NULL COMPARISON
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the query that silently returned zero rows?
-- MISTAKE: Used WHERE column = NULL instead of WHERE column IS NULL
-- LESSON: NULL = NULL evaluates to NULL (unknown) in SQL - never TRUE
-- LESSON: This returns zero rows and no error - a silent data bug
-- RULE: Always use IS NULL or IS NOT NULL. Never = NULL or != NULL.
--
-- BAD:  WHERE deleted_at = NULL
-- GOOD: WHERE deleted_at IS NULL
--
-- BAD:  WHERE status != NULL
-- GOOD: WHERE status IS NOT NULL


-- -------------------------------------------------------------------
-- COUNT WITH NULLS
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the count discrepancy that confused the stakeholder?
-- MISTAKE: Used COUNT(column) expecting total row count
-- LESSON: COUNT(column) skips NULL values - only COUNT(*) counts all rows
-- RULE: Use COUNT(*) for row counts. Use COUNT(column) only when intentionally
--       excluding NULLs and that intent is clear from context.
--
-- BAD:  SELECT COUNT(email) FROM users  -- misses rows where email IS NULL
-- GOOD: SELECT COUNT(*) FROM users      -- counts all rows
-- GOOD: SELECT COUNT(email) FROM users  -- only if NULL emails should be excluded


-- -------------------------------------------------------------------
-- AGGREGATE WITH NULLS
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the SUM returning NULL for the whole column?
-- MISTAKE: SUM() returned NULL when any value in the column was NULL
-- LESSON: SUM(column) returns NULL if ALL values are NULL
-- LESSON: Arithmetic with NULL always produces NULL
-- RULE: Use COALESCE() to handle NULLs before aggregation when appropriate
--
-- BAD:  SELECT SUM(revenue) FROM orders
-- GOOD: SELECT SUM(COALESCE(revenue, 0)) FROM orders
-- GOOD: SELECT COALESCE(SUM(revenue), 0) FROM orders


-- -------------------------------------------------------------------
-- JOIN WITH NULLS
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the JOIN that dropped valid rows due to NULL keys?
-- MISTAKE: JOIN on a column that had NULL values - NULL never matches NULL
-- LESSON: NULL = NULL is never TRUE in a JOIN condition
-- RULE: Ensure JOIN keys are NOT NULL, or handle with COALESCE in join condition
--
-- BAD:  JOIN other ON t.foreign_key = other.id  -- drops rows where foreign_key IS NULL
-- GOOD: Ensure foreign_key is NOT NULL before joining, or use LEFT JOIN + IS NULL check


-- -------------------------------------------------------------------
-- COALESCE PATTERN
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the NULL propagating through CASE expressions?
-- MISTAKE: CASE WHEN without ELSE returned NULL for unmatched rows
-- LESSON: CASE WHEN with no matching condition and no ELSE returns NULL
-- RULE: Always include ELSE in CASE expressions to make the NULL case explicit
--
-- BAD:
-- CASE WHEN status = 'active' THEN 'Active'
--      WHEN status = 'inactive' THEN 'Inactive'
-- END
--
-- GOOD:
-- CASE WHEN status = 'active' THEN 'Active'
--      WHEN status = 'inactive' THEN 'Inactive'
--      ELSE 'Unknown'  -- explicit - makes NULL case visible
-- END
