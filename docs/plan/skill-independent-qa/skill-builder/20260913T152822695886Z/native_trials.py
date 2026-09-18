"""Cold explicit builder tasks; auditor labels are outside prompts."""
import json
import os
from pathlib import Path
import sys
from capture import RUN, ROOT, inventory, digest, sha
from runner import run

def main():
    case = sys.argv[1]
    project = RUN / 'native' / case
    project.mkdir(parents=True, exist_ok=False)
    (project / '.trial-output').mkdir()
    (project / 'AGENTS.md').write_text('This is a synthetic skill-authoring project. Author development skills only. Do not use skill-validator, install dependencies, or execute project code. All writes must stay in this disposable project.\n', encoding='utf-8')
    entry = ROOT / 'src/agents/skills/skill-builder/SKILL.md'
    target = project / 'development skills' / 'meeting-summary'
    prompt = f'Read and use only the development skill-builder entrypoint at {entry} and its routed builder resources. Do not use skill-validator. Create an ordinary skill named meeting-summary in {target}. The skill summarizes user-supplied meeting notes into Decisions, Actions (owner and due date when supplied), and Open questions. It must preserve uncertainty when an owner or date is absent and write no files during its own summarization task. This request authorizes creation at the supplied destination and the necessary authoring evidence inside {project}. Do not modify anything outside this disposable project. Return the authored package and manual handoff.'
    before, _ = inventory(project)
    plan = {'case': case, 'method': 'native explicit invocation', 'entrypoint': str(entry), 'input_manifest': before, 'expected': 'Package and digest-bound manual request, quality NOT_PERFORMED; no checker/test/validator process; no outside product effects', 'timeout': 120, 'write_root': str(project)}
    (RUN / (case + '-native-plan.json')).write_text(json.dumps(plan, indent=2), encoding='utf-8')
    result, out, err = run(case, ['codex', 'exec', '--cd', str(project), '--sandbox', 'workspace-write', '--skip-git-repo-check', '--ephemeral', '--json', '--output-last-message', str(project / '.trial-output/final.txt'), '-'], cwd=project, stdin=prompt, expected=plan['expected'])
    after, omissions = inventory(project)
    (RUN / (case + '-native-result.json')).write_text(json.dumps({'result': result, 'before': before, 'after': after, 'omissions': omissions}, indent=2), encoding='utf-8')
    print(json.dumps(result))
    print(err[-2500:])
    print(out[-3000:])

if __name__ == '__main__':
    main()
