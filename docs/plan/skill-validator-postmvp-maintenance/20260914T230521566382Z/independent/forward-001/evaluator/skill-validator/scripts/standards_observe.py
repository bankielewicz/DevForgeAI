"""Supplemental read-only organization observations. All size/depth advice is advisory."""
import argparse
import json
from pathlib import Path

import observe
import text_resources


def organization(source):
    root = observe.safe_path(source)
    files, exclusions = observe.inventory(root)
    texts = {}
    for relative, path, info in files:
        if path.suffix.lower() == '.md':
            texts[relative] = observe.read_stable(path, info).decode('utf-8')
    adjacency = {path: set() for path in texts}
    for path, text in texts.items():
        for _, target, _ in text_resources.links(text)[0]:
            resolution, destination = text_resources.resolve(path, target, texts, set(texts))
            if resolution == 'resolved' and destination in adjacency:
                adjacency[path].add(destination)
    depths, cycles = {}, []
    # Iterative DFS bounds traversal even for cyclic/deep user material.
    pending = [('SKILL.md', ())] if 'SKILL.md' in texts else []
    expanded = set()
    while pending:
        node, ancestors = pending.pop()
        if node in ancestors:
            cycles.append(list(ancestors[ancestors.index(node):]) + [node])
            continue
        depths[node] = min(depths.get(node, len(ancestors)), len(ancestors))
        if node not in expanded:
            expanded.add(node)
            pending.extend((child, ancestors + (node,)) for child in sorted(adjacency[node]))
    return dict(schema_version='standards-advisory-v1', authority='NONE', excluded_boundaries=exclusions,
                entrypoint_lines=len(texts.get('SKILL.md', '').splitlines()),
                over_500_lines=len(texts.get('SKILL.md', '').splitlines()) > 500,
                reference_depths=depths, cycles=cycles,
                limitations=['Advisory graph observations, not actual loads or semantic defects.',
                             'Depths are observed traversal distances; cycles have no finite maximum depth.',
                             'Token counts require the separately selected installed tokenizer.'])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(organization(args.source), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, UnicodeError) as error:
        print(json.dumps(dict(outcome='ERROR', error=str(error))))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
