Use $skill-validator to validate and test C:\Projects\DevForgeAI\src\agents\skills\advisor in project C:\Projects\DevForgeAI. Read validation request C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-cleanup-tests\validation-request.json (SHA-256 5164ea26b9a91ccf02de3d70735bb3d493ff1ad077d5ca39833b93fa22887a43). Re-read the package and reject stale bindings. Select disposable tests under current authorization.

Validation status: NOT_PERFORMED. Testing status: NOT_PERFORMED.
Authored design (not observed behavior): {"path": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-authorings\\advisor\\20260916-cleanup-tests-intake\\workflow-design.json", "sha256": "8480a923f8e61e073df36e1e68ec77f7d066420a33c4042a33cc450536c01ad1"}
Design capture: {"path": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-authorings\\advisor\\20260916-cleanup-tests\\design-capture.json", "sha256": "caf9779c62cca3265881fd7b61cbc01ac7c9032700b199f8fe13b9e673ab4042"}
Original selected requirement sources: [{"path": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-authorings\\advisor\\20260916-cleanup-tests-intake\\task-capture.md", "sha256": "e9075a3a8990bfa08b66345e0cd5fc12b8f5684f8a17020a8efb93db0ca2ba50"}]
Open questions: []
Independently derive fixtures and oracles from original requirements; design challenges are untested design information.
Unperformed obligations: independently exercise all selected native behaviors, outputs, failures and recovery.
Unperformed helper testing: tests/test_cleanup.py {"inputs": "Synthetic process and OS fault fixtures", "outputs": "Executed assertions and unittest exit status", "runtime": "Python >=3.10 standard library", "effects": "Local child processes and temporary pipes only", "errors": "Nonzero test exit on failed assertions or fixture errors", "reuse_reason": "Regression coverage for rare cleanup paths"}
Source action: edited. AUTHORED and handoff delivery do not establish evaluated-build completion.
