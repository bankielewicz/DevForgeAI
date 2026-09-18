import os
if os.environ.get('COVERAGE_PROCESS_START'):
    import coverage
    coverage.process_startup()
    import atexit
    import hashlib
    import json
    from pathlib import Path
    def capture_source_identities():
        current = coverage.Coverage.current()
        if current is None:
            return
        rows = {}
        for name in current.get_data().measured_files():
            path = Path(name)
            if path.is_file():
                rows[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        folder = os.environ.get('SV_COVERAGE_IDENTITIES')
        if folder:
            Path(folder, str(os.getpid()) + '.json').write_text(json.dumps(rows), encoding='utf-8')
    atexit.register(capture_source_identities)
