"""Read back emitted evaluator measurements without changing their original inputs."""
import datetime, json, pathlib
import trial

root=trial.ROOT
index=json.loads((root/'evaluation-index.json').read_text())
retained_names={'adopt-01':'adopt-01-published','revision-01-conflict':'revision-01-conflict','revision-02-resolved':'revision-02-resolved-successful','later-revision-03':'later-revision-03-successful'}
commands=[(p,json.loads(p.read_text())) for p in (root/'commands').glob('*.json')]
audits=[];missing=[];total_candidates=0;total_cases=0;mappings=[]
for entry in index['files']:
    original_result=pathlib.Path(entry['path']);original_run=original_result.parent
    retained_run=root/'retained'/retained_names[original_run.name]
    retained_result=retained_run/original_result.name
    result_hash=trial.digest(retained_result)
    assert result_hash==entry['sha256']
    matches=[]
    for command_path,command in commands:
        args=command['argv']
        if '--output' in args and pathlib.Path(args[args.index('--output')+1])==original_result:
            matches.append((command_path,command))
    assert len(matches)==1,(str(original_result),len(matches))
    command_path,command=matches[0];args=command['argv']
    original_candidate=pathlib.Path(args[args.index('--candidate-root')+1])
    original_cases=pathlib.Path(args[args.index('--cases')+1])
    retained_candidate=retained_run/original_candidate.relative_to(original_run)
    retained_cases=retained_run/original_cases.relative_to(original_run)
    emitted=[json.loads(line) for line in retained_result.read_text().splitlines()]
    row_audits=[];measured_union=set()
    for row in emitted:
        actual_case_digest=trial.digest(retained_cases)
        case_check={'emitted_cases_sha256':row['cases_sha256'],'actual_retained_sha256':actual_case_digest,'original_locator':str(original_cases),'retained_locator':str(retained_cases),'passed':actual_case_digest==row['cases_sha256']}
        total_cases+=1
        if not case_check['passed']: missing.append(case_check)
        candidate_checks=[]
        for relative,expected_hash in row['candidate_digests'].items():
            measured_union.add(relative);total_candidates+=1
            selected=retained_candidate/relative
            actual=trial.digest(selected) if selected.is_file() else None
            check={'emitted_locator':relative,'emitted_sha256':expected_hash,'original_absolute_locator':str(original_candidate/relative),'retained_same_locator':str(selected),'same_locator_actual_sha256':actual,'readback_locator':str(selected),'mapping':None}
            if actual!=expected_hash:
                eligible=original_result.name=='delivered-results.jsonl' and relative==original_run.name+'/evidence/revision-plan.json'
                prior=selected.with_name('revision-plan-before-publication.json')
                prior_hash=trial.digest(prior) if eligible and prior.is_file() else None
                if eligible and prior_hash==expected_hash:
                    mapping={'from_emitted_locator':relative,'to_retained_relative_locator':prior.relative_to(retained_candidate).as_posix(),'retained_absolute_locator':str(prior),'sha256':prior_hash,'basis':'The executed driver copied the actual APPLIED plan bytes immediately before replacing the plan for pointer advancement. This retained byte copy exactly matches the emitted delivered-evaluation digest.'}
                    check.update(readback_locator=str(prior),mapping=mapping)
                    actual=prior_hash;mappings.append({'result_file':str(retained_result),'case_id':row['case_id'],**mapping})
            check['readback_sha256']=actual
            check['passed']=actual==expected_hash
            if not check['passed']:missing.append(check)
            candidate_checks.append(check)
        row_audits.append({'case_id':row['case_id'],'grader_id':row['grader_id'],'cases':case_check,'candidate_measurements':candidate_checks,'passed':case_check['passed'] and all(x['passed'] for x in candidate_checks)})
    current_files={p.relative_to(retained_candidate).as_posix():trial.digest(p) for p in retained_candidate.rglob('*') if p.is_file()}
    extra_files=[]
    known_post=set()
    if original_result.name=='evaluation-results.jsonl' and original_run.name=='adopt-01':
        known_post={'adoption/evidence/published-origin.json'}
    elif original_result.name=='delivered-results.jsonl':
        known_post={original_run.name+'/evidence/published-origin.json',original_run.name+'/evidence/revision-plan-before-publication.json'}
    for relative in sorted(set(current_files)-measured_union):
        extra_files.append({'path':relative,'sha256':current_files[relative],'classification':'CREATED_AFTER_EVALUATION_BY_RECORDED_PUBLICATION_SEQUENCE' if relative in known_post else 'PRESENT_BUT_NOT_IN_THIS_RESULT_FILE_MEASURED_INPUT_SET','chronology_basis':'executed driver publication order' if relative in known_post else 'No chronology claim; membership only.'})
    audits.append({'original_result':str(original_result),'retained_result':str(retained_result),'result_sha256':result_hash,'command_receipt':str(command_path),'command_receipt_sha256':trial.digest(command_path),'original_candidate_root':str(original_candidate),'retained_candidate_root':str(retained_candidate),'measured_union_count':len(measured_union),'current_retained_root_file_count':len(current_files),'unmeasured_current_files':extra_files,'records':row_audits,'passed':all(x['passed'] for x in row_audits)})
audit={'schema_version':'1','audited_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Every cases_sha256 and every candidate_digests entry emitted by the 19 records in the eight indexed final-chain evaluator result files, read against retained bytes. Measurements are not expanded to all files later present in a reused root.','result_files':audits,'summary':{'result_file_count':len(audits),'record_count':total_cases,'cases_digest_checks':total_cases,'candidate_digest_checks':total_candidates,'mapped_measurement_count':len(mappings),'distinct_mapped_retained_files':len({x['retained_absolute_locator'] for x in mappings}),'unavailable_or_mismatched_count':len(missing),'passed':not missing},'explicit_locator_mappings':mappings,'unavailable_or_mismatched':missing,'mutations':'This audit reads original result/input files and writes new audit artifacts only. No measured bytes or paths are replaced.'}
trial.write(root/'measured-input-readback-audit.json',audit)
print(json.dumps(audit['summary'],indent=2))
if missing:
    print(json.dumps(missing,indent=2))
    raise SystemExit(1)
