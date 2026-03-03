"""
Grep baseline token measurement for STORY-353 A/B testing.

Measures token consumption when using Grep for code search queries.
"""
import subprocess
from typing import Optional
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


def run_grep_query(pattern: str, directory: str = ".",
                   context_lines: int = 3) -> str:
    """
    Execute a Grep query and return results.

    Args:
        pattern: Regex pattern to search
        directory: Directory to search in
        context_lines: Number of context lines (-C flag)

    Returns:
        Grep output as string
    """
    cmd = ["grep", "-rn", f"-C{context_lines}", pattern, directory]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return ""
    except Exception:
        return ""


def measure_grep_query(pattern: str, directory: str = ".") -> dict:
    """
    Run grep query and measure tokens.

    Args:
        pattern: Search pattern
        directory: Directory to search

    Returns:
        Dict with output and token count
    """
    output = run_grep_query(pattern, directory)
    tokens = measure_tokens(output)

    return {
        "pattern": pattern,
        "output": output,
        "tokens": tokens,
        "lines": len(output.splitlines()) if output else 0
    }
