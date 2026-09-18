from pathlib import Path
RUN = Path(__file__).resolve().parent
B, V = [RUN / 'candidate' / x for x in ('skill-builder','skill-validator')]
text = '''# Validator-owned deterministic assessment

Use these profiles for historical validated-build records and compatibility regressions. Their schema-1/schema-2 COMPLETE semantics do not apply to new authoring-v1 completion. New handoffs use [authoring-intake.md](authoring-intake.md); read [assessment ownership](assessment-ownership.md) when planning maintenance checks.

## Bound runner and input records

The standard-library Python 3.10+ runner verifies [build-manifest.json](../evals/build-manifest.json), grader versions, files and [profiles.json](../evals/profiles.json) before loading grader bytes. Keep this harness in validator. Changed manifests must reflect intentional package edits before execution; a manifest is reproducibility evidence, not protected approval. Already installed PyYAML is needed only by YAML-aware helpers and Skill Creator's checker.

```text
python -B -X utf8 <validator>/scripts/run_evaluation.py --package-root <validator> --candidate-root <snapshot> --cases <case-jsonl> --output <fresh-jsonl> --run-id <id> --profile <profile>
python -B -X utf8 -m unittest discover -s <validator>/tests -v
```

For authoring integration regressions, AUTHORING_BUILDER_ROOT selects the development builder package under assessment; default is a sibling skill-builder. This maintenance-only selection does not make ordinary validator operation depend on builder availability. Set temporary storage to the disposable run and retain exact evaluator input snapshots/cases before execution. Preserve every command, stdout/stderr, exit/timeout, failed attempt and retry. The default execution timeout is 120 seconds; record any bounded override.

The JSONL output is a new file outside package and candidate; its parent must exist. Case and snapshot inputs are bound before execution. Snapshot ceiling is 2,000 files / 32 MiB; case ceiling is 1 MiB / 1,000 rows. Reject links, junctions, special files, excluded boundaries and unsafe overlaps. No case selects arbitrary executable code.

## Legacy profiles

| Profile | Measured contract |
| --- | --- |
| legacy-import-v1 | Package links and source/disposition accounting |
| import-v2 | Import accounting plus build traceability |
| spec-v1 | Package links and specification traceability |
| revision-import-v2 | Import and B/C/N consistency |
| revision-spec-v1 | Schema-1 specification revision |
| builder-v2 | Legacy five-grader enhancement fixture |
| adoption-v1 | Explicit adoption custody consistency |
| revision-spec-v2 | Adopted/generated schema-2 lineage |
| routing-adoption-v1 | Legacy routing classification |

[evaluator-contracts.md](evaluator-contracts.md) retains exact parameter and record shapes. The [legacy cases](../evals/cases.jsonl), [enhancement cases](../evals/builder-cases.jsonl) and [emitted schema](../evals/evidence.schema.json) remain compatibility inputs. Profiles must include exactly their grader set; duplicate/unknown IDs or nonfinite JSON are errors. Expected negative cases can observe FAIL and still match their expected result. Exit 0 means expectations matched, 1 mismatch, 2 usage/configuration/execution error; no exit code implies framework acceptance.

## Behavioral assessment

For a substantial authoring enhancement, select fresh import, conversational/specification creation, observed editing, untested revision, ownership/conflict and adoption cases as applicable. Give independent evaluators minimal raw inputs and realistic requests without intended corrections. Builder task traces must end with authored artifacts and a manual packet; validator separately executes generated scripts and task behaviors using synthetic positive/negative inputs. Routing classification is separate from native implicit activation. Retain source readback and real partial/publication failures.

Ordinary assessment selects proportionate cases rather than automatically launching every campaign. Report structural checks, deterministic fixtures, script execution, independent workflow behavior, native activation and self-review separately. Missing required coverage remains NOT_RUN. No installation, dependencies, external writes or Rust authority are implied.
'''
(V / 'references/evaluation.md').write_text(text,encoding='utf-8')
# Remove the unused quality result constructor accidentally caught by name-only
# extraction; custody variable names named result do not call this constructor.
import ast
for root in (B,V):
    p = root / 'scripts/custody.py'
    s = p.read_text(encoding='utf-8')
    node = next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='result')
    lines = s.splitlines(keepends=True)
    p.write_text(''.join(lines[:node.lineno-1]+lines[node.end_lineno:]),encoding='utf-8')
print('Removed superseded evaluator ownership instructions and unused result constructor.')
