import datetime, hashlib, json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parent
for cid in ['structure','installed-checker']:
    d=R/'trials'/cid;p=json.loads((d/'plan.json').read_text());start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        x=subprocess.run(p['command'],cwd=R,capture_output=True,timeout=p['timeout_seconds']);out,err,code=x.stdout,x.stderr,x.returncode;timeout=False
    except subprocess.TimeoutExpired as e:out,err,code=e.stdout or b'',e.stderr or b'',None;timeout=True
    (d/'attempt-001.stdout.txt').write_bytes(out);(d/'attempt-001.stderr.txt').write_bytes(err)
    record={'command':p['command'],'cwd':str(R),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout':timeout,'exit_code':code,'stdout_file':'attempt-001.stdout.txt','stderr_file':'attempt-001.stderr.txt','input_manifest_sha256':hashlib.sha256((R/'source-manifest.json').read_bytes()).hexdigest(),'side_effect_scope':'Only child stdout/stderr captured; final target/evaluator readback performed separately.'}
    (d/'attempt-001.json').write_text(json.dumps(record,indent=2)+'\n'); print(cid,code,out.decode('utf-8')[:120])
