# Result review

Responsibility: Check the actual produced JSON fields and the unchanged input digest (REQ-05, using the output contract from REQ-02 and REQ-03).

Inputs: The original CSV path, its SHA-256 captured before totaling, and the actual output JSON path. Read [the result schema](../../assets/result.schema.json). Missing pre-run digest evidence prevents claiming input preservation.

Output and return format: Return the inspected input and output paths, findings, the observed `count` and `total`, the before and after input SHA-256 values, and whether they match. State any missing or failed observation explicitly.

Check that JSON is an object with exactly `count` and `total`; `count` must be a nonnegative integer and `total` must match the schema's two-place decimal string pattern. Reject extra fields, incorrect types, or malformed JSON. Read the input bytes and compare SHA-256 with the provided original digest. Do not infer preservation from mtime, filenames, or a caller's claim.

Assigned candidate write paths: None. Review does not repair files or modify input/output bytes.

Required tools: Read-only Python standard-library or PowerShell terminal operations to inspect JSON and hash files. No external packages or services.

Independent execution: Optional; sequential review by the main agent is explicitly allowed because separate identity is not essential to this task.

Required isolation: None. This text supplies no process or filesystem isolation.

Failure and incomplete results: Return findings and inspected paths even on schema failure, digest mismatch, or unavailable evidence. Do not report a completed review if a required observation could not be made.

Use the host's available subagent tool if delegating this bounded read-only task. This is advisory work organization, not an installed agent profile, framework gate, or acceptance decision.
