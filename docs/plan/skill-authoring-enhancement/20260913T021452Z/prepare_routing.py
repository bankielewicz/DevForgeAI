from pathlib import Path
import json
import re
RUN = Path(__file__).resolve().parent
CASE = RUN / 'independent-trials/routing'
CASE.mkdir()
definitions = {}
for name in ('skill-builder','skill-validator'):
    text = (RUN / 'candidate' / name / 'SKILL.md').read_text()
    definitions[name] = text.split('---',2)[1].strip()
requests = [
('R01','Create a skill that turns my notes into action items.','skill-builder'),
('R02','Change the display name of my existing development skill.','skill-builder'),
('R03','Import this local Claude skill into a Codex development package.','skill-builder'),
('R04','Implement a skill from this Markdown specification.','skill-builder'),
('R05','Record explicit adoption of this existing development skill.','skill-builder'),
('R06','Revise this skill; there is no builder history.','skill-builder'),
('R07','Validate and test the skill from this authoring packet.','skill-validator'),
('R08','Audit this skill for ceremonial steps and missing resources.','skill-validator'),
('R09','Check whether this generated skill script handles invalid input.','skill-validator'),
('R10','Install this skill into my personal active skills folder.','neither'),
('R11','Explain what this skill does; do not change it.','neither'),
('R12','Write an enhancement specification for later review, without changing skills.','neither'),
('R13','Fix a bug in our web application.','neither'),
('R14','Assess the changes to my skill before adoption.','skill-validator')]
(CASE / 'raw-input.json').write_text(json.dumps({'descriptions':definitions,'requests':[{'id':i,'request':r} for i,r,e in requests]},indent=2))
(CASE / 'expectations.json').write_text(json.dumps({i:e for i,r,e in requests},indent=2))
prompt = f'''Read only {CASE / 'raw-input.json'}. For each request classify the best matching capability from the supplied descriptions as skill-builder, skill-validator, or neither. Use only the descriptions rather than invoking any skill. Save a JSON object mapping request IDs to classifications at {CASE / 'observed.json'}, and a brief explanation at {CASE / 'response.md'}. Do not read other files or delegate. This is classification only.
'''
(CASE / 'prompt.txt').write_text(prompt)
print(CASE)
