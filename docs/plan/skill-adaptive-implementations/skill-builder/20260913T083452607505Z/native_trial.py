"""Retained cold CLI attempt. No auth/config changes or bypass flags."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
BUILDER = ROOT / 'src/agents/skills/skill-builder'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=['ordinary', 'edit', 'author-set', 'review-updates', 'python', 'rust', 'typescript', 'docs'])
    args = parser.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt = RUN / 'native' / (stamp + '-' + args.case)
    attempt.mkdir(parents=True, exist_ok=False)
    if args.case == 'edit':
        candidates = sorted(p for p in (RUN / 'native').glob('*-ordinary/receipt.json') if json.loads(p.read_text()).get('exit_code') == 0)
        if not candidates:
            raise SystemExit('No completed ordinary creation exists; edit is NOT_RUN.')
        fixture = candidates[-1].parent / 'project'
    else:
        fixture = attempt / 'project'
        fixture.mkdir(parents=True, exist_ok=False)
    tool = fixture / 'tools/skill-builder'
    if args.case != 'edit':
        shutil.copytree(BUILDER, tool)
    output = fixture / '.trial-output' / stamp
    output.mkdir(parents=True)
    common = 'Synthetic disposable project. Only this project may receive task outputs. No network, installation, hooks, configuration or external writes. Do not run application scripts during discovery.\n'
    case_files = {
        'ordinary': {'notes.txt': 'Release notes are short summaries of supplied changes.\n'},
        'edit': {},
        'author-set': {},
        'review-updates': {},
        'python': {'AGENTS.md': common + 'Python service. Add a failing regression before implementation changes.\n', 'pyproject.toml': '[project]\nname="trial-service"\nversion="0.1.0"\n[tool.pytest.ini_options]\ntestpaths=["tests"]\n', 'src/service.py': 'def health():\n    return {"status": "ok"}\n', 'docs/requirements.md': 'REQ-7: Add a health endpoint returning HTTP 200 with JSON status ok.\nStorage owns persisted health history. HTTP owns response routing.\n'},
        'rust': {'AGENTS.md': common + 'Rust library. Implementation may precede regression tests.\n', 'Cargo.toml': '[package]\nname="health"\nversion="0.1.0"\nedition="2021"\n', 'src/lib.rs': 'pub fn health_status() -> bool { true }\n', 'docs/requirements.md': 'REQ-7: Add a health endpoint returning HTTP 200 with JSON status ok.\n'},
        'typescript': {'AGENTS.md': common + 'Service package owns HTTP; use service-local commands.\n', 'package.json': '{"private":true,"workspaces":["packages/*"]}', 'packages/service/package.json': '{"name":"service","scripts":{"test":"node --test"}}', 'docs/requirements.md': 'REQ-7: Add a health endpoint returning HTTP 200 with JSON status ok.\n'},
        'docs': {'AGENTS.md': common + 'Documentation-only project. Do not create application code.\n', 'docs/requirements.md': 'REQ-7: Document the health-response contract; do not create application code.\n', 'docs/api.md': 'GET /health returns HTTP 200 and JSON status ok.\n'},
    }
    files = case_files[args.case]
    if args.case != 'edit':
        files.setdefault('AGENTS.md', common)
    for relative, text in files.items():
        path = fixture / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    if args.case in ('author-set', 'review-updates'):
        # Only raw selected inputs enter the cold project, no tests or labels.
        os.environ['ADAPTIVE_TEST_ROOT'] = str(fixture)
        import test_adaptive as fixtures
        maker = fixtures.AdaptiveTests()
        maker.root, maker.sequence = fixture, 0
        proposal = maker.proposal()
        if args.case == 'author-set':
            selection = maker.selection(proposal)
            fixtures.write(fixture / 'selection.json', selection)
            task = 'Author the explicitly selected member A from ' + str(fixture / 'selection.json') + '. This current request authorizes the specified development destination and local custody work.'
        else:
            core = fixture / 'parents/original/notes-core'
            fixtures.package(core)
            parent = maker.package_ref(core)
            variant = fixture / 'skills/notes-a'
            fixtures.package(variant, 'project_variant', {'name': core.name, 'package_digest': parent['package_digest'], 'requirement_ids': ['R1', 'R2', 'R3']})
            for ident, statement in [('R2', 'Use local files.'), ('R3', 'Preserve inputs.')]:
                proposal['requirements'].append({**proposal['requirements'][0], 'id': ident, 'statement': statement})
            proposal['members'][0].update(role='project_variant', action='retain', existing_package=maker.package_ref(variant), parent_core=parent, requirement_ids=['R1', 'R2', 'R3'], lineage_delta=[{'requirement_id': x, 'disposition': 'retained', 'reason': 'Existing variant retains this behavior.', 'replacement_requirement_ids': [x]} for x in ['R1', 'R2', 'R3']])
            proposal['state'] = 'NO_CHANGE'
            fixtures.write(fixture / 'prior-proposal.json', proposal)
            current = fixture / 'parents/current/notes-core'
            shutil.copytree(core, current)
            (current / 'editorial-note.txt').write_text('Clarified explanatory wording; this file defines no additional behavior.')
            task = 'Review the existing variant at ' + str(variant) + ' against the explicitly selected current core at ' + str(current) + '. Its retained prior proposal is ' + str(fixture / 'prior-proposal.json') + '. Prepare an update-impact proposal only. Do not edit either skill.'
    elif args.case == 'edit':
        task = 'Edit the existing release-brief skill in ' + str(fixture / 'skills/release-brief') + ' to return four factual bullets instead of three. Preserve its other behavior. This request authorizes the focused edit and its necessary local custody evidence.'
    elif args.case == 'ordinary':
        task = 'Create a small skill named release-brief in ' + str(fixture / 'skills/release-brief') + ' that turns supplied release notes into three factual bullets. It should read supplied text and return the bullets in conversation. No external effects are needed. This request authorizes creation and the necessary local evidence.'
    else:
        task = 'Recommend a project-appropriate framework skill set from this project\'s instructions, source and requirements. Prepare a proposal only. The proposed development destination parent is ' + str(fixture / 'skills') + '. Use only this selected project; do not implement the application requirement.'
    prompt = 'Use $skill-builder at ' + str(tool / 'SKILL.md') + '.\n' + task + '\nOnly local files under this disposable project may be written. Do not install or change host configuration.'
    (attempt / 'prompt.txt').write_text(prompt, encoding='utf-8')
    cli = shutil.which('codex')
    command = [cli or 'codex', 'exec', '--cd', str(fixture), '--sandbox', 'workspace-write', '--skip-git-repo-check', '--json', '--output-last-message', str(output / 'final.txt'), '-']
    plan = {'case': args.case, 'command': command, 'timeout_seconds': 120, 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(), 'permitted_write_root': str(fixture), 'started_at_utc': stamp, 'host_boundary': 'Child CLI workspace-write requested; no OS isolation claim.', 'oracle': 'Frozen BAT behavior, retained outside cold prompt in implementation log and case plan.'}
    (attempt / 'plan.json').write_text(json.dumps(plan, indent=2), encoding='utf-8')
    before = {p.relative_to(fixture).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in fixture.rglob('*') if p.is_file()}
    (attempt / 'before.json').write_text(json.dumps(before, indent=2), encoding='utf-8')
    with (attempt / 'stdout.jsonl').open('wb') as stdout, (attempt / 'stderr.txt').open('wb') as stderr:
        try:
            child = subprocess.Popen(command, cwd=fixture, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr)
            try:
                child.communicate(prompt.encode(), timeout=120)
                plan.update(exit_code=child.returncode, timed_out=False)
            except subprocess.TimeoutExpired:
                subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'], capture_output=True, timeout=15)
                child.wait(timeout=10)
                plan.update(exit_code=child.returncode, timed_out=True)
        except OSError as exc:
            plan.update(exit_code=None, status='NOT_RUN', reason=str(exc))
    after = {p.relative_to(fixture).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in fixture.rglob('*') if p.is_file()}
    (attempt / 'after.json').write_text(json.dumps(after, indent=2), encoding='utf-8')
    plan['ended_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
    (attempt / 'receipt.json').write_text(json.dumps(plan, indent=2), encoding='utf-8')
    print(str(attempt))
    print(json.dumps(plan))
    print((attempt / 'stderr.txt').read_text(encoding='utf-8', errors='replace')[-4000:])
    return plan.get('exit_code') or 0


if __name__ == '__main__':
    sys.exit(main())
