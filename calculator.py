#calculator py
#NOT MINE

#!/usr/bin/env python3
"""Simple command-line calculator.

Usage:
    python calculator.py "2 + 3 * 4"
    python calculator.py
"""

from __future__ import annotations

import ast
import operator
import sys
from typing import Any


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(expression: str) -> float:
    """Safely evaluate a calculator expression using Python's AST."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc.msg}") from exc

    def _eval(node: ast.AST) -> Any:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
            left = _eval(node.left)
            right = _eval(node.right)
            return _ALLOWED_OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
            operand = _eval(node.operand)
            return _ALLOWED_OPERATORS[type(node.op)](operand)
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    result = _eval(tree.body)
    if isinstance(result, bool):
        raise ValueError("Boolean values are not allowed.")
    return float(result)


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: python calculator.py ["expression"]")
        return 1

    expression = sys.argv[1] if len(sys.argv) == 2 else input("Enter expression: ")

    try:
        result = _safe_eval(expression)
        print(f"Result: {result}")
        return 0
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
