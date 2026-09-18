"""Independent artifact predicates; semantic adequacy always needs separate review."""
import re
import yaml

FIELDS = {'format_version', 'brief_id', 'revision', 'updated_at_utc', 'disposition', 'supersedes'}
SECTIONS = ['Selected work and context', 'Problem and outcomes', 'Scope and exclusions',
            'Options and direction', 'Constraints and architecture questions',
            'Evidence and experiments', 'Decisions and open questions', 'Handoff',
            'Follow-up and change notes']

def grade_brief(data):
    errors = []
    text = data.decode('utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        return ['Missing YAML frontmatter']
    metadata = yaml.safe_load(match[1])
    if not isinstance(metadata, dict):
        return ['Metadata must be a mapping']
    if metadata.get('format_version') != 'brainstorm-brief-v1':
        errors.append('Wrong artifact format')
    return errors
