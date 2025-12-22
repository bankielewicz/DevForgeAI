"""
Test Fixture: Eval/Exec Safe Patterns (Python)

This file contains SAFE alternatives to eval/exec that should NOT trigger false positives
for SEC-004 rule.

Expected detections: 0 violations (no false positives)
Rule ID: SEC-004
Severity: CRITICAL
"""

import ast
import operator
from typing import Any, Dict


# Safe Pattern 1: ast.literal_eval for safe evaluation
def parse_user_data_safe(data_string: str) -> Any:
    """SAFE: ast.literal_eval only allows literals"""

    # SAFE - ast.literal_eval cannot execute code
    data = ast.literal_eval(data_string)

    return data


# Safe Pattern 2: Explicit operator mapping
OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def calculate_safe(left: float, op: str, right: float) -> float:
    """SAFE: Explicit operator whitelist"""

    # SAFE - operator mapping instead of eval()
    if op not in OPERATORS:
        raise ValueError(f"Unsupported operator: {op}")

    return OPERATORS[op](left, right)


# Safe Pattern 3: Expression parser (safe subset)
class SafeCalculator:
    """SAFE: Limited expression parser"""

    def __init__(self):
        self.allowed_operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }

    def evaluate(self, expression: str) -> float:
        """SAFE: Parse and validate AST before evaluation"""

        # SAFE - parse to AST and validate
        tree = ast.parse(expression, mode='eval')

        # Validate: only allow numbers and basic operators
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.Num, ast.Constant)):
                if not isinstance(node, tuple(self.allowed_operations.keys())):
                    raise ValueError(f"Forbidden operation: {type(node).__name__}")

        # SAFE - controlled evaluation
        return self._eval_node(tree.body)

    def _eval_node(self, node: ast.AST) -> float:
        """Recursively evaluate AST node"""
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_func = self.allowed_operations[type(node.op)]
            return op_func(left, right)
        else:
            raise ValueError(f"Unsupported node: {type(node).__name__}")


# Safe Pattern 4: Configuration parsing
def load_config_safe(config_string: str) -> Dict:
    """SAFE: JSON/YAML parsing instead of eval()"""
    import json

    # SAFE - JSON parsing (no code execution)
    config = json.loads(config_string)

    return config


# Safe Pattern 5: Template substitution
def format_template_safe(template: str, values: Dict) -> str:
    """SAFE: String formatting instead of eval()"""

    # SAFE - str.format() for substitution
    result = template.format(**values)

    return result


# Safe Pattern 6: Domain-specific language (DSL)
class QueryBuilder:
    """SAFE: DSL for query construction"""

    def __init__(self):
        self.filters = []

    def where(self, field: str, operator: str, value: Any):
        """SAFE: Structured query API"""

        # SAFE - no string evaluation, structured API
        allowed_operators = {'=', '>', '<', '>=', '<=', '!='}
        if operator not in allowed_operators:
            raise ValueError(f"Invalid operator: {operator}")

        self.filters.append((field, operator, value))
        return self

    def build(self) -> str:
        """SAFE: Build query from structured data"""

        # SAFE - constructs query from validated components
        conditions = [f"{field} {op} ?" for field, op, _ in self.filters]
        return " AND ".join(conditions)
