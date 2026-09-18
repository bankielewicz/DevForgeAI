# Observation Extractor - Data Validation Rules

1. **Context Parameter:** Must be valid JSON string or object; maximum 500KB payload size
2. **Phase Number:** Must be string value "01" through "09"
3. **Observation ID:** Must match pattern `obs-{phase}-{sequence}` (e.g., `obs-02-001`)
4. **Category Values:** Must be one of: friction, success, pattern, gap, idea, bug, warning
5. **Severity Values:** Must be one of: low, medium, high
6. **Note Length:** Maximum 200 characters; truncate with "..." if exceeded
7. **Files Array:** Each entry must be relative path (no leading `/`, no absolute paths)
