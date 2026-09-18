Use $skill-validator to validate and test C:\Projects\DevForgeAI\src\agents\skills\advisor in project C:\Projects\DevForgeAI. Read validation request C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-api-retry-progress-02\validation-request.json (SHA-256 1b7b2f9e227d317be935b9d7622c1ea28c9460fac5e3302b7306085dc2f75277). Re-read the package and reject stale bindings. Select disposable tests under current authorization.

Validation status: NOT_PERFORMED. Testing status: NOT_PERFORMED.
Authored design (not observed behavior): {"path": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-authorings\\advisor\\20260916-api-retry-progress-intake\\workflow-design.json", "sha256": "39ace305ece45197183656addd12c659a975021dbbbe7a9e34aa5a03f8db3759"}
Design capture: {"path": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-authorings\\advisor\\20260916-api-retry-progress-02\\design-capture.json", "sha256": "c05c29e4977bf4820a7028a49bb713e40d42b1bd13ecfa171ce4c6229c861d1f"}
Original selected requirement sources: [{"path": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-authorings\\advisor\\20260916-api-retry-progress-intake\\task-capture.md", "sha256": "8dd22c94c8f806cd9424a5101ebb1cffea5c2b035d6445b4830696cb44d333c0"}]
Open questions: []
Independently derive fixtures and oracles from original requirements; design challenges are untested design information.
Unperformed obligations: independently exercise all selected native behaviors, outputs, failures and recovery.
Unperformed helper testing: scripts/advisor_stream.py {"inputs": "Parsed JSONL events", "outputs": "Numeric retry progress and unchanged raw evidence", "runtime": "Python >=3.10 standard library", "effects": "Write existing progress sink", "errors": "Suppress invalid metadata without changing execution outcome", "reuse_reason": "Expose retries for every streaming invocation"}
Source action: edited. AUTHORED and handoff delivery do not establish evaluated-build completion.
