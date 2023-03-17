# SQL Optimizer Streamlit App
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sql-optimizer.streamlit.app)

A web app to optimize and lint SQL queries using [sqlglot](https://github.com/tobymao/sqlglot) and [sqlfmt](http://sqlfmt.com).

## Features
- Optimize SQL queries using various optimization rules from sqlglot
- Lint SQL queries with sqlfmt
- Customizable optimization rules

## Usage
1. Enter your SQL query in the left editor.
2. Select the optimization rules you want to apply.
3. Choose whether to preserve CTEs or combine them and/or lint the query with sqlfmt.
4. Click the "Optimize SQL" button.
5. The optimized and linted SQL query will appear in the right editor.


## Examples
For the given sample query:
```
WITH users AS (
    SELECT *
    FROM users_table),
orders AS (
    SELECT *
    FROM orders_table),
combined AS (
    SELECT users.id, users.name, orders.order_id, orders.total
    FROM users
    JOIN orders ON users.id = orders.user_id)
SELECT combined.id, combined.name, combined.order_id, combined.total
FROM combined
```
Applying all rules except `canonical` will expand the `select *` expressions in the initial CTEs, which has been shown to improve performance on [some data warehouses](https://select.dev/posts/should-you-use-ctes-in-snowflake). Removing the `qualify_tables rule will also yield a cleaner result:
```
WITH users AS (
  SELECT
    users_table.id AS id,
    users_table.name AS name
  FROM users_table
), orders AS (
  SELECT
    orders_table.order_id AS order_id,
    orders_table.total AS total,
    orders_table.user_id AS user_id
  FROM orders_table
)
SELECT
  users.id AS id,
  users.name AS name,
  orders.order_id AS order_id,
  orders.total AS total
FROM users
JOIN orders
  ON users.id = orders.user_id
```


