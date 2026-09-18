"""Independent artifact predicates; semantic adequacy always needs separate review."""
import re
import datetime as dt
from pathlib import PurePosixPath
import yaml

FIELDS = {'format_version', 'brief_id', 'revision', 'updated_at_utc', 'disposition', 'supersedes'}
SECTIONS = ['Selected work and context', 'Problem and outcomes', 'Scope and exclusions',
            'Options and direction', 'Constraints and architecture questions',
            'Evidence and experiments', 'Decisions and open questions', 'Handoff',
            'Follow-up and change notes']

def grade_brief(data):
    errors = []
    try:
        text = data.decode('utf-8')
    except UnicodeError:
        return ['Invalid UTF-8']
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        return ['Missing YAML frontmatter']
    class UniqueLoader(yaml.SafeLoader):
        pass
    def mapping(loader,node,deep=False):
        result={}
        for key_node,value_node in node.value:
            key=loader.construct_object(key_node,deep=deep)
            if not isinstance(key,str) or key in result:
                raise ValueError('Invalid or duplicate metadata key')
            result[key]=loader.construct_object(value_node,deep=deep)
        return result
    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
    try:
        metadata = yaml.load(match[1],Loader=UniqueLoader)
    except (yaml.YAMLError,ValueError):
        return ['Malformed or duplicate metadata']
    if not isinstance(metadata, dict):
        return ['Metadata must be a mapping']
    if metadata.get('format_version') != 'brainstorm-brief-v1':
        errors.append('Wrong artifact format')
    if set(metadata) != FIELDS:
        errors.append('Metadata fields must match the six-field contract')
    ident=metadata.get('brief_id')
    if not isinstance(ident,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}',ident):
        errors.append('Invalid brief ID')
    revision=metadata.get('revision')
    if type(revision) is not int or revision < 1:
        errors.append('Invalid positive integer revision')
    stamp=metadata.get('updated_at_utc')
    if isinstance(stamp,dt.datetime):
        stamp=stamp.isoformat().replace('+00:00','Z')
    try:
        if not isinstance(stamp,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z',stamp):
            raise ValueError('UTC format')
        dt.datetime.fromisoformat(stamp.replace('Z','+00:00'))
    except ValueError:
        errors.append('Invalid RFC3339 UTC timestamp')
    if metadata.get('disposition') not in ('READY_FOR_PRD','NEEDS_INPUT','REUSE_EXISTING'):
        errors.append('Invalid disposition')
    previous=metadata.get('supersedes')
    if previous is not None and (not isinstance(previous,str) or not previous or ':' in previous or '\\' in previous or PurePosixPath(previous).is_absolute() or '..' in PurePosixPath(previous).parts):
        errors.append('Invalid project-relative supersedes')
    if type(revision) is int and ((revision==1 and previous is not None) or (revision>1 and previous is None)):
        errors.append('Revision lineage mismatch')
    body=text[match.end():]
    found=re.findall(r'^## (.+?)\s*$',body,re.M)
    if found != SECTIONS:
        errors.append('Required section sequence missing or duplicated')
    for section in SECTIONS:
        section_match=re.search(r'^## '+re.escape(section)+r'\s*\n(.*?)(?=^## |\Z)',body,re.M|re.S)
        if section_match and not section_match[1].strip():
            errors.append('Empty required section: '+section)
    if re.search(r'\{\{.*?\}\}',body,re.S):
        errors.append('Unfilled template placeholder')
    return errors
