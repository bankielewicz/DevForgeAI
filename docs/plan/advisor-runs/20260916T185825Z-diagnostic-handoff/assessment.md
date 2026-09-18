# Advisor assessment: diagnostic QA handoff

Ask: Is the selected handoff ready to guide independent offline QA of the frozen Rust diagnostic candidate, including privacy, rejection checks and a separate native-launch boundary?

The installed [advisor skill](../../../../.agents/skills/advisor/SKILL.md) ran a read-only Claude Opus/high review with subscription-mode child environment handling. Attempt 001 failed with ConnectionRefused before useful review. Attempt 002 used `--reason retry --show-progress`, succeeded with exit 0, produced a VALID response and returned **PROCEED_WITH_CHANGES**. The receipt confirms `stream-json` plus `--verbose`, the helper's progress transport. Both attempts are consumed. Attempt 002 reported USD 0.9861765 against its USD 1.00 cap; configured reservations total USD 2.00. This is reported CLI cost, not an independently verified billing statement.

Evidence: [successful execution receipt](attempt-002/execution.json), [reviewer response](attempt-002/response.md), [first execution receipt](attempt-001/execution.json), [fresh assessment readback](assessment-evidence.json).

## Assessed recommendations

| Recommendation | Assessment and disposition |
| --- | --- |
| Make accounting-query failure a visible gap | Accepted with qualification. `protocol.rs:258` has zero execution in retained coverage; no accounting injection seam was found. Runtime status is NOT_RUN. Record blocked readiness when no authorized feasible method exists; missing required evidence cannot become PASS. The review does not prove all non-mutating testing techniques impossible. |
| Isolate QA-authored cases from the frozen package | Accepted. Prefer external harness/stimuli where feasible. A separate package copy requires production-byte verification, an explicit test-only delta and treatment of path-sensitive behavior. Merely moving the package is not proof of equivalence. |
| Clarify denominators for added cases | Accepted as useful clarification of existing QA requirements. Keep required unit and overall-suite rates separate; include new required cases and never inflate counts with retries or duplicate instrumented runs. |
| Preserve the full suite and review coverage changes | Accepted. Freshly summed per-file evidence is 3335/3497 across 13 files. At that denominator, 12 lost covered lines still meet the floor; 13 do not. The assertion that slow tests specifically carry this margin is unsupported by the aggregate evidence and is excluded. |
| Clarify branch status | Accepted with terminology correction: NOT_RUN when uncollected; unsupported is a reason only when demonstrated. No fabricated branch percentage or branch floor. |

The compatible clarifications are applied in [qa-handoff-addendum.md](qa-handoff-addendum.md). The recommendation to edit the historical handoff directly is excluded: it is bound by retained artifact hashes. Neither original handoff nor delivery/manifest/snapshot was changed. No product repair, test-seam addition, installation, operational skill modification or native launch was performed.

## Verification and limitations

Ran `python -B -X utf8 docs/plan/advisor-runs/20260916T185825Z-diagnostic-handoff-intake/verify_assessment.py` from `C:\Projects\DevForgeAI` using native Windows Python through PowerShell: exit 0. It verified all 58 current candidate files, all 58 snapshot files and all 323 indexed historical artifacts against retained byte lengths and SHA256 values. Manifest SHA256 remains `419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540`. It independently summed the retained suite output to 133 passed, zero failed/ignored, summed coverage to 3335/3497, and extracted the zero-count LLVM segments on the query-failure expression. These are readbacks of developer evidence, not fresh test executions.

The reviewer used repository reads; it did not hash the package or execute tests. Parent hash/readback checks address identity and arithmetic only. Unsupported claims about impossibility of testing and per-test coverage contribution remain qualified above; no third reviewer call is permitted. Independent offline QA remains NOT_RUN, native WN-01/WN-02 remain NOT_RUN, and framework acceptance remains NOT_EVALUATED. The assessed handoff can guide a separate QA session, which must preserve unresolved required gaps and all original launch boundaries.
