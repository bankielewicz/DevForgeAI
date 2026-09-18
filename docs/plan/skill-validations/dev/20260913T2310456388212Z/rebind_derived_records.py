"""Correct a copied derived-record reference caught by records-001; preserve its old bytes."""
import json
import native_trials as n
root = n.RUN
def digest(name):
    return n.h.sha((root / name).read_bytes())
for name in ('findings.json', 'handoff.json'):
    n.save(root / 'inputs/finalization-before-rebind' / name, (root / name).read_text(encoding='utf-8'))
findings = json.loads((root / 'findings.json').read_bytes())
findings['findings'][0]['observation_refs'][0]['sha256'] = digest('input-binding-audit.json')
(root / 'findings.json').write_text(json.dumps(findings, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
with (root / 'command-log.md').open('a', encoding='utf-8') as stream:
    stream.write('\nFinal record check records-001 rejected one stale reference copied from the historical assessment to the newly identified input-binding-audit.json. Only the derived current finding reference was rebound to the already observed bytes; pre-correction findings/handoff are preserved under inputs/finalization-before-rebind/. No target, original input or historical evidence was repaired. The second record check is a distinct attempt.\n')
handoff = json.loads((root / 'handoff.json').read_bytes())
handoff['findings']['sha256'] = digest('findings.json')
(root / 'handoff.json').write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Derived reference corrected; original record attempt retained')
