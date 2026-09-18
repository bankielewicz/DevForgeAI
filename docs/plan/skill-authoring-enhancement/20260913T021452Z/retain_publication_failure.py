from pathlib import Path
p = Path(__file__).resolve().parent / 'candidate/skill-builder/scripts/authoring.py'
s = p.read_text(encoding='utf-8')
start = s.index("    save(run / 'delivered-manifest.json', manifest(delivered))")
end = s.index('\ndef main():',start)
tail = s[start:end].rstrip()
wrapped = '    try:\n' + '\n'.join('    '+line if line else '' for line in tail.splitlines()) + '''
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # A failed record write after destination effects must not escape as a
        # misleading no-write BLOCKED response. Preserve the observed delta in
        # a separate attempt file when possible, and always return it on stdout.
        failure = {'state': 'PARTIAL' if applied or delivered != before else 'BLOCKED',
                   'run_root': str(run), 'applied_paths': applied,
                   'delivered_manifest': manifest(delivered), 'error': str(exc)}
        try:
            save(run / 'publication-failure.json', failure)
        except (OSError, ValueError):
            failure['evidence_write_failed'] = True
        return failure

'''
p.write_text(s[:start]+wrapped+s[end:],encoding='utf-8')
