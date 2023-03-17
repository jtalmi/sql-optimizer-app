from typing import Callable, Dict, Sequence

from sqlfmt.api import Mode, format_string
from sqlglot import parse_one
from sqlglot.expressions import Select
from sqlglot.optimizer import RULES, optimize

RULE_MAPPING: Dict[str, Callable] = {rule.__name__: rule for rule in RULES}
SAMPLE_QUERY: str = """WITH users AS (
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
"""


def _generate_ast(query: str) -> Select:
    """
    Generate an AST from a query.
    """
    ast = parse_one(query)
    return ast


def apply_optimizations(
    query: str, rules: Sequence[Callable] = RULES, remove_ctes: bool = False
) -> Select:
    """
    Apply optimizations to an AST.
    """
    ast = _generate_ast(query)
    if remove_ctes:
        return optimize(ast, rules=rules)
    else:
        return optimize(ast, rules=rules, leave_tables_isolated=True)


def format_sql_with_sqlfmt(query: str) -> str:
    """
    Format a query using sqlfmt.
    """
    mode = Mode()
    return format_string(query, mode)
