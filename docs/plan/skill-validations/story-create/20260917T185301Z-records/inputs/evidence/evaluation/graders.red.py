"""Independent artifact checks; initial metadata-only implementation for TDD."""
import re
import yaml

def grade_story(text, expected):
    match=re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)',text,re.S)
    if not match:
        return ['frontmatter_missing']
    try:
        meta=yaml.safe_load(match[1])
    except yaml.YAMLError:
        return ['frontmatter_invalid']
    if not isinstance(meta,dict):
        return ['frontmatter_invalid']
    return []
