"""Run the unchanged helper suite on native Linux temporary fixtures."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import platform
import shutil
import sys
import tempfile
import time
import unittest

RUN=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RUN))

def main():
    out=RUN/'evaluation/linux-attempt-002';out.mkdir(exist_ok=False)
    temp=Path(tempfile.mkdtemp(prefix='story-create-validation-'))
    shutil.copytree(RUN/'source',temp/'source')
    cov=None
    if importlib.util.find_spec('coverage'):
        import coverage
        cov=coverage.Coverage(data_file=str(out/'coverage.data'),source=[str(RUN/'source/scripts')],branch=True)
        cov.start()
    import test_binding
    test_binding.RUN=temp
    tick=time.monotonic();stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_binding))
    (out/'unittest.txt').write_text(stream.getvalue(),encoding='utf-8')
    boundary=temp/'link-boundary';boundary.mkdir()
    (temp/'link').symlink_to(boundary,target_is_directory=True)
    link_result='UNPROVEN'
    try:test_binding.target.safe_path(temp/'link')
    except test_binding.target.BindingError as error:link_result=error.code
    # Retain link identity as data without following it; only known fixture directories are copied.
    (temp/'link').unlink()
    if cov:
        cov.stop();cov.save();cov.json_report(outfile=str(out/'coverage.json'))
    shutil.copytree(temp/'test-work',out/'fixtures')
    report={'platform':platform.platform(),'python':sys.version,'executable':sys.executable,'cwd':str(Path.cwd()),'fixture_filesystem':str(temp),'run_evidence_filesystem':str(RUN),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'symlink_result':link_result,'elapsed_seconds':time.monotonic()-tick,'coverage':'MEASURED' if cov else 'NOT_RUN','source_sha256':hashlib.sha256((RUN/'source/scripts/check_project_binding.py').read_bytes()).hexdigest(),'notes':'Linux Python and /tmp synthetic fixtures; captured source and retained reports cross /mnt/c. No repository relocation, dependency install or native Codex workflow.'}
    (out/'summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))
    return 0 if result.wasSuccessful() and link_result=='UNSAFE_PATH' else 1

if __name__=='__main__':raise SystemExit(main())
