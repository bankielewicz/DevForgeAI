# skill-creator validation report

## Conclusion
**FAIL — assessment completed.** Basic structure and both independent authoring scenarios pass, but helpers have reproducible validation/output defects. Eight distinct findings: three major, five minor.

Target: C:/Users/bryan/.codex/skills/.system/skill-creator.
Run: 20260915T120847Z.
Package SHA-256: 48298d08909b8be87327c023dbd9f29b3c0f0f57419505c1ee6cab5accb4fbf4.
Rule-set SHA-256: e6aae3af79286efaa718a34cf1eee0a9a9b8566fd2e01a9852b8996c9ee06a42.
All 9 captured files remain unchanged; snapshot complete, no exclusions. Historical origin unknown.

## Requested areas
| Area | Result | Evidence |
| --- | --- | --- |
| Structure | Basic frontmatter/name/link checks PASS; local UI length constraint FAIL | [structure](observations/structure/stdout.txt), [UI measurement](observations/ui-length.json) |
| Helpers | 42/51 PASS, 9 FAIL (82.3529411764706%) | [helper report](trials/helpers/helper-report.md), [cases](trials/helpers/case-results.json) |
| Instructions | Scope/resource routing coherent; naming boundary contradicts helpers | [semantic review](semantic-review.md), [workflow](workflow-map.json) |
| Independent behavior | Creation 1/1 PASS; update 1/1 PASS; routing 6/6 PASS | [creation](trials/create/primary-review-002.json), [update](trials/update/primary-review-002.json), [routing](trials/routing/primary-review.json) |

Helper breakdown: initializer 13/14; generator 13/15; quick validator 16/22. Two failures concern the same local naming inconsistency at different interfaces. Nine failed cases reduce to seven helper/instruction findings; bundled UI metadata adds the eighth.
Combined declared behavior cases: 50/59 passing (84.7457627118644%). Each case is counted once. The predeclared partial-init retry is a distinct preservation case and does not replace its producer. This is below 95% if used as a qualification suite; it is not framework acceptance.

## Findings
| Finding | Severity | Observed defect | Cases |
| --- | --- | --- | --- |
| SC-F01 | major | Blank name and whitespace-only description both return success. | V08-blank-name, V09-blank-description |
| SC-F02 | major | A standalone unfinished TODO expressed as a Markdown list item returns success. | V16-scaffold-bullet |
| SC-F03 | major | Closing marker ---trailing is accepted as a frontmatter delimiter. | V17-closing-delimiter |
| SC-F04 | minor | Mixed numeric and string YAML keys raise uncaught TypeError while sorting. | V20-mixed-yaml-keys |
| SC-F05 | minor | An accepted internal carriage return is written literally; YAML parsing changes it to a space. | G15-carriage-return |
| SC-F06 | minor | Prose requires fewer than 64 characters; both helpers accept exactly 64. | I10-name-64, V11-name-64 |
| SC-F07 | minor | Generator accepts a default_prompt lacking $skill-name, contrary to bundled UI guidance. | G14-invalid-prompt |
| SC-F08 | minor | Bundled short_description has 24 characters; its UI guidance and generator require 25–64. | UI-LENGTH |

Source locators, exact observations, stable IDs and corrections: [findings.json](findings.json).
UI length/default_prompt constraints are local package requirements. CR round-trip loss is low frequency but demonstrated. Mixed-key rejection exits nonzero with an uncaught traceback.
Whole-file generator replacement is documented; the independent update correctly used in-place editing. Partial initialization is disclosed; rollback was not promised.

## Independent trials
Creation produced exactly [release-note-draft/SKILL.md](trials/create/workspace/release-note-draft/SKILL.md): Added/Changed/Fixed grouping, empty-group omission, preserved issue IDs, unspecified unknown version/date, no invented changes/publication. No unnecessary helpers, references, UI metadata or installation.
Update changed only the requested two values in [draft-note/agents/openai.yaml](trials/update/workspace/draft-note/agents/openai.yaml). Skill, icon, prompt, comments, policy and dependencies were preserved. The unquoted request's final period was treated as part of the description; both punctuation readings are semantically acceptable.
Task agents received realistic requests, their own snapshot/raw fixture, and instrumentation instructions. No intended answer or suspected bug was supplied. Primary review examined actual artifacts and hashes rather than relying on authors' PASS.

## Dimensions and coverage
| Dimension | Outcome | Required evaluated/total |
| --- | --- | --- |
| standards | FAIL | 8/8 |
| workflow | FAIL | 5/5 |
| instructions | FAIL | 6/6 |
| behavior | FAIL | 59/59 |

78/78 applicable required assessment checks evaluated; 10 adaptive rules NOT_APPLICABLE. Unknown applicability: 0 within selected scope. These include semantic summaries and are not independent test case counts.
No new framework enforcement controls proposed; local corrections only.

## Preserved failures and limitations
- Reviewer attempt 001 falsely flagged snapshot drift because Windows Path sorting differed from manifest relative-string ordering. Initial reports/script retained. Corrected readback proves identical path/size/hash mappings; no product trial rerun or modification.
- Native implicit activation, default-directory discovery, rendered UI, forced process cancellation, cross-platform behavior, runtime line/branch coverage: NOT_RUN. No 95% coverage claim.
- Explicit host subagents are distinct from a separate Codex CLI process or native discovery test. Task prose is not OS-enforced isolation. Readback covers selected package/fixtures, not every machine file.
- Helpers retain argv, environment identity/digest, UTC times, exits, raw stdout/stderr and manifests. Agent logs retain commands, combined output, measured durations and exits; exact per-command UTC times were not exposed.
- Text byte/character/line counts complete. Token counts/actual model context use: NOT_RUN.
- Live [official Build skills documentation](https://learn.chatgpt.com/docs/build-skills) agrees on progressive disclosure, scoped descriptions and optional invocation metadata. Its user-directory table differs from the installed default-path instructions. Discovery at those defaults was not tested; no local defect is inferred.
- No repair, installation, operational changes, production mutation or external service use. Python/model evidence is not DevForgeAI framework acceptance.

## Origin and evidence
[Origin](origin-spec.md), [manifest](source-manifest.json), [final original readback](observations/final-readback/stdout.txt), [frozen plan](trials/helpers/frozen-plan.json), [checks](checks.jsonl), [commands](command-log.md).
The Markdown-only helper left original-directory identity/manual consumers unresolved. Primary review bound identity to the manifest and mapped helper calls; raw output retained unchanged.
Official guidance was refreshed read-only; local policy is separately pinned. Model/API-specific requirements do not apply.

## Proposed correction
[Complete proposed revision specification](revision-spec.md) covers all eight findings. No installed file was edited.
Review pending. Builder execution BLOCKED under legacy handoff rules because no generated/adopted baseline or installed-system repair authorization is established. This assessment is complete; no permission is needed to review its results.
[Record-integrity verification](record-integrity.md) is separate and checks evidence shapes/digests, not semantic correctness or framework acceptance.
