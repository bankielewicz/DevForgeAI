from pathlib import Path
import shutil
import json
RUN = Path(__file__).resolve().parent
CASE = RUN / 'operational-revalidation'
CASE.mkdir()
(CASE / 'project').mkdir()
shutil.copytree(RUN / 'candidate/skill-builder',CASE / 'skill-builder')
prompt = f'''Use the operational skill-validator at {RUN / 'inputs/operational-validator/SKILL.md'} for a fresh linked revalidation of {CASE / 'skill-builder'} against the approved enhancement specification {RUN / 'inputs/skill-builder-authoring-enhancement-spec.md'}.
Project root: {CASE / 'project'}.
Compare the selected package with the prior assessment you produced at {RUN / 'operational-assessment/project/docs/plan/skill-validations/skill-builder/20260913-operational-001'}. Re-execute the relevant bounded cases, assess prior findings as resolved, persistent, new or unverified, and retain actual receipts. Assess metadata preservation through a realistic synthetic import if needed. Do not edit the target or read unrelated sibling task results. No installation, external writes or delegation. Retain a fresh report and exact source readback under this project's docs/plan and save the final response to {CASE / 'response.md'}.
'''
(CASE / 'prompt.txt').write_text(prompt)
(CASE / 'plan.json').write_text(json.dumps({'executor':'independent operational validator revalidation','expected':'Evidence-backed reassessment of prior findings without target edits','input_paths':['skill-builder','prompt.txt'],'timeout_seconds':900},indent=2))
print(CASE)
