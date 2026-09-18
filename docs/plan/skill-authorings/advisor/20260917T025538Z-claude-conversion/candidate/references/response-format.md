# Response contract and interpretation

Claude receives the external contract directly through `--append-system-prompt-file`. This document defines how the calling agent consumes its output; it is not a second Claude prompt. The configured SHA256 must match before execution and is checked again afterward. A changed contract requires content review and updated compatibility evidence, not an automatic digest refresh.

The runner requests a JSON CLI envelope to distinguish a completed answer from reported budget/error termination. It accepts only an object with `type: result`, `subtype: success`, `is_error: false`, and a string `result`. Optional reported cost must be a finite nonnegative number or null. A nonzero exit, spawn error, or timeout prevents response interpretation. Raw output is always retained after a normal helper return.

Inside `result`, the first nonblank line must be exactly one of:

```text
VERDICT: PROCEED
VERDICT: PROCEED_WITH_CHANGES
VERDICT: STOP_REDIRECT
VERDICT: INSUFFICIENT_CONTEXT
```

Exactly one verdict line is allowed. Its next nonblank line must be `ASK RESTATED:`. Required labels, each on its own line and in this order: `ASK RESTATED:`, `DO THIS:`, `DO NOT:`, `CLAIM AUDIT:`, `RISKS:`, `COULD NOT VERIFY:`, `FLIP CONDITIONS:`. Every section has nonempty content; `none` is allowed for genuinely empty sections. `MISSING:` is required last only for INSUFFICIENT_CONTEXT and must name missing evidence rather than say `none`, including bulleted or numbered forms. The calling agent must still judge whether the named items are actionable.

Invalid examples: bare `VERDICT:`; `VERDICT: APPROVED`; preamble before the verdict; duplicate verdict; omitted DO NOT; a second MISSING section; error envelope containing apparently valid Markdown. A structurally complete invented or prematurely shortened answer can still pass syntax checks: the calling agent must assess completeness and meaning. The helper does not prove semantic completeness.

`all_unverified` is true when CLAIM AUDIT contains no recognized claim statuses or only `UNVERIFIED`. Mixed statuses do not establish adequate investigation. The calling agent must assess whether the confirmed items are load-bearing, whether citations resolve, and whether a contradicted claim invalidates the plan. No source-code read proves a runtime assertion.

Receipt exit codes: helper 0 means preflight completed or response syntax is valid; 1 means a recorded attempt failed or produced invalid output; 2 means input/preflight/history blocked execution. None is an acceptance decision. Reviewer STOP_REDIRECT is valid advice and can produce helper exit 0.
