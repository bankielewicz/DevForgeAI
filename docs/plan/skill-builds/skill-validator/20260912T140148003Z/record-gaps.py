"""Record pre-generation gaps from the preserved raw specification; no package writes."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / 'inputs/SKILL-SPEC-013-skill-validator.md'
raw = source.read_bytes()
digest = hashlib.sha256(raw).hexdigest()

def refs(*phrases):
    result = []
    for phrase in phrases:
        excerpt = phrase.encode('utf-8')
        start = raw.index(excerpt)
        result.append(dict(input_id='spec', start_byte=start, end_byte=start + len(excerpt),
                           sha256=hashlib.sha256(excerpt).hexdigest()))
    return result

gaps = [
    dict(id='GAP-001', reason_code='CONTRADICTORY_REQUIREMENT', requirement_ids=[],
         source_refs=refs('pass` when no finding of any kind was recorded',
                          'The verdict may still be `pass`, but the unrun rule is visible.',
                          'docs/reports/validate-skill-validator.md exists with verdict pass'),
         affected_outputs=['references/report.md', 'scripts/validate_skill.py', 'evals/evals.json'],
         description='Section 7 requires findings for divergence or not_run; section 9 permits pass with not_run. Section 10 eval 2 requires pass while requiring a Review divergence. Eval 1 expected_output says pass while its expectations require findings and only the not_run fix row, despite a required divergence.',
         required_resolution='Specify the governing verdict and Fixes policy and authorize corrected evaluation expectations, or provide a corrected specification. Recommended: section 7 closed verdict rule; retain all applicable findings and repairs.'),
    dict(id='GAP-002', reason_code='CONTRADICTORY_REQUIREMENT', requirement_ids=[],
         source_refs=refs('Zero matches or more than one match is `status: needs_user`.',
                          'Where the package records `metadata.devforgeai-spec`, that id is the tie-breaker'),
         affected_outputs=['SKILL.md', 'references/spec_conformance.md', 'scripts/spec_diff.py'],
         description='Section 6 requires needs_user for ambiguous specification matches and treats metadata mismatch as a finding; section 9 also introduces metadata.devforgeai-spec as a tie-breaker. These produce different selected inputs for the same package.',
         required_resolution='Choose whether ambiguity always requires an explicit --spec (recommended, section 6), or define when metadata may resolve it.'),
    dict(id='GAP-003', reason_code='UNSUPPORTED_CAPABILITY', requirement_ids=[],
         source_refs=refs('Call `devforgeai phase start skill-validator <name>`.',
                          'the `SubagentStop` hook routes each worker\'s receipt to the sequencer',
                          'a read-only sandbox with an approval policy that requests no approval'),
         affected_outputs=['SKILL.md', 'references/envelope.md', 'references/workers/anatomy_checker.md',
                           'references/workers/provider_checker.md', 'references/workers/spec_conformance_checker.md',
                           'references/workers/validate_report_writer.md'],
         description='devforgeai is absent from the observed Windows PATH. Available collaboration tools do not expose per-worker tool denial, sandbox/approval selection, or the required SubagentStop sequencer integration. Task instructions cannot establish those enforcement properties. No legacy implementation was inspected or executed.',
         required_resolution='Provide a supported compiled-Rust runtime and the required integration, or explicitly authorize a revised standalone development-observation contract that removes reliance on sequencer enforcement, native identities, and promotion. The latter changes the specification and must be recorded as a digest-bound clarification.'),
]

def write(name, obj):
    (root / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

write('spec-gaps.json', dict(schema_version='1', gaps=gaps))
write('input-inventory.json', dict(schema_version='1', inputs=[dict(
    id='spec', path='inputs/SKILL-SPEC-013-skill-validator.md',
    resolved_path=r'\\wsl$\Ubuntu\home\bryan\Projects\DevForgeAI\docs\design\specs\SKILL-SPEC-013-skill-validator.md',
    role='spec', bytes=len(raw), sha256=digest)],
    target=r'C:\Projects\DevForgeAI\src\agents\skills\skill-validator',
    target_created=False, contract_status='BLOCKED_BEFORE_CONTRACT_COMPLETION',
    exclusions=['backup directories', 'legacy CLI/hook implementations',
                r'\\wsl$\Ubuntu\home\bryan\Projects\DevForgeAI2\.claude\scripts\devforgeai_cli']))

report = '''# Skill Specification Build Report

## Result

Authoring: **BLOCKED before candidate generation**. No skill-validator package was created.

| Dimension | State | Evidence or reason |
| --- | --- | --- |
| Structural checks | NOT_PERFORMED | No candidate exists. |
| Deterministic evaluation | NOT_PERFORMED | spec-v1 requires a resolved contract and candidate. |
| Behavioral evaluation | NOT_PERFORMED | Contradictory expectations and unavailable runtime. |
| Supporting-script execution | NOT_PERFORMED | No package scripts generated. record-gaps.py only records build evidence. |
| Independent forward trials | NOT_PERFORMED | This is not a builder enhancement. |
| Routing evaluation | NOT_PERFORMED | No generated skill. |
| Framework enforcement | NOT_IMPLEMENTED | No supported runtime established in this build. |
| Rust qualification | NOT_PERFORMED | No runtime qualification. |
| Operational installation | NOT_PERFORMED | Development-source request only. |

## Request, selection, and boundary

The user authorized a specification build named skill-validator in C:/Projects/DevForgeAI/src/agents/skills from the explicitly selected WSL specification. That instruction resolves the specification's example ./out location and the builder selects a Codex development package; dual-provider output and native profiles are not generated merely for symmetry.

The original 92,463 bytes are retained in [the input snapshot](inputs/SKILL-SPEC-013-skill-validator.md). SHA-256: DIGEST.

Host observations: Windows, PowerShell; python resolves to Python 3.10.11, PyYAML import is available; codex-cli identifies itself as 0.154.0 with access-denied warnings for temporary PATH aliases. devforgeai and skills-ref were not found on PATH. The specification requires Python 3.11+; other interpreters have not been qualified. CLI identification is not qualification.

## Contract and resource traceability

[Input inventory](input-inventory.json) preserves identity and raw-byte digest. [Machine-readable gaps](spec-gaps.json) bind exact source excerpts by byte interval and SHA-256. Requirement IDs are empty because a finalized requirement mapping was not created before detecting contradictions. No completed build-contract, candidate, generated baseline, provenance, or successful baseline pointer is claimed. Specification dependency digests were not verified; exploration stopped at substantive contract gaps.

## SPEC GAPS

GAPS

## Revision result

NOT_APPLICABLE: destination was absent. No regeneration or destination mutation occurred.

## Executed checks and editorial findings

Read the loaded builder and its specification, evidence, evaluation, evaluator-contract and report references. Read the selected specification after the initial sandbox access denial and approved retry; captured raw bytes with an approved filesystem read. Examined the relevant rule, worker, handoff, script, target and evaluation sections. The initial large outputs were truncated by the tool; targeted section reads supplied the cited gap evidence. No claimed structural, semantic, or deterministic PASS is inferred from inspection.

The builder explicitly says: "An essential unavailable capability, missing decision, or contradiction produces a concrete gap and `BLOCKED`; do not replace required behavior with advisory prose." Its references/spec-build.md additionally says: "Do not generate candidate package files while a blocking contract gap remains." Specification section 0 rule 7 separately requires stopping before output on contradiction.

## Handoff

Resolve GAP-001 and GAP-002 and select a supported runtime or authorize the revised development-observation scope described in GAP-003. Preserve this run and use a fresh evidence directory for the resolved build. [Command log](command-log.md). No generated package or installation is available from this run.
'''
gap_text = '\n\n'.join(f"### {g['id']} — {g['reason_code']}\n\n{g['description']}\n\nRequired resolution: {g['required_resolution']}" for g in gaps)
(root / 'build-report.md').write_text(report.replace('DIGEST', digest).replace('\nGAPS\n', '\n' + gap_text + '\n'), encoding='utf-8')
print(json.dumps({'status': 'BLOCKED', 'gaps': len(gaps), 'input_bytes': len(raw), 'input_sha256': digest,
                  'package_created': False}, indent=2))
