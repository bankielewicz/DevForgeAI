"""Independent mechanical artifact checks; no semantic or acceptance authority."""
import re
import yaml
import xml.etree.ElementTree as ET

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader,node,deep=False):
    result={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in result:
            raise yaml.YAMLError('duplicate key')
        result[key]=loader.construct_object(value_node,deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)

def parse_yaml(text):
    return yaml.load(text,Loader=UniqueLoader)

def collect_ids(value):
    if isinstance(value,dict):
        own={value['id']} if isinstance(value.get('id'),str) else set()
        return own.union(*(collect_ids(v) for v in value.values()))
    if isinstance(value,list):
        return set().union(*(collect_ids(v) for v in value))
    return set()

def grade_story(text, expected):
    match=re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)',text,re.S)
    if not match:
        return ['frontmatter_missing']
    try:
        meta=parse_yaml(match[1])
    except yaml.YAMLError:
        return ['frontmatter_invalid']
    if not isinstance(meta,dict):
        return ['frontmatter_invalid']
    issues=[]
    for key in expected.get('required_fields',[]):
        if key not in meta:issues.append('field_missing:'+key)
    for key in ['id','type']:
        if key in expected and meta.get(key)!=expected[key]:issues.append('metadata:'+key)
    for key,value in [('status','Backlog'),('format_version','0.1.0')]:
        if meta.get(key)!=value:issues.append('metadata:'+key)
    if type(meta.get('depends_on')) is not list:issues.append('metadata:depends_on')
    if meta.get('pr_merged') is not False:issues.append('metadata:pr_merged')
    headings=set(re.findall(r'^## (.+?)\s*$',text,re.M))
    for section in expected.get('required_sections',[]):
        if section not in headings:issues.append('section_missing:'+section)
    for literal in expected.get('required_literals',[]):
        if literal not in text:issues.append('literal_missing:'+literal)
    for section in ['Definition of Done','Acceptance Criteria Verification Checklist']:
        block=re.search(r'^## '+re.escape(section)+r'\s*$(.*?)(?=^## |\Z)',text,re.M|re.S)
        if block and re.search(r'^\s*- \[[xX]\]',block[1],re.M):issues.append('premature_completion')
    if re.search(r'<(?:Selected outcome|actual actor|capability|value|specific required behavior|project-relative path)>|STORY-NNN|YYYY-MM-DD\s*$',text,re.M):issues.append('template_placeholder')
    technical=None
    for block in re.findall(r'^```ya?ml\s*\n(.*?)^```\s*$',text,re.M|re.S):
        try:value=parse_yaml(block)
        except yaml.YAMLError:
            issues.append('yaml_block_invalid');continue
        if isinstance(value,dict) and 'technical_specification' in value:technical=value['technical_specification']
    if not isinstance(technical,dict):issues.append('technical_missing')
    elif technical.get('format_version')!='2.0':issues.append('technical_version')
    technical_ids=collect_ids(technical)
    ac_ids=[]
    for block in re.findall(r'^```xml\s*\n(.*?)^```\s*$',text,re.M|re.S):
        try:root=ET.fromstring(block)
        except ET.ParseError:
            issues.append('xml_invalid');continue
        if root.tag!='acceptance_criteria':continue
        ident=root.get('id')
        if not ident:issues.append('ac_id_missing')
        elif ident in ac_ids:issues.append('ac_duplicate:'+ident)
        ac_ids.append(ident)
        for tag in ['given','when','then']:
            node=root.find(tag)
            if node is None or not ''.join(node.itertext()).strip():issues.append('ac_empty:'+tag)
        for obligation in re.split(r'[\s,]+',root.get('implements','').strip()):
            if obligation and obligation not in technical_ids:issues.append('implements_unresolved:'+obligation)
    if not ac_ids:issues.append('ac_missing')
    return sorted(set(issues))
