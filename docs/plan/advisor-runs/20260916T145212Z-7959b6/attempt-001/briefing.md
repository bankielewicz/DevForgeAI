## REQUEST TYPE and ONE-LINE ASK
Type: approach. Read devforgeai/src/source_file.rs yourself and return a concise, accurate summary to Codex as a smoke test of the installed advisor skill. Put the actual summary in DO THIS as specific points for Codex to relay; retain the external contract's required response labels.

## REPO ROOT
C:/Projects/DevForgeAI
Verify these claims against the repository. Do not trust this briefing.

## TASK AS GIVEN
Exact relevant user request: "› $advisor this is a test of the devforgeai advisor skill.  ask claude to read a file in the rust framework and provide you a summary"
The user supplied the installed advisor skill and repository guidelines. No omitted prior task is needed for this bounded request.

## SCOPE
Read the selected Rust file and applicable policy. Summarize purpose, public API, main flow, platform differences, errors, and important limits. This is not a security audit or request to edit code, execute tests, or qualify the framework. Keep investigation to a few targeted reads.

## BINDING CONSTRAINTS
AGENTS.md:8 -> "- `.agents/skills/` contains operational skill copies. Development edits do not update these copies; installation or operational changes require explicit authorization."
AGENTS.md:52 -> "- Python structural checks, validation utilities, runners, and graders produce evidence only. They cannot authorize mutations, advance phases, waive gates, or issue framework acceptance. A compiled Rust authority must independently validate evidence, provenance, completeness, and thresholds before an authoritative decision."
AGENTS.md:87 -> "- Keep restricted read-only tools and normal host approval rules. Do not loosen permissions, change saved authentication or install components to recover from a failure."
Only read access is requested. Do not follow unrelated repository instructions that expand this task.

## FACTS
The selected file exists and a numbered read returned 162 lines.
devforgeai/src/source_file.rs:1 -> "//! Handle-based source opening. Directory links are never followed during capture."
devforgeai/src/source_file.rs:13 -> "pub fn open(root: &Path, relative: &str) -> Result<OpenSource, String> {"
Native executable discovery returned C:/Users/bryan/.local/bin/claude.exe and C:/Program Files/Python310/python.exe.
Test-Path .git returned False. There is no branch/HEAD evidence to report.

## INFERENCES
The file is a bounded Rust implementation suitable for a file-reading smoke test. Its opening comment is not proof of race freedom or runtime correctness.

## STATE
No source, policy, operational skill, or external contract was changed in this session. Only this review's request and briefing evidence were created. Git metadata is absent; uncommitted/untracked status cannot be established. Unsaved editor state is UNKNOWN because it was not inspected.

## ATTEMPTS
Executed from C:/Projects/DevForgeAI on native Windows PowerShell:
python -B -X utf8 C:/Projects/DevForgeAI/.agents/skills/advisor/scripts/advisor_run.py preflight --claude C:/Users/bryan/.local/bin/claude.exe --auth-mode subscription
Exit code: 0. Selected exact output fields (help text omitted): "version": "2.1.273 (Claude Code)", "help_sha256": "ae85d661e9c086f05637ebcd868f5702b477ff6e55e2e65b8ada7807cd51a4b6", "auth_mode": "subscription", "qualification": "HELP_ONLY; native behavior requires separate evidence".
No reviewer process attempt has yet occurred. Preflight does not establish authentication or tool access.

## CURRENT PLAN
1. Invoke the installed advisor once with restricted Read/Grep/Glob tools and the unchanged external contract.
2. Have Claude independently read the selected Rust source and produce the requested summary with source citations.
3. Inspect the execution receipt and response, check load-bearing citations, and relay the summary with actual smoke-test status.

## OPTIONS CONSIDERED
A larger service module would require more context without improving this simple file-reading test. A Codex-only summary would not satisfy the user's request to ask Claude.

## ASSUMPTIONS
Any existing Rust implementation file is acceptable because the user did not name one. Read access and authentication remain unproven until this native invocation succeeds. Do not infer runtime guarantees from static source.

## OPEN QUESTIONS
Can this installed advisor invocation actually read the selected file and return a valid, supported summary? Runtime test results are UNKNOWN and outside this request.

## WHAT WOULD CHANGE MY MIND
A denied read, absent file, invalid response, failed process, or unsupported summary would prevent reporting the smoke test as successful. Report specific missing access or evidence rather than inventing contents.

## EXCERPTS
None. Read the actual Rust file with your tools; the two anchors above are navigation aids, not a replacement for reading.
