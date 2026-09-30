"""Generate the mechanical Codex adaptation of the approved 29 PRD cases.

No fixture rewriting or behavioral-rubric changes. Run with --check for drift.
The original files stay under src/claude/DevForgeAI/evals/prd.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE.parents[1] / 'claude/DevForgeAI/evals/prd'
DESTINATION = PACKAGE / 'evals/prd'

def adapt(relative, data):
    if relative.name == 'scaffold.sh' or relative.name == 'case.yaml':
        return data
    text = data.decode('utf-8')
    if relative.as_posix() == 'records-provenance/graders/model-is-a-claude-model-id.md':
        # A Claude model-family regex cannot verify Codex identity. Compare the
        # authored value with native thread/start metadata; never inject it.
        return b'---\ntype: codex_runtime_identity\nfield: model\ntarget: docs/specs/prd/PRD-001.md\n---\n'
    if relative.name == 'prompt.md':
        # Claude tool allow-list is runner metadata, never part of the task prompt.
        text = re.sub(r'^allowed_tools:.*\n', '', text, flags=re.M)
        if relative.parts[0] == 'policy-bad-date':
            text = text.replace('name the file and the field.', 'name the file, the field and the schema rule.')
    elif relative.parent.name == 'graders':
        if 'type: tool_used\n' in text:
            # Codex has no Claude Skill call. Preserve min/max and arm semantics.
            text = text.replace('type: tool_used\n', 'type: codex_skill_read\n')
            text = text.replace('tool: Skill\n', 'skill: prd\n')
            text = re.sub(r'^input_match:.*\n', '', text, flags=re.M)
        elif 'type: regex\n' in text:
            text = text.replace('/devforgeai:', r'\$devforgeai:')
        else:
            text = text.replace('/devforgeai:', '$devforgeai:')
        if relative.parts[0] == 'records-provenance':
            text = text.replace('claude-code', 'codex')
        elif relative.as_posix() == 'extension-keeps-review-history/graders/new-row-unreviewed.md':
            # New authoring row only; historical Claude rows/authors stay unchanged.
            text = text.replace('claude-code', 'codex')
        if relative.as_posix() == 'policy-bad-date/graders/names-field.md':
            # SPEC-002 ERR-08 and issue 15 require the schema label, too.
            text = text.replace(r'\bupdated\b', r'(?s)(?=.*\bupdated\b)(?=.*\bschema\b)')
    return text.encode('utf-8')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    mapping = []
    for source in sorted(SOURCE.rglob('*')):
        if not source.is_file():
            continue
        if source.is_symlink():
            raise ValueError(f'Symlink source: {source}')
        relative = source.relative_to(SOURCE)
        original = source.read_bytes()
        adapted = adapt(relative, original)
        target = DESTINATION / relative
        if args.check:
            if not target.is_file() or target.read_bytes() != adapted:
                raise ValueError(f'Generated file drift: {relative}')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(adapted)
            target.chmod(source.stat().st_mode & 0o777)
        mapping.append({'path': relative.as_posix(),
                        'source_sha256': hashlib.sha256(original).hexdigest(),
                        'adapted_sha256': hashlib.sha256(adapted).hexdigest(),
                        'changed': original != adapted})
    path = DESTINATION / 'provider-mapping.json'
    expected = json.dumps(mapping, indent=2) + '\n'
    if args.check:
        assert path.read_text() == expected, 'Provider mapping drift'
    else:
        path.write_text(expected)
    print(f'{len(mapping)} evaluation files verified; {sum(x["changed"] for x in mapping)} mechanical adaptations.')

if __name__ == '__main__':
    main()
