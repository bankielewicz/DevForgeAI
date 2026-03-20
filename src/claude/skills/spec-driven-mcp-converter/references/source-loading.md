# MCP Source Loading Guide

**Purpose:** Define how to discover, load, and parse MCP server sources across all supported source types.

---

## Supported Source Types

| Type | Identifier | How to Load |
|------|-----------|-------------|
| Local Directory | Path to directory | Scan for tool definitions in source files |
| JSON Schema | Path ending in `.json` | Parse JSON for tool definitions |
| npm Package | Starts with `npm:` | Use `npm view` or `npm pack` to inspect |

---

## Local Directory Loading

### Python MCPs

Scan for `@mcp.tool()` or `@tool()` decorated functions:

```python
# Detection pattern
import re
pattern = r'@.*\.tool\(\s*\)?\s*(?:async\s+)?def\s+(\w+)\s*\((.*?)\)'

# For each .py file in source directory:
for match in re.finditer(pattern, content, re.DOTALL):
    tool_name = match.group(1)
    params = match.group(2)
```

### TypeScript/JavaScript MCPs

Scan for `server.tool()` or `@tool()` definitions:

```
# Look for patterns like:
server.tool("tool_name", "description", { param: z.string() }, handler)
```

### Fallback

If no tools detected via pattern matching:
1. Look for `mcp.json` or `mcp-manifest.json`
2. Look for `tools.json` schema file
3. Look for README with tool documentation
4. HALT if no tools found

---

## JSON Schema Loading

Parse JSON file with expected structure:

```json
{
  "tools": [
    {
      "name": "tool_name",
      "description": "What this tool does",
      "inputs": {
        "param1": {"type": "string", "required": true},
        "param2": {"type": "integer", "default": 5}
      },
      "outputs": "return_type"
    }
  ]
}
```

### Validation

- `tools` array must exist
- Each tool must have `name` field
- `inputs` field defaults to `{}` if missing

---

## npm Package Loading

### Inspect Package

```bash
npm view <package> --json
```

Extract `main`, `types`, or `exports` fields to find entry point.

### Extract Schema

```bash
npx <package> --schema  # If package supports it
# OR
npm pack <package> && tar xzf <package>.tgz && scan package/
```

---

## Normalized Tool Definition

All source types produce a normalized structure:

```json
{
  "name": "tool_name",
  "description": "What this tool does",
  "inputs": {
    "param_name": "type_string"
  },
  "outputs": "return_type",
  "async": true,
  "side_effects": ["browser_state"]
}
```

### Normalization Rules

1. Tool names: snake_case (Python) or camelCase (TS) → preserved as-is for analysis
2. Parameter types: simplified to string representations
3. Async detection: presence of `async def` or `async function`
4. Side effects: inferred from tool body or explicit annotations

---

## Output

Write normalized tools to: `tmp/${CONVERT_ID}/mcp_definition.json`

```json
{
  "source": "$MCP_SOURCE",
  "source_type": "$SOURCE_TYPE",
  "tool_count": 4,
  "tools": [
    { "name": "...", "inputs": {...}, "outputs": "...", "async": true }
  ]
}
```
