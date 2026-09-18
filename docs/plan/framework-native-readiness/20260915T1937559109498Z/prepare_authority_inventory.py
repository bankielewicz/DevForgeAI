"""Bind existing QA inputs for future Rust policy development; no acceptance decision."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=Path('C:/Projects/DevForgeAI')
QA=WORK/'docs/plan/framework-worker-qa/20260915T1901023951559Z-retest'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(QA/'handoff-manifest.json')
assert sha(QA/'handoff-manifest.json')=='c216960995b9fc599b05d19d62704948ce1794b046ad9af4d73e7d0141050e01'
assert all(sha(Path(v['actual_path']))==v['sha256'] for v in manifest.values())
tests=read(QA/'test-inventory.json');assert len({t['name'] for t in tests})==len(tests)==50
source=read(QA/'source-denominator.json')
candidate=read(QA/'selected-manifest.json')
base=WORK/'devforgeai/experiments/codex-worker-probe'
out={'schema_version':1,'status':'PROPOSED_POLICY_INVENTORY_NOT_INSTALLED','policy_id':'worker-windows-offline-v1','scope_id':'worker-windows-offline-v1','required_platforms':['windows-x86_64'],'accepted_provenance_modes':['operator_attested_import'],'coverage_floor_basis_points':9500,'case_floor_basis_points':9500,'candidate_manifest_sha256':sha(QA/'selected-manifest.json'),'reference_evidence_manifest_sha256':sha(QA/'handoff-manifest.json'),'candidate_files':[{'path':str(Path(c['path']).relative_to(base)).replace('\\','/'),'sha256':c['sha256']} for c in candidate],'source_files':[{'path':str(Path(c['path']).relative_to(base)).replace('\\','/'),'sha256':c['sha256'],'zero_executable':Path(c['path']).name=='lib.rs'} for c in source['files']],'tests':[{'name':t['name'],'category':t['category'],'level':t['level']} for t in tests],'required_cases':[{'case_id':c['id'],'mandatory':True,'platform':'windows-x86_64','oracle_id':'worker-offline-qa-v1:'+c['id']} for c in read(QA/'cases.json')],'reference_artifacts':[{'artifact_id':'a'+str(i).zfill(5),'origin_relative_path':k,'sha256':v['sha256'],'bytes':v['bytes']} for i,(k,v) in enumerate(sorted(manifest.items()),1)],'required_reference_artifact_count':len(manifest),'operator_judgments_required':['ffi_ownership_review','test_integrity_review','mandatory_subfixtures_complete','independent_qa_review','unresolved_defects'],'native_cases_selected':False}
(ROOT/'authority-worker-inventory.proposed.json').write_text(json.dumps(out,indent=2)+'\n')
(ROOT/'operator-selection.json').write_text(json.dumps({'selection':'operator_attested_import','source':'Explicit user reply in this conversation: Operator-attested evidence first (Recommended)','selected_at_date':'2026-09-15','service_installation_authorized':False,'operator_account_provisioned':False},indent=2)+'\n')
print(json.dumps({'candidate_files':len(candidate),'source_files':len(source['files']),'tests':len(tests),'groups':len(out['required_cases']),'reference_artifacts':len(manifest),'reference_bytes':sum(v['bytes'] for v in manifest.values())}))
