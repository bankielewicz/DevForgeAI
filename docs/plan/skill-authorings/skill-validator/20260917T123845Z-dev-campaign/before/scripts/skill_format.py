"""Shared Agent Skills format observations for Claude Code targets.

Required rows carry only constraints both the Agent Skills specification and the
Claude Code skills reference state. Where the two sources diverge, the stricter
portable rule stays required only when Claude Code also rejects it; otherwise the
divergence is reported through advisory_checks so a legal Claude Code package is
not failed against a specification it does not claim.
"""
import re

# Claude Code reads all host metadata from this frontmatter; there is no separate
# configuration file. Values are the accepted YAML shapes after a safe load.
STRING_FIELDS = ('license', 'compatibility', 'model', 'effort', 'context', 'agent',
                 'shell', 'argument-hint', 'when_to_use')
LIST_OR_STRING_FIELDS = ('allowed-tools', 'disallowed-tools', 'paths', 'arguments')
MAPPING_FIELDS = ('metadata', 'hooks')
BOOLEAN_FIELDS = ('disable-model-invocation', 'user-invocable', 'background')
SUPPORTED_FIELDS = (('name', 'description') + STRING_FIELDS + LIST_OR_STRING_FIELDS
                    + MAPPING_FIELDS + BOOLEAN_FIELDS)

EFFORT_VALUES = ('low', 'medium', 'high', 'xhigh', 'max')
SHELL_VALUES = ('bash', 'powershell')
CONTEXT_VALUES = ('fork',)
# Documented spellings in addition to YAML's own true/false, which a safe load has
# already turned into bool. An unquoted 1 or 0 arrives as int.
BOOLEAN_WORDS = ('yes', 'no', 'on', 'off', '1', '0', 'true', 'false')
# Claude Code truncates description (with when_to_use) in the skill listing here.
LISTING_CAP = 1536
RESERVED_NAME_WORDS = ('anthropic', 'claude')


def yaml_mapping(text):
    import yaml
    class UniqueLoader(yaml.SafeLoader):
        pass
    def mapping(loader, node, deep=False):
        loader.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError('YAML mapping keys must be strings')
            if key in result:
                raise ValueError('duplicate YAML key: ' + key)
            result[key] = loader.construct_object(value_node, deep=deep)
        return result
    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    try:
        result = yaml.load(text, Loader=UniqueLoader)
    except (yaml.YAMLError, TypeError, RecursionError) as error:
        raise ValueError('Invalid YAML mapping: ' + str(error)) from error
    if type(result) is not dict:
        raise ValueError('YAML must be a mapping')
    return result


def string_list(value):
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) for item in value)


def boolean_value(value):
    if type(value) is bool:
        return True
    if type(value) is int:
        return value in (0, 1)
    return isinstance(value, str) and value.strip().lower() in BOOLEAN_WORDS


def metadata_checks(metadata):
    """Return stable (ID, boolean, explanation) rows both selected sources support."""
    name, description = metadata.get('name'), metadata.get('description')
    rows = [('name', isinstance(name, str) and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)) and len(name) <= 64,
             'name: 1-64 lowercase letters/digits with single separating hyphens'),
            ('description', isinstance(description, str) and bool(description.strip()) and len(description) <= 1024,
             'description: nonempty string of at most 1024 characters')]
    for key in STRING_FIELDS:
        if key in metadata:
            rows.append(('metadata_' + key, isinstance(metadata[key], str), 'optional field has supported type'))
    for key in LIST_OR_STRING_FIELDS:
        if key in metadata:
            value = metadata[key]
            rows.append(('metadata_' + key, isinstance(value, str) or string_list(value),
                         'optional field is a string or a nonempty list of strings'))
    for key in MAPPING_FIELDS:
        if key in metadata:
            rows.append(('metadata_' + key, isinstance(metadata[key], dict), 'optional field has supported type'))
    for key in BOOLEAN_FIELDS:
        if key in metadata:
            rows.append(('metadata_' + key, boolean_value(metadata[key]),
                         'optional boolean accepts true/false, yes/no, on/off and 1/0 in any case'))
    if isinstance(metadata.get('compatibility'), str):
        rows.append(('compatibility_length', 1 <= len(metadata['compatibility']) <= 500, 'compatibility 1-500 characters'))
    if isinstance(metadata.get('metadata'), dict):
        rows.append(('metadata_values', all(isinstance(k, str) and isinstance(v, str) for k, v in metadata['metadata'].items()), 'metadata maps string keys to string values'))
    for key, values in (('effort', EFFORT_VALUES), ('shell', SHELL_VALUES), ('context', CONTEXT_VALUES)):
        if isinstance(metadata.get(key), str):
            rows.append((key + '_value', metadata[key] in values, key + ': one of ' + ', '.join(values)))
    if isinstance(metadata.get('agent'), str) and 'context' in metadata:
        rows.append(('agent_requires_fork', metadata.get('context') == 'fork', 'agent selects a subagent type only with context: fork'))
    return rows


def advisory_checks(metadata):
    """Recorded source divergences. Never required: a failing row is not a defect.

    These exist because the two official sources disagree. Promoting one of them to
    a required rule would fail packages the other source calls valid, which is the
    failure mode rules.md forbids.
    """
    rows = []
    if isinstance(metadata.get('allowed-tools'), list) or isinstance(metadata.get('disallowed-tools'), list):
        rows.append(('portable_tool_list', False,
                     'Claude Code accepts a YAML list; the Agent Skills specification defines only a '
                     'space-separated string, so the list form is not portable to other hosts.'))
    description = metadata.get('description')
    when_to_use = metadata.get('when_to_use', '')
    if isinstance(description, str) and isinstance(when_to_use, str) and len(description) + len(when_to_use) > LISTING_CAP:
        rows.append(('description_listing_cap', False,
                     'description plus when_to_use exceeds the ' + str(LISTING_CAP) +
                     '-character Claude Code skill-listing truncation point.'))
    name = metadata.get('name')
    if isinstance(name, str):
        hit = [word for word in RESERVED_NAME_WORDS if word in name.lower()]
        if hit:
            rows.append(('name_reserved_word', False,
                         'the Anthropic authoring guidance prohibits the reserved words ' +
                         ', '.join(RESERVED_NAME_WORDS) + ' in name; the Claude Code reference states no such rule: ' +
                         ', '.join(hit)))
    for key in ('name', 'description'):
        value = metadata.get(key)
        if isinstance(value, str) and re.search(r'</?[A-Za-z][\w-]*[^<>]*>', value):
            rows.append((key + '_xml_tags', False,
                         'the Anthropic authoring guidance prohibits XML tags in ' + key +
                         '; the Claude Code reference states no such rule.'))
    return rows


def frontmatter(text):
    match = re.match(r'\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError('frontmatter delimiters/leading BOM')
    metadata = yaml_mapping(match[1])
    errors = [message for _, passed, message in metadata_checks(metadata) if not passed]
    if errors:
        raise ValueError('; '.join(errors))
    return metadata
