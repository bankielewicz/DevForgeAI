"""Development evidence recorder; no acceptance authority."""
from record import ROOT, WORK, PACKAGE, CARGO, sha, capture, write
import sys

def snapshot(name):
    previous = ROOT / name
    if previous.exists():
        archive = ROOT / ('candidate-' + sha(previous) + '.json')
        if not archive.exists():
            archive.write_bytes(previous.read_bytes())
    files = [p for p in PACKAGE.rglob('*') if p.is_file() and 'target' not in p.relative_to(PACKAGE).parts]
    write(name, [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files)])

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'snapshot':
        snapshot('selected-manifest.json')
    elif mode == 'focused':
        capture(sys.argv[2], [CARGO, 'test', '--locked', '--offline', '--test', 'remediation'], timeout=180)
    elif mode == 'fmt-write':
        capture(sys.argv[2], [CARGO, 'fmt', '--all'], timeout=60)
    elif mode == 'build':
        capture(sys.argv[2], [CARGO, 'build', '--locked', '--offline', '--all-targets'], timeout=180)
