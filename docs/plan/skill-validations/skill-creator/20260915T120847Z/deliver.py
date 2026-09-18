"""Write report and proposed future correction; no target edits."""
import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parent
def read(p):return json.loads((R/p).read_text())
def ref(p):return {"path":p,"sha256":hashlib.sha256((R/p).read_bytes()).hexdigest()}
def write(p,v):
    with (R/p).open("x",encoding="utf-8",newline="\n") as f:f.write(v if isinstance(v,str) else json.dumps(v,indent=2)+"\n")
a=read("assessment.json");f=read("findings.json")["findings"];pkg=a["package_digest"]
proposal=f"""---
id: REVISION-SKILL-CREATOR-20260915T120847Z
skill_name: skill-creator
target: codex
status: proposed
---
# Proposed skill-creator revision

## Identity and scope
Target: C:/Users/bryan/.codex/skills/.system/skill-creator.
Observed package SHA-256: {pkg}.
Origin: [origin-spec.md](origin-spec.md); exact bytes: [source-manifest.json](source-manifest.json).
This proposes a focused future correction of the eight findings. It does not authorize modifying the installed system package or invoking a builder.

## Purpose, triggers and exclusions
Preserve creation/update of appropriately scoped Codex skills and needed supporting resources. Trigger for reusable skill authoring and selected existing-skill edits. Ordinary task execution, installation, publication and standalone independent audits remain separate.
Preserve the core principles, concise discovery metadata, progressive disclosure, current permissions and conditional independent forward testing.

## Inputs and defaults
User outcome, selected destination, existing bytes, optional resources and explicit UI override strings. Ask only for material missing information. Do not reinitialize existing work.
Naming becomes explicitly inclusive: 1–64 lowercase ASCII letters/digits separated by single hyphens. Keep existing disclosed new-name normalization; correct prose without relabeling historical 64-character test failures.
Preserve current default-location behavior in this bounded repair. Official documentation differs on the user directory; defer migration until native evidence resolves compatibility.
Keep implicit invocation enabled by default; preserve existing policy unless the user requests a change. Examples do not require optional UI fields.

## Output contracts
SKILL.md remains YAML plus Markdown, with nonempty name/description and supported optional fields preserved.
Initializer outputs starter SKILL.md, agents/openai.yaml and only requested resources/examples. Initial scaffolds remain permissible during authoring, but recognized unfinished scaffolds must fail completion validation.
Generator produces valid YAML with quoted strings, preserving supported caller values after YAML decoding. Supplied default_prompt must include the selected skill invocation; absent optional prompt remains absent.
Quick validator returns clear nonzero rejection without traceback for identified malformed cases. It remains structural evidence, not semantic or framework acceptance.

## Workflow and routing
1. Inspect selected bytes/outcome; preserve unrelated work.
2. Optionally initialize a new skill using documented arguments; edit existing skills in place.
3. Load references/openai_yaml.md for UI changes. Preserve the whole-file generator warning and in-place branch for policy/dependency-bearing files.
4. Author focused instructions and only necessary resources.
5. Execute limited validation and actual changed-script tests; independently inspect outputs.
6. Run bounded disposable forward trials when needed and authorized, retaining failures.
7. Deliver artifact paths, executed evidence and limitations; no installation/publication implied.

## Requirements and acceptance cases
| ID | Proposed mandatory correction | Acceptance |
| --- | --- | --- |
| REV-01 | Reject blank/whitespace-only required name and description. | V08/V09 reject cleanly; completed V01/V02 remain accepted. |
| REV-02 | Recognize standalone unfinished TODOs in plain/list lines outside literal fenced examples. | V14/V16 reject; V15/V22 remain accepted; add independent ordered-list/fence cases. |
| REV-03 | Require a complete closing delimiter line. | V17 rejects; valid LF/CRLF and EOF delimiters pass. |
| REV-04 | Reject non-string/mixed YAML keys before sorting diagnostic keys. | V20 returns clear nonzero rejection without traceback. |
| REV-05 | Use YAML-safe escaping that preserves supported strings, including internal carriage return. | G15 decoded value exactly equals supplied value; G02 Unicode/quotes/backslashes still round-trip. |
| REV-06 | Replace under 64 with at most 64, consistent with existing helpers. | Future 64-character cases accept under revised contract; original failures remain intact. |
| REV-07 | Validate supplied default_prompt invocation before writing. | G14 rejects without modifying existing YAML; G02/G13 valid prompts pass; omitted prompt remains absent. |
| REV-08 | Align bundled UI short_description with its 25–64 constraint. | Proposed value Create or update Codex skills meets range; all other metadata preserved. |

REV-03: the generator has the same parser pattern by source inspection; add its own red test before changing it. Only quick-validator malformed-delimiter behavior was executed here.
REV-07 is a local guidance/output consistency requirement, not a universal host-format rule. No optional enhancement is silently included.

## Resources, dependencies and portability
Preserve three helper names, existing CLI flags, UI reference, icons and license.
Helpers remain Python supporting resources using existing PyYAML. No added network, GUI, MCP or dependency installation. Use explicit UTF-8 in changed text I/O and verify on native Windows; Linux/macOS remain separately unqualified.
This system-skill audit is not a DevForgeAI framework build. Future selected framework/skill-build contracts must separately supply their mandatory evaluation artifacts; Python cannot become enforcement authority.

## Side effects, recovery and preservation
Future implementation starts from a captured development candidate with exact hashes. Installed-system updates require separate explicit authorization and filesystem permissions.
Validate generator arguments before writing; invalid input preserves prior output. Initializer currently retains partial starters after later failure; rollback is not promised or silently added.
Retain red/green/refactor/QA evidence and failed attempts. No test weakening or rewriting historical results. REV-06 explicitly changes only the future naming contract/oracle.

## File mapping
- scripts/quick_validate.py: REV-01 through REV-04.
- scripts/generate_openai_yaml.py: REV-03 parsing consistency, REV-05, REV-07.
- scripts/init_skill.py: affected integration regressions; no unnecessary edit to inclusive boundary.
- SKILL.md: REV-06; preserve unrelated guidance/routing.
- agents/openai.yaml: REV-08 only.
- UI reference, icons and license: preservation targets.
- Fresh independent tests/evidence: all requirements and manifests.

## Review and execution readiness
Pending review; no findings selected for repair. Execution BLOCKED under the validator's legacy handoff model because no generated/adopted baseline or authorized installed-system mutation is established. This does not block reviewing these findings.
The observed snapshot is recovery evidence, not adoption. A future request should select this proposal, findings and development candidate location. Installation remains separate.
"""
write("revision-spec.md",proposal)
table="\n".join("| "+x["label"]+" | "+x["severity"]+" | "+x["description"]+" | "+", ".join(x["verification_cases"])+" |" for x in f)
dimtable="\n".join(f"| {k} | {v['outcome']} | {v['required_evaluated']}/{v['required_total']} |" for k,v in a["dimensions"].items())
report=f"""# skill-creator validation report

## Conclusion
**FAIL — assessment completed.** Basic structure and both independent authoring scenarios pass, but helpers have reproducible validation/output defects. Eight distinct findings: three major, five minor.

Target: C:/Users/bryan/.codex/skills/.system/skill-creator.
Run: {R.name}.
Package SHA-256: {pkg}.
Rule-set SHA-256: {a['rule_set_digest']}.
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
{table}

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
{dimtable}

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
"""
write("validation-report.md",report)
write("handoff.json",{"schema_version":"1","run_id":R.name,"target_name":"skill-creator","original_target_root":r"C:\Users\bryan\.codex\skills\.system\skill-creator","original_manifest":ref("source-manifest.json"),"origin":ref("origin-spec.md"),"proposed_spec":ref("revision-spec.md"),"findings":ref("findings.json"),"report":ref("validation-report.md"),"selected_finding_ids":[],"deferred_finding_ids":[],"proposal_review_state":"pending","review_instruction":None,"builder_readiness":"BLOCKED","readiness_reasons":["Validation-only authorization; no repair selected.","Legacy generated/adopted baseline not verified; snapshot is not adoption."],"baseline_kind":None,"baseline_reference":None,"adoption_required":True,"adoption_capability":"Not assessed for this external system package.","permitted_target_root":None,"preservation_requirements":["Keep installed package unchanged until separately authorized.","Preserve all evidence/failed attempts.","Separate future development candidate from installation."]})
print(str(R/"validation-report.md"))

