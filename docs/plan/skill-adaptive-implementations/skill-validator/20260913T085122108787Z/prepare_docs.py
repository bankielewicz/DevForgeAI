"""Retain exact policy catalogs as focused skill resources; no spec modification."""
from pathlib import Path
from capture import ROOT, RUN

target = ROOT / 'src/agents/skills/skill-validator'
spec = (RUN / 'inputs/skill-validator-adaptive-enhancement-spec.md').read_text(encoding='utf-8')
builder = (RUN / 'inputs/skill-builder-adaptive-enhancement-spec.md').read_text(encoding='utf-8')
def section(text, start, end):
    return text[text.index(start):text.index(end)]
def write(name, text):
    (target / 'references' / name).write_text(text,encoding='utf-8')

write('adaptive-validation.md', '''# Selected-set and adaptive assessment

Contents: intake; mandatory AV catalog; shared contracts; supplemental records; reductions; helper interfaces.
This is the frozen adaptive project policy (2026-09-12), not universal Codex metadata. Preserve [origin](origin.md), [authoring intake](authoring-intake.md), [rules](rules.md), [reporting](reporting.md), and review-before-repair [handoff](handoff.md). Existing ordinary skills need no adaptive metadata.

''' + section(spec,'## 2. Invocation and intake','### 3.2 Unicode') +
section(spec,'## 4. Adaptive and set contracts','## 5. Bounded execution') +
section(spec,'## 6. Findings, reduction, and deliverables','## 8. Requirement register') + '''
## Shared closed schemas and independent reader

The validator's `scripts/adaptive_contracts.py` reads these schemas locally; it neither imports nor calls builder. Each Ref in these new families is an already retained resolved absolute file plus raw-byte SHA-256. Schema-1 checks retain their own run-relative base. Store new records in separate supplemental/set roots so the legacy observer does not reinterpret absolute references.

''' + '\n'.join('- ['+name+'](../schemas/'+name+'.schema.json)' for name in ('project-evidence-v1','adaptation-proposal-v1','adaptation-selection-v1','adaptive-skill-v1','set-authoring-v1','set-validation-request-v1','project-binding-v1','standalone-set-input-v1','set-assessment-v1','adaptive-observations-v1','adaptive-check-observation-v1')) + '''

Every member checks file must include a required row for each catalog rule, including unknown and justified inapplicable rows. Separate deterministic and semantic/behavioral rows where methods differ. Unknown applicability is NOT_RUN and remains in the denominator. Missing member reports/checks contribute unperformed catalog rows. Retain a pinned rule-set and independent expectations before helper execution; helper stdout is referenced evidence, not additional denominator rows.

New schemas are closed: all listed fields (including nullable fields) are present; unsupported versions/extra fields, duplicate/nonfinite JSON and boolean-as-integer are rejected. Ref locators must support the actual conclusion; shape validation cannot decide meaning. Selected membership, dependencies and handoff graphs must resolve without adding packages. Complete package manifests are sorted row arrays; see [shared definitions](adaptive-shared-contracts.md).

For descriptor parent requirement inventories the helper supports a fenced devforgeai-requirements JSON array or an unambiguous ID/Requirement table. Other clear locators require manual lineage review and a retained explicit mapping; do not report a semantic defect solely for an unsupported locator. Review every parent requirement's retained/modified/removed disposition, current change authorization and core readback. A matching requirement ID alone is not proof of semantic preservation.

Record strengths and limitations for role/domain grounding, project conventions, source identity separation, bindings, updates and actual set handoffs. A valid package/ref is custody evidence. No Python helper, editable binding, model PASS, certification label or speculative Rust command provides protected acceptance.
''')

write('adaptive-shared-contracts.md', '# Shared adaptive record definitions\n\nFrozen project-policy contract. Semantic readers are validator-local. Read only the family needed for the selected input.\n\n' + section(builder,'### 5.1 Type notation','## 7. Update review').replace('[', '[') + '\nAn ordinary validation does not perform setup or authoring actions described as ownership above. Test operational consumers solely under disposable synthetic roots.\n')

write('text-resource-checks.md', '# Text, resources, context and effects\n\nUse `scripts/adaptive_observe.py package --source <captured-package>` for deterministic observations. Name the original package directory when retaining a snapshot; if the snapshot is named source, assess directory identity against its bound original separately.\n\n' + section(spec,'### 3.2 Unicode','## 4. Adaptive') + '''
## Finalizing observations

Retain helper stdout unchanged with its helper-local check identity. Put semantic dispositions, reasons and evidence in a separate adaptive-observations-v1 record. Package parser nodes remain unresolved_usage until actual consumers are reviewed. Unicode excerpts intentionally show only the escaped candidate character, avoiding adjacent secrets; inspect the retained byte/line location under the authorized secret-safe boundary. Scan results are not security certification.

Inspect malformed tables, ambiguous destinations, script calls, instruction path mentions and template uses manually. Add located edges of the declared kinds to the finalized graph; dynamic/unsupported renderer behavior remains unresolved. Read schemas and examples as data, never import a target to discover its runtime behavior. Binary resources are inventoried with classification and reviewed at call sites; declared binary/text type overrides guessing during finalized review.

The optional metadata reader checks supported string/boolean/dependency shapes. Unknown extension fields remain applicability questions; do not strip them or require optional configuration. Pin [installed UI guidance](../assets/openai-yaml-guidance.md) when this host configuration is relevant, and record source freshness.

For a selected required token budget, null tokens imply NOT_RUN and incomplete budget verification. No budget is inferred. Named tiktoken encoding data must already be local; no downloads, arbitrary module imports or character-to-token conversions. Retain exact excerpt evidence for observed excerpts; do not charge a full-file estimate as actual host consumption. The record checker verifies arithmetic but cannot reconstruct missing host load events.
''')

write('set-trials.md', '# Bounded terminal, adaptive and set trials\n\nRead [trials](trials.md) for existing trial/attempt records. Pin cases and independent expected effects before execution. Ordinary skill runs select applicable tests proportionately; the full VAT suite is maintenance coverage.\n\n' + section(spec,'### 5.1 Case planning','## 6. Findings') + section(spec,'| Case | Fixture/action','## 9. Excluded profiles') + '''
## Record and report each branch

Retain false positives and missed seeded defects with case IDs and observed artifacts. Description classification uses unlabeled prompts and only the actual description; explicit loading, native selection, cold child execution and self-review are different evidence. User corrections and actual applicable precedence govern; ambiguity at equal scope is unresolved. Do not repeat already answered permission questions.

For binding tests run the selected target's inspected helper via an argument vector before any authorized synthetic product action. Verify exact package/root/role/selected state, parent responsibility conflicts, missing/stale/relocated cases and before/after allowed writes. The editable binding checks applicability, not privileged enforcement. A rejected check must yield no product outputs/downstream calls; merely observing helper exit 1 is insufficient evidence of the surrounding workflow.

For updates compare recorded parent/evidence bytes and all requirement dispositions; changed bytes trigger impact review, not automatic defect, core rebase, repair or carried quality approval. Preserve partial work and every attempt. When unavailable host/auth/selection evidence or companion prevents an integration case, retain NOT_RUN and continue independent supported checks.

Keep repair, dependency installation, binding setup outside synthetic fixtures, plugin/MCP assembly, hooks/CI, WCAG/enterprise/OWASP certification, L0-L3/repository maturity scoring and future Rust acceptance outside this assessment. Validate an explicitly selected accessibility/security output only to its actual contract.
''')
(target / 'assets/openai-yaml-guidance.md').write_bytes(Path('C:/Users/bryan/.codex/skills/.system/skill-creator/references/openai_yaml.md').read_bytes())
