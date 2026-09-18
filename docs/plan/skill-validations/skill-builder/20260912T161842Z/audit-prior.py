import hashlib, importlib.util, json, pathlib, sys, datetime
R=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('C:/Projects/DevForgeAI');PLAN=ROOT/'docs/plan';P=PLAN/'skill-builder-adoption-verification-20260912'
sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('obs',R/'inputs/validator/scripts/observe.py');o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
measurements=[];selected=[]
def verify(path,digest=None):
    path=o.safe_path(path);assert path.is_relative_to(PLAN) or path.is_relative_to(ROOT/'src/agents/skills/skill-builder')
    data=o.read_stable(path);actual=hashlib.sha256(data).hexdigest()
    if digest: assert actual==digest,str(path)
    measurements.append({'original_path':str(path),'sha256':actual,'bytes':len(data)})
    return data
def retain(path,data):
    dest=R/'inputs/prior-observed'/path.relative_to(PLAN);dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():dest.write_bytes(data)
    assert dest.read_bytes()==data
    selected.append(dest.relative_to(R).as_posix())
manifest=hashlib.sha256((R/'source/evals/build-manifest.json').read_bytes()).hexdigest()
summaries=[]
# Enumerate one directory at a time and audit only explicitly listed profile result/case inputs.
for d in sorted((P/'profile-checks-release').iterdir()):
    o.safe_path(d)
    if not d.is_dir():continue
    result=d/'evaluation.jsonl';cases=d/'cases.jsonl';raw=verify(result);retain(result,raw);case=verify(cases);retain(cases,case)
    retain(d/'command.json',verify(d/'command.json'))
    rows=[json.loads(l) for l in raw.splitlines()]
    for row in rows:
        assert row['build_manifest_sha256']==manifest and row['cases_sha256']==hashlib.sha256(case).hexdigest() and row['expectation_met'] is True
        for rel,digest in row['candidate_digests'].items():
            assert o.normalized_relative(rel);verify(d/'candidate'/rel,digest)
    summaries.append({'suite':d.name,'records':len(rows),'pass':sum(x['status']=='PASS' for x in rows),'expected_fail':sum(x['status']=='FAIL' for x in rows)})
# Read original immutable pre-evaluation roots identified by the retained adoption audit, never temporary roots.
a=json.loads((P.parent/'skill-builder-adoption-verification-20260912-independent-adoption-trial-final2/measured-input-readback-audit.json').read_text())
adopt_count=0
for row in a['result_files']:
    result=pathlib.Path(row['retained_result']);raw=verify(result,row['result_sha256']);retain(result,raw)
    command=pathlib.Path(row['command_receipt']);retain(command,verify(command,row['command_receipt_sha256']))
    capture=row['pre_evaluation_capture_receipt'];cases=pathlib.Path(capture['preserved_cases']);rawcase=verify(cases,capture['cases_sha256']);retain(cases,rawcase)
    candidate=pathlib.Path(row['retained_candidate_root']);o.safe_path(candidate)
    for r in [json.loads(l) for l in raw.splitlines()]:
        assert r['build_manifest_sha256']==manifest and r['cases_sha256']==hashlib.sha256(rawcase).hexdigest() and r['expectation_met'] is True
        for rel,digest in r['candidate_digests'].items():assert o.normalized_relative(rel);verify(candidate/rel,digest)
        adopt_count+=1
summary={'schema_version':'1','audited_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'builder_manifest_sha256':manifest,'profile_suites':summaries,'independent_adoption_result_files':len(a['result_files']),'independent_adoption_observations':adopt_count,'verified_measurements':len(measurements),'all_selected_hashes_match':True,'limitations':'Readback of historical executed evidence, not a new evaluator or target workflow execution. Legacy and fault reports retained as reports; their complete measured inputs were not independently replayed in this run. No self-generated/adopted builder baseline established.'}
(R/'observations/prior-evidence-readback.json').write_text(json.dumps({**summary,'measurements':measurements,'retained_result_case_command_files':sorted(set(selected))},indent=2)+'\n')
print(json.dumps(summary))
