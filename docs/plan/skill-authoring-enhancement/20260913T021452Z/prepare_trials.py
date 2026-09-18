from pathlib import Path
import json
import shutil
RUN = Path(__file__).resolve().parent
root = RUN / 'independent-trials'
root.mkdir()
for name in ('conversation','observed-edit','validator-intake'):
    case = root / name
    case.mkdir()
    (case / 'project').mkdir()
    shutil.copytree(RUN / 'candidate/skill-builder', case / 'skill-builder')
    shutil.copytree(RUN / 'candidate/skill-validator', case / 'skill-validator')
case = root / 'conversation'
prompt = f'''Use $skill-builder at {case / 'skill-builder/SKILL.md'}.
Create a skill named meeting-brief that turns meeting notes supplied in the conversation into a concise summary and a list of action items. Each action should include its owner only when the notes identify one. When no actions are present, say so. It needs no scripts or external services. Project root: {case / 'project'}. Save the development skill under the parent folder {case / 'project/Draft skills'}.
You may write only inside {case / 'project'} and save your final response to {case / 'response.md'}. Do not install anything or contact external services. Complete the requested workflow and retain its artifacts. Record tool commands and outcomes in {case / 'trace.md'}.
'''
(case / 'prompt.txt').write_text(prompt)
(case / 'plan.json').write_text(json.dumps({'case_ids':['AC-01','AC-03','AC-09','AC-10','AC-13'],'expected':'Conversation contract, selected portable destination, small useful package, unperformed quality, manual request; no checker/test/validator execution','executor':'independent Codex agent','timeout_seconds':600,'input':'skill-builder snapshot and prompt.txt','permitted_write_root':str(case / 'project')},indent=2))
case = root / 'observed-edit'
target = case / 'project/Development skills/daily-brief'
(target / 'agents').mkdir(parents=True)
(target / 'references').mkdir()
(target / 'SKILL.md').write_text('---\nname: daily-brief\ndescription: Summarize supplied daily notes into decisions and open questions.\nmetadata:\n  maintainer: internal-team\n---\n\n# Daily Brief\n\nUse only supplied notes. Return decisions, then open questions. For repeated meeting series, use [series conventions](references/series.md).\n')
(target / 'references/series.md').write_bytes(b'# Series conventions\r\n\r\nPreserve the meeting identifier exactly as supplied.\r\n')
(target / 'agents/openai.yaml').write_text('interface:\n  display_name: "Daily Brief"\n  short_description: "Summarize decisions and open questions"\n  brand_color: "#334455"\npolicy:\n  allow_implicit_invocation: false\ndependencies:\n  tools: []\n')
prompt = f'''Use $skill-builder at {case / 'skill-builder/SKILL.md'}.
In project {case / 'project'}, update the existing development skill {target}. Add the instruction that when notes disagree, the summary must show both statements without deciding which one is correct. Also change its UI display name to "Daily Notes Brief". Preserve its other behavior, metadata and resources. I have no previous builder records for this skill.
You may write only inside {case / 'project'} and save your final response to {case / 'response.md'}. Do not install anything or contact external services. Complete the requested workflow and retain artifacts. Record tool commands and outcomes in {case / 'trace.md'}.
'''
(case / 'prompt.txt').write_text(prompt)
(case / 'plan.json').write_text(json.dumps({'case_ids':['AC-05','AC-08','AC-10'],'expected':'Captured observed history, narrow edits only, unrelated bytes/metadata preserved, no adoption or quality execution','executor':'independent Codex agent','timeout_seconds':600,'input':'skill-builder snapshot, project, prompt.txt','permitted_write_root':str(case / 'project')},indent=2))
shutil.copytree(target, case / 'input-target')
print(root)
