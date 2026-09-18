# Observation Extractor - Security Considerations

**Sensitive field filtering:** Observations MUST NOT capture values from fields containing:
- `password`
- `secret`
- `token`
- `key`
- `credential`

When encountering these fields, skip them entirely in observation notes.

**Note content sanitization:** Before storing observation notes:
1. Escape JSON control characters (`\n`, `\t`, `\"`, `\\`)
2. Remove or escape HTML entities (`<`, `>`, `&`)
3. Apply 200-character truncation AFTER sanitization
