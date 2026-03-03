"""
Treelint token measurement for STORY-353 A/B testing.

Measures token consumption when using Treelint for AST-aware code search.
"""
import json
import subprocess
from typing import Optional, Dict, Any
from measure_tokens import estimate_tokens


def measure_tokens(text: str) -> int:
    """
    Measure token count for text (delegates to shared utility).

    Args:
        text: Text to measure

    Returns:
        Estimated token count
    """
    return estimate_tokens(text)


def parse_treelint_json(json_str: str) -> Dict[str, Any]:
    """
    Parse Treelint JSON output.

    Args:
        json_str: JSON string from Treelint --format json

    Returns:
        Parsed JSON as dictionary
    """
    if not json_str:
        return {}

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}


def run_treelint_query(query: str, query_type: str = "function",
                        directory: str = ".") -> str:
    """
    Execute a Treelint query with JSON format output.

    Args:
        query: Symbol name to search
        query_type: Type of symbol (function, class, method, etc.)
        directory: Directory to search in

    Returns:
        Treelint JSON output as string
    """
    cmd = ["treelint", "search", query, "--type", query_type,
           "--format", "json", directory]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "{}"
    except FileNotFoundError:
        # Treelint not installed - return empty JSON
        return "{}"
    except Exception:
        return "{}"


def measure_treelint_query(query: str, query_type: str = "function",
                           directory: str = ".") -> dict:
    """
    Run treelint query and measure tokens.

    Args:
        query: Symbol to search
        query_type: Type of symbol
        directory: Directory to search

    Returns:
        Dict with output and token count
    """
    output = run_treelint_query(query, query_type, directory)
    tokens = measure_tokens(output)
    parsed = parse_treelint_json(output)

    return {
        "query": query,
        "type": query_type,
        "output": output,
        "tokens": tokens,
        "parsed": parsed,
        "results_count": len(parsed.get("results", []))
    }
