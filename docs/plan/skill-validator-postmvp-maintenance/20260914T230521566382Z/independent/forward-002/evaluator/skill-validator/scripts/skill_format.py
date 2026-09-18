"""Shared Agent Skills format observations; host compatibility remains separate."""
import re


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


def metadata_checks(metadata):
    """Return stable (ID, boolean, explanation) rows for the selected ASCII profile."""
    name, description = metadata.get('name'), metadata.get('description')
    rows = [('name', isinstance(name, str) and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)) and len(name) <= 64,
             'name: 1-64 lowercase letters/digits with single separating hyphens'),
            ('description', isinstance(description, str) and bool(description.strip()) and len(description) <= 1024,
             'description: nonempty string of at most 1024 characters')]
    types = {'license': str, 'compatibility': str, 'metadata': dict, 'allowed-tools': str}
    for key, expected in types.items():
        if key in metadata:
            rows.append(('metadata_' + key, isinstance(metadata[key], expected), 'optional field has supported type'))
    if isinstance(metadata.get('compatibility'), str):
        rows.append(('compatibility_length', 1 <= len(metadata['compatibility']) <= 500, 'compatibility 1-500 characters'))
    if isinstance(metadata.get('metadata'), dict):
        rows.append(('metadata_values', all(isinstance(k, str) and isinstance(v, str) for k, v in metadata['metadata'].items()), 'metadata maps string keys to string values'))
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
