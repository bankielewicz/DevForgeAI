import datetime, hashlib, json, os, pathlib, subprocess, sys, time
BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CANDIDATE = ROOT/'devforgeai/experiments/codex-worker-probe-logging'
attempt = BASE/'attempts'/sys.argv[1]
attempt.mkdir(parents=True, exist_ok=False)
argv = sys.argv[2:]
manifest = [{'path':str(p.relative_to(CANDIDATE)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(CANDIDATE.rglob('*')) if p.is_file() and 'target' not in p.parts]
(attempt/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
env = os.environ.copy()
env['CARGO_TARGET_DIR'] = str(BASE/'target')
env['CARGO_LLVM_COV_TARGET_DIR'] = str(BASE/'coverage-target')
env['WF_TEST_EVIDENCE'] = str(attempt/'fixtures')
start = time.monotonic()
receipt = {'argv':argv, 'cwd':str(CANDIDATE),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'environment_overrides':{k:env[k] for k in ['CARGO_TARGET_DIR','CARGO_LLVM_COV_TARGET_DIR','WF_TEST_EVIDENCE']}}
(attempt/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (attempt/'stdout.txt').open('wb') as out, (attempt/'stderr.txt').open('wb') as err:
    result = subprocess.run(argv,cwd=CANDIDATE,env=env,stdout=out,stderr=err)
receipt.update(exit_code=result.returncode, elapsed_seconds=time.monotonic()-start)
(attempt/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
print((attempt/'stdout.txt').read_text(errors='replace')[-7000:])
print((attempt/'stderr.txt').read_text(errors='replace')[-3000:])
sys.exit(result.returncode)
