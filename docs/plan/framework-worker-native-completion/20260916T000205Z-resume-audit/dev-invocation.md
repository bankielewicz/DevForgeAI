# Resolved development and retest selection

This is a manual next-assignment prompt. It has not been dispatched. The current host catalog exposes `dev` and `qa`; operational skill files are read-only inputs. Existing QA remains STOPPED/FAIL. This supplemental handoff does not modify the frozen candidate, reopen the stopped test campaign or establish authorization by itself.

```text
Use $dev for a new, bounded remediation assignment for QA-F-COV-01, followed by a separately run independent $qa retest of the new frozen candidate.

Workspace: C:\Projects\DevForgeAI, native Windows x64, PowerShell, local Windows filesystem. Candidate: C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe. Do not relocate it or substitute WSL/Linux evidence.

Read applicable AGENTS.md and these exact selected contracts:
- C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md
- C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-native-readiness-v1.md
- C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-preflight-v1.md
Their hashes and companion architecture/schema inputs are bound by C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260915T2306060954875Z\inputs-manifest.json (SHA-256 3fafe784e180b37cabaf8e276c8f324ea464fd568dcfa9a05688a55db9e88288).

Read the independent QA report:
C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z\qa-report.md
SHA-256 0cea59ae0461aec0530ee144d8bae340dba7208bec9ad03c97bb8cd1802d1095

Read the original fix handoff:
C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z\dev-handoff.md
SHA-256 fbb6926a4b3a67433f06a7c12e48a24a013249402c2cc7e1b868eb3e2c4c075c

Read the complete supplemental fix packet:
C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T000205Z-resume-audit\qa-fix.md
Its verified hash is entry qa_fix in C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T000205Z-resume-audit\handoff-manifest.json. That external manifest also binds this invocation and the original QA report.

Failed candidate manifest:
C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260915T2306060954875Z\candidate-manifest.json
SHA-256 809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd (48 files).
Before editing, verify current candidate and handoff identities. Report material drift; do not restore old source over someone else's changes.

Selected finding: QA-F-COV-01, mandatory executed-line coverage failure, 2,852/3,103 = 91.91105381888495004834031582%. No functional root cause is established merely by coverage counts. Inspect the bound raw report and unexecuted behavior, especially effective-profile validation, source inventory and runner/protocol orchestration. Add meaningful contract-derived tests with independent expected results. If a product defect is reproduced, retain valid Red, implement the minimum correction, then Green/refactor/QA. Do not fabricate a failing behavioral test for an existing correct path merely to label the work TDD.

Preserve all existing source expectations, tests, specifications, fixtures, operational copies, raw coverage, historical attempts and original FAIL evidence. Do not weaken assertions, lower thresholds, duplicate passing cases, copy product logic into an oracle or exclude uncovered first-party executable code. No automatic rerun may erase an observed failure.

Use fresh timestamped development evidence under C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion. Declare required-case/source denominators before measurement, retain exact bounded commands/cwd/tool versions/exit codes/durations and raw stdout/stderr. Preserve original WF-01..20 with every subfixture, F-01/F-02, all native-readiness offline behavior and all new checks. Run discovered locked/offline Rust regression, formatting, Clippy and complete first-party executed-line coverage. Both coverage and required-case rate must reach at least 95%, with no waived mandatory failures. Follow any new terminal QA stop.

Return a corrected candidate manifest, specification bindings, changed-file manifest, meaningful test mappings, all retained attempts, raw coverage JSON/profiles, and a resolution map marking QA-F-COV-01 FIX_REPORTED only if supported. Development must not self-close the independent finding.

Freeze the returned bytes. The separate independent QA retest must verify identity and test integrity, repeat the invalidated full coverage measurement and affected regression/negative cases, retain new evidence in a distinct timestamped directory under C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa, and issue its own verdict. Only that retest may mark the finding VERIFIED_FIXED.

This assignment does not authorize operational cache/configuration/credential/startup changes, installation, deployment, authority implementation/provisioning, or a source-inventory exception. Native trial selection remains the existing WN-01/WN-02, Codex 0.154.0, gpt-6-astra/high, one attempt each; their quality/source/profile prerequisites remain in force. Preserve zero consumed attempts until prerequisites are met. Framework acceptance remains NOT_EVALUATED unless a separately qualified protected compiled-Rust authority actually issues a decision.
```

The stopped QA campaign cannot start this next assignment automatically. The selected [qa skill](../../../../.agents/skills/qa/SKILL.md) says: “Never promote earlier planning-only intent into execution or automatically invoke dev or another QA session.” Its [restart contract](../../../../.agents/skills/qa/references/reporting-handoff.md) specifies: “No automatic repair/retest loop.” The user's [QA instructions](../../../prompt/qa.md) also require a separate remediation assignment. Existing native selections remain intact; they do not authorize bypassing the metric stop or changing operational sources.
