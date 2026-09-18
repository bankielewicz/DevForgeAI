"""Bounded cold CLI task runner. Inputs contain no auditor's expected answers."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import time

RUN = Path(__file__).resolve().parent
BUILDER = RUN / ('source-final04/skill-builder/SKILL.md' if len(sys.argv)>1 and sys.argv[1]=='04' else ('source-final/skill-builder/SKILL.md' if len(sys.argv) > 2 else 'source/skill-builder/SKILL.md'))
CASES = {
    'ordinary-create': ('Create a skill named concise-note that rewrites a supplied paragraph as three short bullet points, preserving facts. Save it under {project}/skills/concise-note.', {}),
    'ordinary-edit': ('Update {project}/skills/concise-note so every bullet ends with a period. Preserve the existing behavior and unrelated files.', {}),
    'propose-python': ('Recommend an adaptive skill set for this project. Use {project}/skills as the proposed development destination.', {'AGENTS.md': 'This Python project uses unittest. Production behavior changes require red then green tests. Skill authoring follows its authoring-only contract.\n', 'pyproject.toml': '[project]\nname="orders"\nversion="0.1"\n', 'docs/product.md': 'Orders stores local inventory snapshots. Storage owns snapshot retention and schema compatibility. HTTP owns REST request translation.\n'}),
    'propose-rust': ('Recommend an adaptive skill set for this project. Use {project}/skills as the proposed development destination.', {'AGENTS.md': 'This Rust project uses implementation-first prototypes followed by regression tests. No fixed phase count. Skill authoring follows its authoring-only contract.\n', 'Cargo.toml': '[package]\nname="snapshot"\nversion="0.1.0"\nedition="2021"\n', 'docs/product.md': 'A local CLI turns image metadata into an immutable catalog. No HTTP interface exists.\n'}),
    'propose-typescript': ('Recommend an adaptive skill set for this project. Use {project}/skills as the proposed development destination.', {'AGENTS.md': 'This TypeScript monorepo uses service-local tests. Inspect the relevant package before choosing a test command.\n', 'package.json': '{"private":true,"workspaces":["packages/*"]}', 'packages/web/package.json': '{"name":"web","scripts":{"test":"vitest"}}', 'docs/product.md': 'Web renders a customer catalog. A separate storage service owns catalog writes.\n', 'mystery.manifest': 'toolchain = unknown-fox-7\n'}),
    'propose-docs': ('Recommend an adaptive skill set for this project. Use {project}/skills as the proposed development destination.', {'AGENTS.md': 'This is a documentation-only project. Changes receive factual and link review. No executable product or compiler is required.\n', 'docs/product.md': 'The handbook documents municipal garden planting dates and volunteer intake. Editors own citations and source dates.\n'}),
    'partial-set': ('Propose and author the three selected skills phase-gate, gate-report, and plain-note under {project}/skills. phase-gate must perform actual compiled Rust release acceptance using this project release authority. gate-report requires phase-gate and consumes its accepted release record. plain-note independently rewrites a supplied sentence clearly. All three responsibilities and destinations are selected by this request.', {'AGENTS.md':'Development skill authoring only. No compiler or dependency installation is authorized.\n','docs/product.md':'Release acceptance must be issued by our compiled Rust release authority. This project has no release authority implementation or executable yet. Gate reports consume accepted release records. Plain text note rewriting is independent of release acceptance.\n'}),
    'propose-monorepo': ('Recommend an adaptive skill set for this project. Inspect relevant project inputs and existing skill coverage. Use {project}/skills as the proposed development destination.', {'AGENTS.md':'This monorepo has Python storage and TypeScript HTTP services. Use existing responsibility boundaries. Never execute project scripts during discovery.\n','pyproject.toml':'[project]\nname="storage"\nversion="0.1"\n','packages/http/package.json':'{"name":"http","scripts":{"test":"node test.js"}}','mystery.manifest':'required-tool = fox-unknown\n','docs/product.md':'Storage owns snapshot versioning, retention, and schema compatibility. HTTP owns REST request translation. Existing skill skills/http-owner owns HTTP API translation and response conventions. Storage lacks a skill.\n','skills/http-owner/SKILL.md':'---\nname: http-owner\ndescription: Handle HTTP request translation and response conventions.\n---\nOwn REST request translation and response contracts. Storage persistence and retention are excluded.\n','node_modules/ignored/secret.txt':'Synthetic ignored marker.\n','scripts/do-not-run.py':'from pathlib import Path\nPath("project-script-executed").write_text("unexpected")\n'}),
    'implicit-propose': ('Recommend project adaptations and a suitable skill set for this project. Use {project}/skills as the development destination.', {'docs/product.md':'A documentation repository maintains local planting guidance. No executable product is required.\n'}),
    'routing-description': ('Classify these requests against the supplied skill description. For each, say whether that skill applies and name its operation if applicable. Do not carry out the requests or load additional skill instructions. Requests: (1) Recommend a framework skill set for this project. (2) Build the selected members of proposal.json. (3) Review this variant against the changed core. (4) Install this skill into my active personal skills. (5) Run quality tests on this skill.', {}),
    'review-equivalent': ('Review the selected variant at {project}/skills/note-project against the current core at {project}/current/note-core. Its retained parent bytes are at {project}/history/note-core. Retain the comparison artifacts in this project.', {}),
    'review-removed': ('Review the selected variant at {project}/skills/note-project against the current core at {project}/current/note-core. Its retained parent bytes are at {project}/history/note-core. Retain the comparison artifacts in this project.', {}),
    'ordinary-import': ('Import the Claude skill at {project}/claude-source/brief-note into a Codex development skill named brief-note at {project}/skills/brief-note, preserving its note format and meaning.', {'claude-source/brief-note/SKILL.md':'---\nname: brief-note\ndescription: Turn a paragraph into a concise note.\n---\nUse Read to obtain the supplied local paragraph if it is a file. Return a one-sentence summary followed by two bullets. Preserve dates and names. Ask for missing paragraph text. Do not write or publish outside the requested output.\n'}),
    'negative-install': ('Install the skill at the selected entrypoint into my personal active skills.', {}),
    'negative-test-only': ('Test and validate the skill at the selected entrypoint. Do not edit it.', {}),
}

def inventory(root):
    result = []
    pending = [root]
    total = 0
    excluded = {'.git', '.trial-output', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build', '__pycache__', 'backup', 'backups', 'devforgeai_cli'}
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir(), key=lambda p: p.name):
            relative = path.relative_to(root)
            if any(p.casefold() in excluded or p.startswith('.env') for p in relative.parts):
                continue
            if relative.as_posix().endswith('.agents/devforgeai/project-binding.json') or path.name.casefold() in {'id_rsa', 'id_ed25519', 'id_dsa', 'id_ecdsa', 'id_ecdsa_sk', 'id_ed25519_sk'} or path.suffix.casefold() in {'.pem', '.key', '.pfx', '.p12', '.ppk'}:
                continue
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Refused link/reparse inventory path: '+relative.as_posix())
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
                continue
            if not stat.S_ISREG(info.st_mode):
                raise ValueError('Refused special inventory path: '+relative.as_posix())
            total += info.st_size
            if len(result) >= 2000 or total > 32 * 1024 * 1024:
                raise ValueError('Native inventory capture limit exceeded')
            with path.open('rb') as stream:
                data = stream.read(32 * 1024 * 1024 + 1)
            after = path.lstat()
            if len(data) != info.st_size or (info.st_size, info.st_mtime_ns, info.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                raise ValueError('Native inventory changed during read')
            result.append({'path': relative.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return sorted(result, key=lambda row: row['path'])

def execute(name, task, files):
    attempt_number = sys.argv[1] if len(sys.argv) > 1 else '01'
    attempt = RUN / 'native' / (name + '-' + attempt_number)
    attempt.mkdir()
    project = RUN / 'native/ordinary-create-03/project' if name == 'ordinary-edit' else attempt / 'project'
    if name != 'ordinary-edit':
        project.mkdir()
    for relative, content in files.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    if name == 'implicit-propose':
        copied = project / '.agents/skills/skill-builder'
        for row in inventory(BUILDER.parent):
            destination = copied / row['path']
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((BUILDER.parent / row['path']).read_bytes())
    if name in ('review-equivalent', 'review-removed'):
        old = project / 'history/note-core'
        current = project / 'current/note-core'
        variant = project / 'skills/note-project'
        old.mkdir(parents=True); current.mkdir(parents=True); (variant/'references').mkdir(parents=True); (variant/'assets').mkdir()
        core = '---\nname: note-core\ndescription: Write a factual note.\n---\n| ID | Requirement |\n| --- | --- |\n| R1 | Preserve facts |\n| R2 | Preserve attribution |\n| R3 | Retain uncertainty |\n'
        (old/'SKILL.md').write_text(core,encoding='utf-8')
        (current/'SKILL.md').write_text(core+'\n' if name=='review-equivalent' else core.replace('| R2 | Preserve attribution |\n',''),encoding='utf-8')
        parent_digest = hashlib.sha256(json.dumps(inventory(old),ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        descriptor={'schema_version':'adaptive-skill-v1','name':'note-project','role':'project_variant','binding_required':True,'parent_core':{'name':'note-core','package_digest':parent_digest,'requirement_ids':['R1','R2','R3']},'contract_path':'references/adaptive-contract.md','required_capabilities':['Python 3.10+'],'resource_roles':[{'path':'references/adaptive-contract.md','role':'reference','reason':'Product note contract'},{'path':'scripts/check_project_binding.py','role':'runtime','reason':'Check selected operational binding before product work'}]}
        (variant/'assets/devforgeai-skill.json').write_text(json.dumps(descriptor),encoding='utf-8')
        (variant/'SKILL.md').write_text('---\nname: note-project\ndescription: Write local product notes.\n---\nUse the [contract](references/adaptive-contract.md). [Descriptor](assets/devforgeai-skill.json) identifies parent lineage. Before product work and after resume or changed bytes, run scripts/check_project_binding.py with Python -B -X utf8 and --project-root for the selected project and --skill-root for this loaded package, passing paths as arguments. On non-MATCH, report the reason and request authorized setup; perform no product writes or downstream calls.\n',encoding='utf-8')
        (variant/'references/adaptive-contract.md').write_text('Write a local product note. Input is text; output is a factual paragraph. No external effects. R1 retained: preserve facts. R2 retained: preserve attribution. R3 retained: retain uncertainty. Missing text requires clarification. Activation: local product note requests; exclude source implementation and installation. Complete when the requested factual paragraph is returned. No downstream dependencies.\n```devforgeai-requirements\n[{"id":"R1","statement":"Preserve facts"},{"id":"R2","statement":"Preserve attribution"},{"id":"R3","statement":"Retain uncertainty"}]\n```\n',encoding='utf-8')
        (variant/'scripts').mkdir()
        (variant/'scripts/check_project_binding.py').write_bytes((BUILDER.parent/'assets/adaptive-runtime/check_project_binding.py').read_bytes())
    output = attempt / 'output'
    output.mkdir()
    selection = '' if name in ('implicit-propose','routing-description') else 'Use the selected development skill entrypoint: ' + str(BUILDER) + '\n'
    if name == 'routing-description':
        selection = next(line for line in BUILDER.read_text(encoding='utf-8').splitlines() if line.startswith('description:')) + '\n'
    prompt = selection + task.format(project=project) + '\nAll writes are authorized only inside ' + str(project) + '. Read any selected skill without modifying it. No installations, external publication, configuration edits or real operational effects are authorized.'
    (attempt / 'prompt.txt').write_text(prompt, encoding='utf-8')
    command = [shutil.which('codex'), 'exec', '--cd', str(project), '--sandbox', 'workspace-write', '--skip-git-repo-check', '--json', '--output-last-message', str(output / 'final.txt'), '-']
    metadata = {'argv': command, 'cwd': str(project), 'timeout_seconds': 120, 'started': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'before': inventory(project), 'invocation': 'implicit discovery' if name == 'implicit-propose' else 'explicit', 'retry_reason': 'Normal escalation after app-server initialization access denied' if attempt_number != '01' else None}
    (attempt / 'plan.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    start = time.monotonic()
    with (output / 'stdout.jsonl').open('wb') as stdout, (output / 'stderr.txt').open('wb') as stderr:
        child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, cwd=project)
        try:
            child.communicate(prompt.encode('utf-8'), timeout=120)
            metadata['timed_out'] = False
        except subprocess.TimeoutExpired:
            metadata['timed_out'] = True
            termination = subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'], capture_output=True, timeout=20)
            (output / 'termination.txt').write_bytes(termination.stdout + termination.stderr)
            child.wait(timeout=20)
        metadata.update({'exit_code': child.returncode, 'elapsed_seconds': time.monotonic() - start, 'ended': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'after': inventory(project)})
    (attempt / 'result.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return {'case': name, 'exit_code': metadata['exit_code'], 'timeout': metadata['timed_out'], 'files': len(metadata['after'])}

if __name__ == '__main__':
    batch = {'ordinary-edit','propose-python','propose-rust','propose-typescript','propose-docs','partial-set','propose-monorepo','implicit-propose'}
    remaining_batch = {'routing-description','review-equivalent','review-removed','ordinary-import'}
    selection = sys.argv[2] if len(sys.argv)>2 else None
    selected = {name: value for name,value in CASES.items() if selection is None or name == selection or (selection == 'required-batch' and name in batch) or (selection == 'remaining-batch' and name in remaining_batch)}
    if selection and not selected:
        raise ValueError('Unknown native case selection')
    for name in selected:
        attempt = RUN/'native'/(name+'-'+(sys.argv[1] if len(sys.argv)>1 else '01'))
        if attempt.exists():
            raise ValueError('Fresh attempt required: '+str(attempt))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(execute, name, task, files) for name, (task, files) in selected.items()]
        for future in concurrent.futures.as_completed(futures):
            print(json.dumps(future.result()), flush=True)
