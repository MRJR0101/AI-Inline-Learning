-- patterns/sql/performance.sql
-- Copy-paste ready inline learning warnings for SQL performance mistakes
-- Add these at the lines where queries could cause performance issues

-- -------------------------------------------------------------------
-- IMPLICIT TYPE CONVERSION IN WHERE
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the query that ran for 45 minutes on an indexed column?
-- MISTAKE: CAST(date_column AS VARCHAR) = '2024-12-26' in WHERE clause
-- LESSON: Casting an indexed column in WHERE prevents index usage - full table scan
-- RULE: Always compare columns to literals of the same type. Never cast in WHERE.
--
-- BAD:  WHERE CAST(created_at AS DATE) = '2024-12-26'  -- full table scan
-- GOOD: WHERE created_at >= '2024-12-26' AND created_at < '2024-12-27'


-- -------------------------------------------------------------------
-- WILDCARD AT START OF LIKE
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the LIKE query that ignored the index entirely?
-- MISTAKE: WHERE email LIKE '%@gmail.com' - leading wildcard = no index use
-- LESSON: LIKE with leading % forces full table scan even on indexed columns
-- RULE: Avoid leading wildcards. Use full-text search or reverse-string techniques.
--
-- BAD:  WHERE email LIKE '%@gmail.com'     -- full scan
-- BETTER: WHERE email LIKE 'michael%'      -- index can be used
-- BEST:  Use full-text search for suffix matching


-- -------------------------------------------------------------------
-- SELECT * IN PRODUCTION
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the query that fetched 40 columns when we needed 3?
-- MISTAKE: SELECT * FROM large_table WHERE ... in production queries
-- LESSON: SELECT * transfers all columns - unnecessary I/O, slower, fragile to schema changes
-- RULE: Always specify exactly the columns you need. No SELECT * in production queries.
--
-- BAD:  SELECT * FROM users WHERE active = 1
-- GOOD: SELECT id, email, created_at FROM users WHERE active = 1


-- -------------------------------------------------------------------
-- UPDATE/DELETE WITHOUT WHERE
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the missing WHERE clause incident?
-- MISTAKE: UPDATE orders SET status = 'cancelled' -- no WHERE clause
-- LESSON: UPDATE/DELETE without WHERE affects ALL rows in the table
-- RULE: Never run UPDATE or DELETE without a WHERE clause
-- RULE: Always SELECT first to verify the affected rows, then UPDATE/DELETE
-- RULE: Test on a single row with WHERE id = X before running batch updates
--
-- BAD:  UPDATE orders SET status = 'cancelled'   -- UPDATES EVERY ROW
-- GOOD: UPDATE orders SET status = 'cancelled' WHERE id = 12345
-- GOOD: UPDATE orders SET status = 'cancelled' WHERE created_at < '2024-01-01'


-- -------------------------------------------------------------------
-- N+1 QUERY PATTERN
-- -------------------------------------------------------------------

-- HEY CLAUDE: Remember the loop that ran 10,000 individual queries?
-- MISTAKE: Running SELECT inside a loop for each ID in a list
-- LESSON: N+1 queries - one query per record - is catastrophically slow at scale
-- RULE: Use IN clause or JOIN to fetch all needed records in one query
--
-- BAD (in application code):
--   for id in id_list:
--       result = execute("SELECT * FROM orders WHERE id = ?", id)
--
-- GOOD:
--   SELECT * FROM orders WHERE id IN (1, 2, 3, 4, 5)
