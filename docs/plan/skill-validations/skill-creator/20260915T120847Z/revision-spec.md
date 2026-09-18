---
id: REVISION-SKILL-CREATOR-20260915T120847Z
skill_name: skill-creator
target: codex
status: proposed
---
# Proposed skill-creator revision

## Identity and scope
Target: C:/Users/bryan/.codex/skills/.system/skill-creator.
Observed package SHA-256: 48298d08909b8be87327c023dbd9f29b3c0f0f57419505c1ee6cab5accb4fbf4.
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
