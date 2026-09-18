"""Focused documentation correction from independent completeness review."""
from capture import ROOT, RUN

root = ROOT/'src/agents/skills/skill-validator/references'
path = root/'adaptive-validation.md'
text = path.read_text(encoding='utf-8')
text = text.replace('Keep the name `skill-validator`; update description to include selected sets and adaptive core/variant/expertise assessment without attracting general repository audits. Preserve automatic invocation unless explicitly changed by the user.', 'The selected skill may be ordinary or adaptive; the validator also accepts explicit sets. Preserve its existing invocation policy during assessment.')
text = text.replace('Implement schemas/readers locally in validator; it must not import runtime code from an installed builder or require builder availability. Shared golden JSON fixtures must prove that the two implementations agree.', 'Validator-local schemas/readers consume these interfaces without importing runtime code from an installed builder or requiring builder availability. Maintenance golden fixtures assess agreement between implementations.')
start = text.index('Add mode routing in SKILL.md')
end = text.index('```text',start)
text = text[:start] + 'The read-only helper interfaces are:\n\n' + text[end:]
text = text.replace('Missing member reports/checks contribute unperformed catalog rows.', 'When checks exist but a report is missing, preserve the available checks and their failures/counts while marking that member INCOMPLETE. Missing checks contribute unperformed catalog obligations.')
path.write_text(text,encoding='utf-8')
builder = (RUN/'inputs/skill-builder-adaptive-enhancement-spec.md').read_text(encoding='utf-8')
common = builder[builder.index('### 5.1 Type notation'):builder.index('### 5.2 Project evidence')]
tables = []
for start,end in [('### 5.2 Project evidence','### 5.3 Selection'),('### 5.3 Selection','### 5.4 Portable'),('### 5.4 Portable','## 6. Operational'),('### 6.1 Record','### 6.2 Runtime')]:
    fragment = builder[builder.index(start):builder.index(end)]
    tables.append('\n'.join(line for line in fragment.splitlines() if line.startswith('|')))
text = '''# Shared adaptive record definitions

These frozen project-policy schemas are input contracts for read-only validation, not authoring or operational setup instructions. Read the relevant family only. Schema documents under ../schemas are local data; scripts/adaptive_contracts.py is an independent validator reader. Ordinary skills need no adaptive descriptor.

''' + common + '\n## Project evidence and proposals\n\n' + tables[0] + '\n## Selection and set envelopes\n\n' + tables[1] + '\n## Portable descriptors\n\n' + tables[2] + '\n## Operational binding shape\n\n' + tables[3] + '''

## Cross-record review

Verify IDs are unique and references resolve to exact retained bytes. Source/user requirements need supporting locators; derived requirements need rationale. Unknown facts do not assert observed conclusions. Expertise needs domain/architecture evidence or current user domain requirements; names/personas alone do not ground a role. Missing evidence remains a gap.

For a proposal, create actions have no existing package; retain/revise actions require one; retention also requires a concrete destination. Core/expertise have no parent lineage. Variants require a distinct parent identity, exact digest, one disposition per parent requirement and equivalent retained child statements. Modified requirements identify replacements; removal needs current user support and semantic review. No reader grants authorization from a keyword or matching ID. Parent/current bytes are read-only.

Selected destinations correspond exactly to selected members without overlap with each other or parent roots. Dependencies and directed handoffs are acyclic, with ASCII-ID topological tie breaking. Required handoff producers occur in consumer depends_on. Missing dependencies do not authorize adding packages.

Validate set-authoring per-member custody, partial applied paths, transitive DEPENDENCY_BLOCKED outcomes and aggregate state: all RETAINED means NO_CHANGE; at least one AUTHORED and all others AUTHORED/RETAINED means AUTHORED; delivered changes plus unresolved members means PARTIAL; otherwise BLOCKED. Authoring validation/testing fields remain NOT_PERFORMED and do not establish quality.

Full-set requests contain the complete original selection with no omissions. Eligible subsets partition the selected IDs, include at least one omission, contain only complete AUTHORED/RETAINED package bindings, and are dependency-closed. Handoffs equal original selected handoffs whose endpoints are requested; omitted IDs identify all others. Copy scope/omissions into the assessment unchanged. Later narrowing requires a new captured input.

Descriptors carry no own digest, framework project UUID, author-machine root or binding record. Parent digest/name and product-relative facts are allowed. Contract path is references/adaptive-contract.md and defines responsibilities/exclusions, triggers/near misses, input/output/effect/recovery/dependency contracts, parent dispositions and observable completion. Resource roles resolve but do not prove usage. The Python 3.10+ binding capability and actual helper/contract routes must be reachable before adaptive product actions.

## Binding observations and portability

Only disposable synthetic operational .agents/devforgeai/project-binding.json fixtures may be created by validation. Real bindings remain read-only; retain sanitized observations and digest, never UUID/content in generic evidence. Call the selected inspected target helper through an argument vector:

```text
python -B -X utf8 <loaded-package>/scripts/check_project_binding.py --project-root <selected-root> --skill-root <loaded-package>
```

Inspect exact loaded package/root/name/role/selection bindings, complete bytes and related selected core/variant descriptors. A core's responsibility group is its name; a variant's group is parent_core.name. At most one selected implementation occupies a group, including two variants sharing a parent. The parent need not be installed solely to preserve lineage. Compare resolved roots using native case normalization; no Windows/WSL path substitution.

The closed binding-observation-v1 object contains status, reason_code, nullable binding_sha256/package_digest and details. MATCH/BOUND exits 0. MISMATCH exits 1 for MISSING_BINDING, INVALID_BINDING, ROOT_MISMATCH, UNBOUND_SKILL, PACKAGE_CHANGED, ROLE_MISMATCH, NOT_SELECTED, AMBIGUOUS_ROLE or UNSAFE_PATH. UNAVAILABLE exits 2 for CAPTURE_LIMIT or IO_ERROR. CLI usage errors use stderr and exit 2. Output must not disclose concrete identity or secrets.

On non-MATCH, the target reports the prerequisite and performs no product writes or downstream calls. A resumed invocation or changed binding/package requires a fresh check; a cached observation grants no authority. Relocation requires separately authorized setup/rebinding, never automatic initialization. This editable applicability check is not protected identity enforcement or Rust qualification. See [set-trials](set-trials.md) for actual effects and two-host fixture evidence requirements.
'''
(root/'adaptive-shared-contracts.md').write_text(text,encoding='utf-8')
print('Focused read-only contract reference; removed maintenance imperatives and corrected missing-report coverage explanation.')
