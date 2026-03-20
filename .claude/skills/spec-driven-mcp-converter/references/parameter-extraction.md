# Parameter Extraction for /convert-mcp

**Purpose:** Define the algorithm for extracting conversion parameters from the conversation context when the `/convert-mcp` command is invoked.

---

## Required Parameters

| Parameter | Extraction Source | Required | Default |
|-----------|------------------|----------|---------|
| `$MCP_SOURCE` | First argument after `/convert-mcp` | **Yes** | HALT if missing |
| `$SOURCE_TYPE` | `--source` flag or inferred from `$MCP_SOURCE` | No | Inferred |
| `$PATTERN_OVERRIDE` | `--pattern` flag | No | null (auto-detect) |
| `$ADAPTER_SCRIPT` | `--adapter-script` flag | No | null |
| `$OUTPUT_DIR` | `--output-dir` flag | No | `./<mcp-name>-cli` |

---

## Extraction Algorithm

### Step 1: Extract MCP Source

```
Scan conversation for pattern: /convert-mcp <value>
Extract first non-flag argument as $MCP_SOURCE

IF $MCP_SOURCE is empty:
  HALT: AskUserQuestion "Which MCP server do you want to convert?"
```

### Step 2: Infer Source Type

```
IF --source flag present:
  $SOURCE_TYPE = flag value

ELSE infer from $MCP_SOURCE:
  IF starts with "npm:" → "npm_package"
  IF ends with ".json" → "json_schema"
  IF is a directory path → "local_directory"
  ELSE → "local_directory" (default)
```

### Step 3: Extract Optional Flags

```
IF --pattern flag present:
  Validate value ∈ {"api-wrapper", "state-based", "custom"}
  $PATTERN_OVERRIDE = value

IF --adapter-script flag present:
  $ADAPTER_SCRIPT = path value

IF --output-dir flag present:
  $OUTPUT_DIR = path value
ELSE:
  $OUTPUT_DIR = "./" + basename($MCP_SOURCE) + "-cli"
```

### Step 4: Generate Conversion ID

```
$CONVERT_ID = "CONVERT-" + strftime("%Y%m%d-%H%M%S")
```

---

## Validation Rules

1. `$MCP_SOURCE` must be non-empty
2. `$PATTERN_OVERRIDE` must be one of: api-wrapper, state-based, custom (or null)
3. `$ADAPTER_SCRIPT` must be a valid file path if provided
4. `$OUTPUT_DIR` parent directory must exist or be creatable

---

## Context Markers

After extraction, these markers are available for all subsequent phases:

| Marker | Example Value |
|--------|---------------|
| `$CONVERT_ID` | `CONVERT-20260319-143000` |
| `$MCP_SOURCE` | `puppeteer-mcp` or `./my-mcp` or `npm:mcp-weather@latest` |
| `$SOURCE_TYPE` | `npm_package`, `local_directory`, `json_schema` |
| `$PATTERN_OVERRIDE` | `state-based` or null |
| `$ADAPTER_SCRIPT` | `./my_adapter.py` or null |
| `$OUTPUT_DIR` | `./puppeteer-mcp-cli` |

---

## Example Invocations

### Minimal
```
/convert-mcp puppeteer-mcp
→ MCP_SOURCE="puppeteer-mcp", SOURCE_TYPE="local_directory", OUTPUT_DIR="./puppeteer-mcp-cli"
```

### With npm source
```
/convert-mcp weather --source npm:mcp-weather@latest
→ MCP_SOURCE="weather", SOURCE_TYPE="npm_package", OUTPUT_DIR="./weather-cli"
```

### Full flags
```
/convert-mcp myservice --source ./my-mcp --pattern custom --adapter-script ./adapter.py --output-dir ./output
→ All parameters explicitly set
```
