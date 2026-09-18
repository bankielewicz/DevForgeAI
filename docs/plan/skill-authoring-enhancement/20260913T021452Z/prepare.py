"""Stage an authorized migration; never change the development destinations."""
import ast
import hashlib
import json
from pathlib import Path
import shutil

RUN = Path(__file__).resolve().parent
STAGE = RUN / 'candidate'
B = STAGE / 'skill-builder'
V = STAGE / 'skill-validator'
shutil.copytree(RUN / 'inputs/skill-builder', B)
shutil.copytree(RUN / 'inputs/skill-validator', V)
# Identify the exact transitive custody/parser dependency subset. No grader
# dispatcher, routing, package-link or quality reduction is included.
source = (B / 'scripts/graders.py').read_text(encoding='utf-8')
tree = ast.parse(source)
definitions = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
needed = {'fields', 'snapshot', 'strings', 'adoption_record', 'revision_origin'}
while True:
    expanded = needed | {n.id for name in needed for n in ast.walk(definitions[name]) if isinstance(n, ast.Name) and n.id in definitions}
    if expanded == needed:
        break
    needed = expanded
parts = ['"""Legacy custody and record readers extracted from builder 2.0.0. No quality grader or dispatcher."""']
for node in tree.body:
    if isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)) or isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in needed:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('GRADER_IDS', 'BUILD_MANIFEST_SHA256') for t in node.targets):
            continue
        parts.append(ast.get_source_segment(source, node))
(B / 'scripts/custody.py').write_text('\n\n'.join(parts) + '\n', encoding='utf-8')
evidence = (B / 'scripts/build_evidence.py').read_text(encoding='utf-8').replace('import graders', 'import custody').replace('graders.', 'custody.')
(B / 'scripts/build_evidence.py').write_text(evidence, encoding='utf-8')
# Quality assets move to validator; legacy records and fixtures retain meanings.
(V / 'evals/cases.jsonl').rename(V / 'evals/validator-cases.jsonl')
for folder in ('tests', 'evals'):
    for source_path in (B / folder).iterdir():
        target = V / folder / source_path.name
        if target.exists():
            raise ValueError('migration collision: ' + str(target))
        if source_path.is_dir():
            shutil.copytree(source_path, target)
        else:
            shutil.copy2(source_path, target)
    # Both resolved endpoints are verified staging descendants, never originals.
    resolved = (B / folder).resolve()
    assert resolved.is_relative_to(STAGE.resolve())
    shutil.rmtree(resolved)
for filename in ('graders.py', 'run_evaluation.py'):
    shutil.move(str(B / 'scripts' / filename), str(V / 'scripts' / filename))
for filename in ('build_evidence.py', 'custody.py'):
    shutil.copy2(B / 'scripts' / filename, V / 'scripts' / filename)
for filename in ('evaluation.md', 'evaluator-contracts.md'):
    shutil.move(str(B / 'references' / filename), str(V / 'references' / filename))
# Builder retains schemas needed to safely interpret legacy custody records.
(B / 'schemas').mkdir()
for name in ('adoption-evidence.schema.json', 'build-artifacts.schema.json', 'evidence.schema.json'):
    shutil.copy2(V / 'evals' / name, B / 'schemas' / name)
for name in ('init_skill.py', 'generate_openai_yaml.py'):
    shutil.copy2(RUN / 'inputs/skill-creator/scripts' / name, B / 'scripts' / name)
shutil.copy2(RUN / 'inputs/skill-creator/license.txt', B / 'assets/skill-creator-license.txt')
(RUN / 'custody-extraction.json').write_text(json.dumps({'source_sha256': hashlib.sha256(source.encode()).hexdigest(), 'functions': sorted(needed)}, indent=2) + '\n')
print(json.dumps({'candidate': str(STAGE), 'custody_functions': len(needed)}))
