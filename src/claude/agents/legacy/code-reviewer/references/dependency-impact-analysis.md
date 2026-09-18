# Dependency Impact Analysis for Code Reviewer

**Version**: 1.0 | **Status**: Reference | **Agent**: code-reviewer

---

## Purpose

Validate that modified functions do not break upstream callers using Treelint dependency queries.

## Workflow for Modified Functions

### 1. Identify Modified Functions

```
Bash(command="git diff --name-only")
```

### 2. Query Callers for Each Modified Function

```
Bash(command="treelint deps --calls --symbol {modifiedFunction} --format json", timeout=5000)
```

### 3. Validate Caller Compatibility

- Check if function signature changed
- Check if return type changed
- Check if behavior changed in breaking way
- Flag callers that may need updates

### 4. Flag Potentially Broken Call Sites

- If signature changed: All callers need review
- If return type changed: All callers using return value need review
- If behavior changed: Callers depending on old behavior need review

## Report Format

```markdown
## Dependency Impact

### Modified Function: `{function_name}`
**Callers ({count}):**
- `{caller_name}` at `{file}:{line}` - [REVIEW NEEDED | OK]

**Callees ({count}):**
- `{callee_name}` at `{file}:{line}`

**Compatibility Assessment:** [BREAKING | NON-BREAKING | NEEDS REVIEW]
```

## Fallback

Use Grep for unsupported languages or when Treelint unavailable:
```
Grep(pattern="function_name\\(", glob="**/*.{py,ts,js}")
```
