---
skill_name: decimal-ledger-spec
status: approved
---
# Decimal ledger specification

Purpose: Build a Codex CLI skill named decimal-ledger-spec that summarizes the amount column of a supplied local CSV.

Activation: Use for requests to total a local CSV's amount column. Do not select it for explanation alone, transaction categorization, network data retrieval, or editing the original CSV.

REQ-01 Inputs: Accept an input CSV path and an output JSON path. Read CSV as UTF-8 with optional BOM and support ordinary quoted CSV fields. Require the amount column. Each row must have a nonempty, finite decimal amount with at most two decimal places. Negative amounts are valid.

REQ-02 Output: Write exactly an object with integer count (number of data rows) and string total (decimal sum formatted with exactly two places), with no extra fields. Empty CSV with the required header yields count 0 and total "0.00". Use decimal arithmetic; do not sum binary floats.

REQ-03 Resource contract: Deliver SKILL.md, scripts/sum_amounts.py, assets/result.schema.json, and references/workers/result-review.md. The helper accepts required --input and --output arguments, exits 0 on success and 2 for invalid input, invalid arguments, or output conflicts, emits success JSON on stdout and diagnostics on stderr, and never overwrites an existing output. Document its actual invocation in SKILL.md. The JSON schema enforces the exact output fields/types and a two-place decimal total string.

REQ-04 Effects and recovery: Preserve input bytes; write only the explicitly selected new output file. No network calls or external packages. Reject missing amounts, NaN, infinity and precision beyond two decimal places. On invalid input or output conflict leave existing output bytes unchanged and report the reason. Do not install this skill or change runtime configuration.

REQ-05 Worker task: The result-review task checks actual produced JSON against the stated fields and verifies that the input digest is unchanged. It returns findings and the inspected input/output paths. It has no assigned write paths. It may be performed sequentially by the main agent; independent identity/isolation is not required. This task contract is advisory work organization and does not supply a framework gate or acceptance decision.

REQ-06 Environment and dependencies: Python 3.10+ standard library only, Windows PowerShell terminal. No desktop, browser, hooks, registry, services, or other skills required by the generated skill's runtime. Frontmatter needs name and description only; no UI metadata or explicit-only invocation policy is requested.
