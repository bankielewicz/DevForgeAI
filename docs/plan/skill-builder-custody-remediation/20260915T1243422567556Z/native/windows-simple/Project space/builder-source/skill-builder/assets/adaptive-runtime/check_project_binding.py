"""Read-only portable project binding observation; Python 3.10+, standard library.

No identity is embedded, initialized, cached, or printed. This is editable local
evidence, not protected authorization. Invoke with -B -X utf8 and argument vectors.
"""
import argparse
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import uuid

sys.dont_write_bytecode = True
MAX_FILES = 2000
MAX_BYTES = 32 * 1024 * 1024
EXCLUDED = {'.git', '.agents', '.claude', '.codex', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build', '__pycache__', 'backup', 'backups', 'devforgeai_cli'}
PRIVATE_KEY_NAMES = {'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519', 'id_ecdsa_sk', 'id_ed25519_sk'}
PRIVATE_KEY_SUFFIXES = {'.pem', '.key', '.pfx', '.p12', '.ppk'}
NAME = r'[a-z0-9]+(?:-[a-z0-9]+)*'
IDENT = r'[A-Za-z0-9][A-Za-z0-9._-]*'
DIGEST = r'[0-9a-f]{64}'


class BindingError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def require(condition, code='INVALID_BINDING'):
    if not condition:
        raise BindingError(code)


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result)
            result[key] = value
        return result
    def invalid(value):
        raise BindingError('INVALID_BINDING')
    try:
        result = json.loads(data.decode('utf-8') if isinstance(data, bytes) else data,
                            object_pairs_hook=pairs, parse_constant=invalid)
        compact(result)
        return result
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise BindingError('INVALID_BINDING') from exc


def fields(value, names):
    require(isinstance(value, dict) and set(value) == set(names.split()))


def string(value, pattern=None):
    require(isinstance(value, str) and len(value) > 0)
    if pattern:
        require(re.fullmatch(pattern, value) is not None)


def name(value):
    string(value, NAME)
    require(len(value) <= 64)


def strings(value, pattern=None, minimum=0):
    require(isinstance(value, list) and len(value) >= minimum)
    for item in value:
        string(item, pattern)
    require(len(value) == len(set(value)))


def relpath(value):
    string(value)
    require(not any(c in value for c in ('\\', ':', '\0')) and not value.startswith('/')
            and all(p not in ('', '.', '..') for p in value.split('/')), 'UNSAFE_PATH')
    return value


def safe_path(value):
    raw = Path(value)
    require('\0' not in str(value) and '..' not in raw.parts, 'UNSAFE_PATH')
    path = Path(os.path.abspath(raw))
    for part in [*reversed(path.parents), path]:
        if os.path.lexists(part):
            info = part.lstat()
            require(not stat.S_ISLNK(info.st_mode) and not getattr(info, 'st_file_attributes', 0) & 0x400, 'UNSAFE_PATH')
    return path


def under(root, relative):
    path = safe_path(root / relpath(relative))
    require(path.is_relative_to(root), 'UNSAFE_PATH')
    return path


def excluded(path):
    return any(p.casefold() in EXCLUDED | PRIVATE_KEY_NAMES or 'backup' in p.casefold() or p.casefold().startswith('.env') for p in path.parts) or path.suffix.casefold() in PRIVATE_KEY_SUFFIXES | {'.pyc', '.pyo'}


class Capture:
    """One aggregate budget, stable reads, originals counted once."""
    def __init__(self):
        self.seen = {}
        self.total = 0

    def read(self, value):
        path = safe_path(value)
        before = path.stat()
        require(stat.S_ISREG(before.st_mode), 'UNSAFE_PATH')
        key = os.path.normcase(str(path))
        if key not in self.seen:
            require(len(self.seen) < MAX_FILES and self.total + before.st_size <= MAX_BYTES, 'CAPTURE_LIMIT')
        require(before.st_size <= MAX_BYTES, 'CAPTURE_LIMIT')
        with path.open('rb') as stream:
            data = stream.read(MAX_BYTES + 1)
        after = safe_path(path).stat()
        require(len(data) <= MAX_BYTES, 'CAPTURE_LIMIT')
        require((before.st_size, before.st_mtime_ns, before.st_ino) ==
                (after.st_size, after.st_mtime_ns, after.st_ino), 'PACKAGE_CHANGED')
        if key in self.seen:
            require(self.seen[key] == digest(data), 'PACKAGE_CHANGED')
        else:
            self.total += len(data)
            require(self.total <= MAX_BYTES, 'CAPTURE_LIMIT')
            self.seen[key] = digest(data)
        return data

    def inventory(self, value):
        root = safe_path(value)
        require(root.is_dir(), 'UNSAFE_PATH')
        rows, pending = [], [root]
        while pending:
            entries = sorted(pending.pop().iterdir())
            for path in entries:
                relative = path.relative_to(root)
                require(not excluded(relative), 'UNSAFE_PATH')
                safe_path(path)
                if path.is_dir():
                    pending.append(path)
                else:
                    data = self.read(path)
                    rows.append({'path': relpath(relative.as_posix()), 'bytes': len(data), 'sha256': digest(data)})
        return sorted(rows, key=lambda row: row['path'])


def descriptor(value, root=None, capture=None):
    fields(value, 'schema_version name role binding_required parent_core contract_path required_capabilities resource_roles')
    require(value['schema_version'] == 'adaptive-skill-v1' and value['binding_required'] is True)
    name(value['name'])
    require(value['role'] in ('core', 'project_variant', 'expertise'))
    require(value['contract_path'] == 'references/adaptive-contract.md')
    strings(value['required_capabilities'])
    require(any(re.search(r'Python\s*3\.10\+', item, re.I) for item in value['required_capabilities']))
    parent = value['parent_core']
    if value['role'] == 'project_variant':
        fields(parent, 'name package_digest requirement_ids')
        name(parent['name'])
        require(parent['name'] != value['name'])
        string(parent['package_digest'], DIGEST)
        strings(parent['requirement_ids'], IDENT, 1)
    else:
        require(parent is None)
    require(isinstance(value['resource_roles'], list))
    paths = []
    for row in value['resource_roles']:
        fields(row, 'path role reason')
        paths.append(relpath(row['path']))
        require(row['role'] in ('runtime', 'template', 'reference', 'fixture', 'license'))
        string(row['reason'])
    require(len(paths) == len(set(paths)))
    if root is not None:
        require(root.name == value['name'])
        for path in set(paths + [value['contract_path']]):
            require(under(root, path).is_file())
        # A conservative standard-library frontmatter identity reader. The
        # authoring reader additionally parses arbitrary supported YAML.
        text = capture.read(under(root, 'SKILL.md')).decode('utf-8')
        header = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
        require(header is not None)
        names = re.findall(r'^name:[ \t]*(.*?)[ \t]*$', header[1], re.M)
        require(len(names) == 1)
        declared = names[0].strip().split(' #', 1)[0].strip()
        require(declared in (value['name'], '"' + value['name'] + '"', "'" + value['name'] + "'"))
    return value


def binding(value):
    fields(value, 'schema_version project_id project_root revision bindings updated_at_utc')
    require(value['schema_version'] == 'project-binding-v1')
    string(value['project_id'])
    try:
        require(str(uuid.UUID(value['project_id'])) == value['project_id'])
        stamp = value['updated_at_utc']
        require(isinstance(stamp, str) and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', stamp) is not None)
        datetime.datetime.fromisoformat(stamp[:-1] + '+00:00')
    except (ValueError, TypeError, AttributeError) as exc:
        raise BindingError('INVALID_BINDING') from exc
    require(type(value['revision']) is int and value['revision'] >= 1)
    string(value['project_root'])
    require(Path(value['project_root']).is_absolute())
    require(str(safe_path(value['project_root'])) == value['project_root'])
    require(isinstance(value['bindings'], list) and len(value['bindings']) >= 1)
    names, paths = [], []
    for row in value['bindings']:
        fields(row, 'name package_path package_digest role selected')
        name(row['name'])
        require(relpath(row['package_path']) == '.agents/skills/' + row['name'])
        string(row['package_digest'], DIGEST)
        require(row['role'] in ('core', 'project_variant', 'expertise') and type(row['selected']) is bool)
        names.append(row['name'])
        paths.append(row['package_path'])
    require(len(names) == len(set(names)) and len(paths) == len(set(paths)))
    return value


def observe(project_root, skill_root):
    result = {'schema_version': 'binding-observation-v1', 'status': 'MISMATCH',
              'reason_code': 'INVALID_BINDING', 'binding_sha256': None,
              'package_digest': None, 'details': []}
    try:
        project, skill = safe_path(project_root), safe_path(skill_root)
        require(project.is_dir() and skill.is_dir(), 'UNSAFE_PATH')
        record_path = under(project, '.agents/devforgeai/project-binding.json')
        require(record_path.exists(), 'MISSING_BINDING')
        capture = Capture()
        binding_capture = Capture()
        raw = binding_capture.read(record_path)
        result['binding_sha256'] = digest(raw)
        value = binding(strict_json(raw))
        require(os.path.normcase(str(safe_path(value['project_root']))) == os.path.normcase(str(project)), 'ROOT_MISMATCH')
        descriptor_path = under(skill, 'assets/devforgeai-skill.json')
        require(descriptor_path.is_file())
        desc = descriptor(strict_json(capture.read(descriptor_path)), skill, capture)
        matches = [b for b in value['bindings'] if b['name'] == desc['name'] and under(project, b['package_path']) == skill]
        require(len(matches) == 1, 'UNBOUND_SKILL')
        selected = matches[0]
        require(selected['role'] == desc['role'], 'ROLE_MISMATCH')
        require(selected['selected'], 'NOT_SELECTED')
        rows = capture.inventory(skill)
        result['package_digest'] = digest(compact(rows))
        require(result['package_digest'] == selected['package_digest'], 'PACKAGE_CHANGED')
        groups = set()
        for item in value['bindings']:
            if not item['selected'] or item['role'] == 'expertise':
                continue
            related = under(project, item['package_path'])
            related_descriptor = under(related, 'assets/devforgeai-skill.json')
            require(related_descriptor.is_file())
            other = descriptor(strict_json(capture.read(related_descriptor)), related, capture)
            require(other['name'] == item['name'] and other['role'] == item['role'])
            group = other['parent_core']['name'] if other['role'] == 'project_variant' else other['name']
            require(group not in groups, 'AMBIGUOUS_ROLE')
            groups.add(group)
        require(binding_capture.read(record_path) == raw, 'INVALID_BINDING')
        require(capture.inventory(skill) == rows, 'PACKAGE_CHANGED')
        result.update(status='MATCH', reason_code='BOUND')
        return 0, result
    except BindingError as exc:
        code = exc.code
    except (OSError, PermissionError):
        code = 'IO_ERROR'
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError):
        code = 'INVALID_BINDING'
    result['reason_code'] = code
    unavailable = code in ('IO_ERROR', 'CAPTURE_LIMIT')
    result['status'] = 'UNAVAILABLE' if unavailable else 'MISMATCH'
    # Deliberately do not serialize exceptions, input values or source excerpts.
    return (2 if unavailable else 1), result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', required=True)
    parser.add_argument('--skill-root', required=True)
    args = parser.parse_args()
    code, result = observe(args.project_root, args.skill_root)
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
