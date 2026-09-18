"""Local schema checks for shipped authoring/adaptive records; no quality verdicts.

Supports the vocabulary used by these schemas, not arbitrary external schemas.
Reference loading is supplied by the caller and never accesses the network.
"""
import json
import re


def need(condition, message):
    if not condition:
        raise ValueError(message)


def validate(value, schema, document=None, location='$', resolve=None):
    document = schema if document is None else document
    if '$ref' in schema:
        reference = schema['$ref']
        if not reference.startswith('#/$defs/'):
            need(resolve is not None, 'unsupported schema reference')
            document, reference = resolve(reference)
        need(reference.startswith('#/$defs/'), 'unsupported schema reference')
        validate(value, document['$defs'][reference[8:]], document, location, resolve)
    if 'anyOf' in schema:
        for option in schema['anyOf']:
            try:
                validate(value, option, document, location, resolve)
                break
            except ValueError:
                pass
        else:
            raise ValueError(location + ': no supported type alternative')
    if 'const' in schema:
        need(type(value) is type(schema['const']) and value == schema['const'], location + ': wrong constant/version')
    if 'enum' in schema:
        need(any(type(value) is type(item) and value == item for item in schema['enum']), location + ': unknown enum')
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool, 'null': type(None)}
    if kind:
        need(kind in types and type(value) is types[kind], location + ': wrong type')
    if isinstance(value, dict):
        properties = schema.get('properties', {})
        need(set(schema.get('required', [])) <= set(value), location + ': missing fields')
        for key, child in value.items():
            if key in properties:
                validate(child, properties[key], document, location + '.' + key, resolve)
            else:
                extra = schema.get('additionalProperties', True)
                need(extra is not False, location + ': extra field ' + key)
                if isinstance(extra, dict):
                    validate(child, extra, document, location + '.' + key, resolve)
    elif isinstance(value, list):
        need(len(value) >= schema.get('minItems', 0), location + ': too few items')
        if schema.get('uniqueItems'):
            encoded = [json.dumps(item, sort_keys=True, ensure_ascii=False, allow_nan=False) for item in value]
            need(len(set(encoded)) == len(value), location + ': duplicate items')
        for index, child in enumerate(value):
            validate(child, schema.get('items', {}), document, location + '[' + str(index) + ']', resolve)
    elif isinstance(value, str):
        need(schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', len(value)), location + ': invalid length')
        if 'pattern' in schema:
            need(re.fullmatch(schema['pattern'], value) is not None, location + ': invalid string')
    elif type(value) is int:
        need(value >= schema.get('minimum', value), location + ': integer below minimum')
