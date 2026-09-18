from trial_support import *

raw = INPUTS/'routing-requests.jsonl'
for path in (raw, BUILDER/'SKILL.md'):
    result=command([sys.executable,'-B','-X','utf8','-c','from pathlib import Path; import sys; print(Path(sys.argv[1]).read_text(encoding="utf-8"))',path],'Read raw routing request/entrypoint bytes; corrected argument-vector read avoids prior nested string escaping error')
    assert result.returncode==0
    (EVIDENCE/('routing-source-'+path.name)).write_bytes(path.read_bytes())
print(json.dumps(dict(request_source=str(raw),request_sha256=sha(raw.read_bytes()),entrypoint_sha256=sha((BUILDER/'SKILL.md').read_bytes()),manifest_currently_observed_sha256=sha((BUILDER/'evals/build-manifest.json').read_bytes()))))
