# CLI Generation Templates

**Purpose:** Templates and patterns for generating CLI wrapper code from MCP analysis results.

---

## Directory Structure Template

```
${OUTPUT_DIR}/
├── cli.py                    # Main entry point (argparse)
├── adapters/
│   ├── __init__.py
│   └── <pattern>_adapter.py  # Pattern-specific adapter
├── utils/
│   ├── __init__.py
│   ├── error_handler.py      # Exit code mapping
│   └── output_formatter.py   # JSON/text/base64 formatting
├── tests/
│   └── test_cli.py           # Test stubs
├── requirements.txt          # Python dependencies
└── README.md                 # Usage documentation
```

---

## CLI Entry Point Template (cli.py)

### Core Structure

```python
#!/usr/bin/env python3
"""Auto-generated CLI from MCP conversion. Pattern: {pattern}"""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="{mcp_name} CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Tool subparsers generated from MCP tools
    {tool_subparsers}

    # Session subparsers (state-based only)
    {session_subparsers}

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    # Execute via adapter
    adapter = {AdapterClass}()
    result = adapter.execute(args.command, vars(args))
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") == "success" else 1

if __name__ == "__main__":
    sys.exit(main())
```

### Tool Subparser Generation

For each tool in `mcp_definition.json`:

```python
# Tool: {tool_name}
{tool_name}_parser = subparsers.add_parser("{cli_command_name}")
{tool_name}_parser.add_argument("--{param}", required={is_required})
{tool_name}_parser.add_argument("--format", default="json", choices=["json", "text", "base64"])
```

Name mapping: `snake_case` → `kebab-case` (e.g., `get_forecast` → `get-forecast`)

### Session Subparser (State-Based Only)

```python
session_parser = subparsers.add_parser("session")
session_sub = session_parser.add_subparsers(dest="subcommand")
session_sub.add_parser("create").add_argument("--name", default="")
destroy = session_sub.add_parser("destroy")
destroy.add_argument("--session", required=True)
session_sub.add_parser("list")
```

---

## Adapter Templates

### API Wrapper Adapter

```python
class APIWrapperAdapter:
    def execute(self, command, args):
        output_format = args.pop("format", "json")
        args = {k: v for k, v in args.items() if v is not None}
        try:
            result = self._call_tool(command, args)
            return {"status": "success", "command": command, "data": result}
        except Exception as e:
            return {"status": "error", "command": command, "error": str(e), "exit_code": 1}

    def _call_tool(self, tool_name, params):
        raise NotImplementedError(f"Implement _call_tool for: {tool_name}")
```

### State-Based Adapter

Includes SessionManager class with create/destroy/list/get methods.
Session timeout: 1 hour default.
All tool commands require `--session` argument.

### Custom Adapter

Minimal template with `execute()` method for user to implement.

---

## Utility Templates

### Error Handler (utils/error_handler.py)

```python
EXIT_CODES = {
    ValueError: 2,       # Invalid arguments
    TimeoutError: 3,     # Timeout
    ConnectionError: 4,  # Resource unavailable
    PermissionError: 5,  # Auth failed
    RuntimeError: 1,     # General error
}
```

### Output Formatter (utils/output_formatter.py)

Supports three formats:
- `json`: `json.dumps(data, indent=2)`
- `text`: `str(data.get("data", data))`
- `base64`: `base64.b64encode(data).decode("utf-8")`

---

## Test Stub Template

```python
import subprocess
import json

class TestGeneratedCLI:
    def test_cli_help(self):
        result = subprocess.run(["python", "cli.py", "--help"], capture_output=True)
        assert result.returncode == 0

    def test_commands_exist(self):
        # Verify each tool is registered as subparser
        pass
```

---

## Requirements Template

```
# Generated CLI dependencies
# Pattern: {pattern}
```

Add `mcp>=0.1.0` if Python MCP SDK detected.

---

## README Template

```markdown
# {mcp_name} CLI

Auto-generated CLI from MCP server conversion.
Pattern: {PATTERN}

## Installation
pip install -r requirements.txt

## Usage
python cli.py <command> [options] --format json

## Available Commands
{tool_list}
```
