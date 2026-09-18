from pathlib import Path
import shutil
import hashlib
import json
RUN = Path(__file__).resolve().parent
CASE = RUN / 'operational-assessment'
CASE.mkdir()
(CASE / 'project').mkdir()
shutil.copytree(RUN / 'candidate/skill-builder', CASE / 'skill-builder')
shutil.copytree(RUN / 'inputs/operational-validator', CASE / 'operational-validator')
shutil.copy2(RUN / 'inputs/skill-builder-authoring-enhancement-spec.md', CASE / 'enhancement-spec.md')
prompt = f'''Use $skill-validator at {CASE / 'operational-validator/SKILL.md'} to assess the development package {CASE / 'skill-builder'} against {CASE / 'enhancement-spec.md'} (SHA-256 43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14).
Project root for the assessment: {CASE / 'project'}.
The selected specification is an approved two-package enhancement; assess this selected builder package's applicable requirements. Run bounded checks and inspect its scripts and workflow. You may execute synthetic disposable tests under the project docs/plan only, with no installation, external actions or target mutations. Read-only official documentation refresh is allowed. No subagents are authorized in this task. Preserve inputs, commands, outputs and limitations in the operational validator's report artifacts. Do not inspect sibling task evidence, prior conclusions or other task results. This assessment is read-only for the selected package.
Save your final response at {CASE / 'response.md'} and return paths plus evidence-backed findings. Native activation and independent model execution are separate from static/helper checks.
'''
(CASE / 'prompt.txt').write_text(prompt)
(CASE / 'plan.json').write_text(json.dumps({'executor':'independent agent following captured operational validator','expected':'Report actual conformance, defects and unperformed coverage without target edits','timeout_seconds':900,'input_paths':['prompt.txt','skill-builder','operational-validator','enhancement-spec.md'],'write_root':str(CASE / 'project')},indent=2))
print(CASE)
