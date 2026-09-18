"""Specification-derived fixtures; imports builder only as system under test."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import unittest
import uuid

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[4]
BUILDER = PROJECT / 'src/agents/skills/skill-builder'
sys.path.insert(0, str(BUILDER / 'scripts'))
import adaptive
import authoring
runtime = adaptive.runtime
PLATFORM = 'windows' if os.name == 'nt' else 'linux'
external_fixtures = os.environ.get('BUILDER_QA_FIXTURE_ROOT')
if external_fixtures:
    if os.name == 'nt' or not external_fixtures.startswith('/tmp/devforgeai-skill-builder-20260913T190357053555Z-') or '..' in Path(external_fixtures).parts:
        raise ValueError('External fixture root must be selected native Linux /tmp QA scope')
FIXTURES = Path(external_fixtures) if external_fixtures else RUN / 'fixtures' / (PLATFORM + '-02')
FIXTURES.mkdir(parents=True, exist_ok=True)

def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(compact(value))
    return {'path': str(path), 'sha256': sha(path.read_bytes())}

def package(root):
    rows = [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in root.rglob('*') if p.is_file()]
    rows.sort(key=lambda row: row['path'])
    return rows, sha(compact(rows))

class Independent(unittest.TestCase):
    def setUp(self):
        self.root = FIXTURES / self._testMethodName
        self.root.mkdir()

    def skill(self, name='note-core', role='core', parent=None, project=None):
        project = project or self.root
        root = project / '.agents/skills' / name
        root.mkdir(parents=True)
        (root / 'references').mkdir()
        (root / 'SKILL.md').write_text('---\nname: '+name+'\ndescription: Write a note.\n---\nWrite a note.\n', encoding='utf-8')
        (root / 'references/adaptive-contract.md').write_text('Own a note; input text; output text; no side effects. R1 retained.\n', encoding='utf-8')
        descriptor = {'schema_version':'adaptive-skill-v1','name':name,'role':role,'binding_required':True,'parent_core':parent,'contract_path':'references/adaptive-contract.md','required_capabilities':['Python 3.10+'],'resource_roles':[{'path':'references/adaptive-contract.md','role':'reference','reason':'Contract'}]}
        save(root / 'assets/devforgeai-skill.json', descriptor)
        return root, descriptor

    def binding(self, skill, role='core', selected=True, more=None):
        record = {'schema_version':'project-binding-v1','project_id':str(uuid.uuid4()),'project_root':str(self.root),'revision':1,'bindings':[{'name':skill.name,'package_path':'.agents/skills/'+skill.name,'package_digest':package(skill)[1],'role':role,'selected':selected}] + (more or []),'updated_at_utc':'2026-09-13T00:00:00Z'}
        path = self.root / '.agents/devforgeai/project-binding.json'
        save(path, record)
        return path

    def observe(self, skill, expected, code=1, root=None):
        before = package(self.root)[0]
        actual_code, result = runtime.observe(str(root or self.root), str(skill))
        self.assertEqual((actual_code, result['reason_code']), (code, expected), result)
        self.assertEqual(result['status'], 'MATCH' if code == 0 else ('UNAVAILABLE' if code == 2 else 'MISMATCH'))
        self.assertEqual(set(result), {'schema_version','status','reason_code','binding_sha256','package_digest','details'})
        self.assertNotIn('project_id', compact(result).decode())
        record = self.root / '.agents/devforgeai/project-binding.json'
        if record.is_file():
            try:
                self.assertNotIn(json.loads(record.read_bytes())['project_id'], compact(result).decode())
            except (ValueError, KeyError):
                pass
        self.assertEqual(before, package(self.root)[0], 'runtime wrote files')
        save(RUN / 'reports' / (PLATFORM+'-'+self._testMethodName+'.json'), {'exit_code':actual_code, 'observation':result, 'effects_unchanged':True})

    def test_binding_bound(self):
        skill, _ = self.skill(); self.binding(skill); self.observe(skill, 'BOUND', 0)

    def test_binding_missing(self):
        skill, _ = self.skill(); self.observe(skill, 'MISSING_BINDING')

    def test_binding_wrong_root(self):
        skill, _ = self.skill(); path = self.binding(skill); value=json.loads(path.read_bytes()); value['project_root']=str(self.root.parent); save(path,value); self.observe(skill,'ROOT_MISMATCH')

    def test_binding_unbound(self):
        skill, _=self.skill(); other,_=self.skill('other-core'); self.binding(other); self.observe(skill,'UNBOUND_SKILL')

    def test_binding_changed(self):
        skill,_=self.skill(); self.binding(skill); (skill/'extra.txt').write_text('changed'); self.observe(skill,'PACKAGE_CHANGED')

    def test_binding_role_mismatch(self):
        skill,_=self.skill(); self.binding(skill,role='expertise'); self.observe(skill,'ROLE_MISMATCH')

    def test_binding_inactive(self):
        skill,_=self.skill(); self.binding(skill,selected=False); self.observe(skill,'NOT_SELECTED')

    def test_binding_ambiguous(self):
        skill,_=self.skill(); other,_=self.skill('note-variant','project_variant',{'name':'note-core','package_digest':'0'*64,'requirement_ids':['R1']}); self.binding(skill,more=[{'name':other.name,'package_path':'.agents/skills/'+other.name,'package_digest':package(other)[1],'role':'project_variant','selected':True}]); self.observe(skill,'AMBIGUOUS_ROLE')

    def test_binding_duplicate(self):
        skill,_=self.skill(); path=self.binding(skill); value=json.loads(path.read_bytes()); value['bindings']*=2; save(path,value); self.observe(skill,'INVALID_BINDING')

    def test_binding_bad_descriptor(self):
        skill,desc=self.skill(); desc['extra']=True; save(skill/'assets/devforgeai-skill.json',desc); self.binding(skill); self.observe(skill,'INVALID_BINDING')

    def test_binding_missing_related_descriptor(self):
        skill,_=self.skill(); self.binding(skill,more=[{'name':'other-core','package_path':'.agents/skills/other-core','package_digest':'0'*64,'role':'core','selected':True}]); self.observe(skill,'INVALID_BINDING')

    def test_binding_secret_excluded(self):
        skill,_=self.skill(); (skill/'id_ed25519').write_text('synthetic excluded bytes'); self.binding(skill); self.observe(skill,'UNSAFE_PATH')

    def test_binding_unsafe_argument(self):
        skill,_=self.skill(); self.binding(skill); code,result=runtime.observe(str(self.root/'..'),str(skill)); self.assertEqual((code,result['reason_code']),(1,'UNSAFE_PATH'))

    def test_binding_hostile_project_path(self):
        self.root=self.root/"space é $x & (a); quote'"; self.root.mkdir(); skill,_=self.skill(); self.binding(skill); self.observe(skill,'BOUND',0)

    def test_binding_malformed_json(self):
        skill,_=self.skill(); path=self.binding(skill); path.write_text('{"schema_version":1,"schema_version":2}'); self.observe(skill,'INVALID_BINDING')

    def test_binding_2000_boundary(self):
        skill,_=self.skill()
        for i in range(1997): (skill/('file'+str(i))).write_bytes(b'')
        self.binding(skill); self.observe(skill,'BOUND',0)

    def test_binding_2001_limit(self):
        skill,_=self.skill()
        for i in range(1998): (skill/('file'+str(i))).write_bytes(b'')
        self.binding(skill); self.observe(skill,'CAPTURE_LIMIT',2)

    def test_binding_byte_boundary(self):
        skill,_=self.skill(); total=sum(p.stat().st_size for p in skill.rglob('*') if p.is_file()); (skill/'padding.bin').write_bytes(b'0'*(32*1024*1024-total)); self.binding(skill); self.observe(skill,'BOUND',0)

    def test_binding_byte_limit(self):
        skill,_=self.skill(); total=sum(p.stat().st_size for p in skill.rglob('*') if p.is_file()); (skill/'padding.bin').write_bytes(b'0'*(32*1024*1024-total+1)); self.binding(skill); self.observe(skill,'CAPTURE_LIMIT',2)

    def test_binding_cli(self):
        skill,_=self.skill(); self.binding(skill); command=[sys.executable,'-B','-X','utf8',str(BUILDER/'assets/adaptive-runtime/check_project_binding.py'),'--project-root',str(self.root),'--skill-root',str(skill)]; result=subprocess.run(command,capture_output=True,timeout=120); self.assertEqual(result.returncode,0,result.stderr); self.assertEqual(json.loads(result.stdout)['reason_code'],'BOUND'); save(RUN/'reports'/f'{PLATFORM}-binding-cli.json',{'argv':command,'exit_code':result.returncode,'stdout':result.stdout.decode(),'stderr':result.stderr.decode()})

    def test_binding_usage(self):
        result=subprocess.run([sys.executable,'-B',str(BUILDER/'assets/adaptive-runtime/check_project_binding.py')],capture_output=True,timeout=120); self.assertEqual(result.returncode,2); self.assertFalse(result.stdout); self.assertTrue(result.stderr)

    def proposal(self):
        raw=self.root/'input.txt'; raw.write_text('Write a concise local note.\n',encoding='utf-8'); ref={'path':str(raw),'sha256':sha(raw.read_bytes())}
        evidence={'schema_version':'project-evidence-v1','run_id':'case','project_root':str(self.root),'scope_roots':[str(self.root)],'inputs':[ref],'facts':[{'id':'F1','category':'domain','statement':'Local notes','basis':'observed','sources':[{'ref':ref,'start_line':1,'end_line':1}]}],'exclusions':[],'complete':True,'capabilities':[],'gaps':[]}
        proposal={'schema_version':'adaptation-proposal-v1','run_id':'case','mode':'propose','project_evidence':save(self.root/'evidence.json',evidence),'prior_proposal':None,'requirements':[{'id':'R1','origin':'source','statement':'Write a concise local note.','source_refs':[{'ref':ref,'start_line':1,'end_line':1}],'rationale':None,'verification':'Read resulting note'}],'members':[],'handoffs':[],'gaps':[],'state':'PROPOSED'}
        for ident in ('A','B','C'):
            proposal['members'].append({'id':ident,'name':'note-'+ident.lower(),'role':'core','action':'create','target_root':str(self.root/'skills'/('note-'+ident.lower())),'existing_package':None,'parent_core':None,'responsibility':'Write note '+ident,'exclusions':['Remote publication'],'triggers':['Local note '+ident],'near_misses':['Installation'],'requirement_ids':['R1'],'fact_ids':['F1'],'rationale':'Selected note','depends_on':['A'] if ident=='B' else [],'capabilities':[],'lineage_delta':[]})
        return proposal,evidence,ref

    def selection(self,proposal):
        auth=self.root/'authorization.txt'; auth.write_text('Create the three selected notes at the proposed destinations.\n'); return {'schema_version':'adaptation-selection-v1','proposal':save(self.root/'proposal.json',proposal),'member_ids':['C','B','A'],'destinations':[{'member_id':m['id'],'target_root':m['target_root']} for m in proposal['members']],'authorization':{'path':str(auth),'sha256':sha(auth.read_bytes())},'permitted_effects':['Write selected skills']}

    def test_records_positive_plan(self):
        proposal,_,_=self.proposal(); selection=self.selection(proposal); reader=adaptive.Reader(); reader.record(selection); self.assertEqual(reader.selection(selection,preflight=True)[2],['A','B','C']); reader.readback()

    def test_records_cycle(self):
        proposal,_,_=self.proposal(); proposal['members'][0]['depends_on']=['B']; self.assertRaisesRegex(ValueError,'cycle',adaptive.Reader().record,proposal)

    def test_records_missing_dependency(self):
        proposal,_,_=self.proposal(); proposal['members'][0]['depends_on']=['Absent']; self.assertRaisesRegex(ValueError,'dependency',adaptive.Reader().record,proposal)

    def test_records_unresolved_requirement(self):
        proposal,_,_=self.proposal(); proposal['members'][0]['requirement_ids']=['Absent']; self.assertRaisesRegex(ValueError,'unresolved',adaptive.Reader().record,proposal)

    def test_records_wrong_locator(self):
        proposal,_,_=self.proposal(); proposal['requirements'][0]['source_refs'][0]['end_line']=3; self.assertRaisesRegex(ValueError,'locator',adaptive.Reader().record,proposal)

    def test_records_stale_reference(self):
        proposal,_,ref=self.proposal(); Path(ref['path']).write_text('changed'); self.assertRaisesRegex(ValueError,'STALE_REFERENCE',adaptive.Reader().record,proposal)

    def test_records_extra_field(self):
        proposal,_,_=self.proposal(); proposal['extra']=1; self.assertRaisesRegex(ValueError,'extra',adaptive.Reader().record,proposal)

    def test_records_unknown_version(self):
        proposal,_,_=self.proposal(); proposal['schema_version']='adaptation-proposal-v2'; self.assertRaisesRegex(ValueError,'unknown',adaptive.Reader().record,proposal)

    def test_records_occupied_target(self):
        proposal,_,_=self.proposal(); Path(proposal['members'][0]['target_root']).mkdir(parents=True); selection=self.selection(proposal); self.assertRaisesRegex(ValueError,'occupied',adaptive.Reader().selection,selection,True)

    def test_records_unavailable_capability(self):
        proposal,_,_=self.proposal(); proposal['members'][0]['capabilities']=[{'id':'rust','command':'required Rust gate','required':True,'observed':'unavailable','evidence':None,'limitation':'Not implemented'}]; selection=self.selection(proposal); self.assertRaisesRegex(ValueError,'capability',adaptive.Reader().selection,selection,True)

    def test_records_missing_selection_dependency(self):
        proposal,_,_=self.proposal(); selection=self.selection(proposal); selection['member_ids']=['B']; selection['destinations']=[selection['destinations'][1]]; self.assertRaisesRegex(ValueError,'dependency',adaptive.Reader().selection,selection,True)

    def test_records_partial_reduction(self):
        rows=[{'status':'BLOCKED','applied_paths':[]},{'status':'DEPENDENCY_BLOCKED','applied_paths':[]},{'status':'AUTHORED','applied_paths':['SKILL.md']}]; self.assertEqual(adaptive.aggregate(rows),'PARTIAL'); self.assertEqual(adaptive.aggregate(rows[:2]),'BLOCKED'); self.assertEqual(adaptive.aggregate([{'status':'RETAINED','applied_paths':[]}]),'NO_CHANGE')

    def test_records_duplicate_and_nonfinite(self):
        for raw in ('{"a":1,"a":2}','{"a":NaN}','{"a":1e999}'):
            with self.subTest(raw=raw): self.assertRaises(ValueError,runtime.strict_json,raw)

    def test_records_boolean_integer(self):
        schema={'type':'integer','minimum':1}; self.assertRaises(ValueError,adaptive.validate_shape,True,schema,schema)

    def test_parent_lf_and_crlf_inventory(self):
        for line_ending,folder in [('\n','lf'),('\r\n','crlf')]:
            root=self.root/folder; root.mkdir(); (root/'unusual.md').write_bytes(line_ending.join(['# Contract','| ID | Requirement |','| --- | --- |','| R1 | Preserve note |','| R2 | Preserve title |','| R3 | Preserve date |','']).encode()); self.assertEqual(set(adaptive.Reader().requirement_index(root)),{'R1','R2','R3'})

    def contract(self,operation='create',target=None):
        return {'schema_version':'authoring-contract-v1','run_id':'case','project_root':str(self.root),'target_root':str(target or self.root/'skills/note'),'target_name':'note','operation':operation,'authorization':'Author note in selected development directory','history_review':'no_known_history','change_paths':['SKILL.md'],'requirements':[{'origin':'user','outcome':'Write note','artifacts':['SKILL.md']}],'capabilities':[],'expected_outputs':[],'side_effects':[],'inputs':[],'known_issues':[]}

    def publish(self,contract,run_name='run'):
        contract_path=self.root/(run_name+'-contract.json'); save(contract_path,contract); run=self.root/'docs/plan/skill-authorings/note'/run_name; authoring.begin(contract_path,run); (run/'candidate/SKILL.md').write_text('---\nname: note\ndescription: Write a note.\n---\nWrite a note.\n',encoding='utf-8'); authoring.publish(run); return run

    def test_ordinary_create_manual_request(self):
        run=self.publish(self.contract()); request=json.loads((run/'validation-request.json').read_bytes()); record=json.loads((run/'authoring-record.json').read_bytes()); self.assertEqual(record['authoring_state'],'AUTHORED'); self.assertEqual(record['validation_status'],'NOT_PERFORMED'); self.assertEqual(record['testing_status'],'NOT_PERFORMED'); self.assertEqual(request['package_digest'],package(self.root/'skills/note')[1]); adaptive.Reader().legacy_ref({'path':str(run/'validation-request.json'),'sha256':sha((run/'validation-request.json').read_bytes())},'validation-request-v1')

    def test_observed_edit_preserves_unrelated(self):
        target=self.root/'skills/note'; target.mkdir(parents=True); (target/'SKILL.md').write_text('old note'); (target/'unrelated.txt').write_bytes(b'keep exact\r\n'); run=self.publish(self.contract('edit',target)); self.assertEqual((target/'unrelated.txt').read_bytes(),b'keep exact\r\n'); record=json.loads((run/'authoring-record.json').read_bytes()); self.assertEqual(record['prior_origin']['kind'],'observed')

    def test_known_corrupt_history_blocks(self):
        target=self.root/'skills/note'; target.mkdir(parents=True); (target/'SKILL.md').write_text('old'); contract=self.contract('edit',target); contract['history_review']='known history missing'; path=self.root/'contract.json'; save(path,contract); self.assertRaisesRegex(ValueError,'known history',authoring.begin,path,self.root/'docs/plan/skill-authorings/note/run'); self.assertEqual((target/'SKILL.md').read_text(),'old')

    def test_legacy_arbitrary_requirements(self):
        contract=self.contract(); contract['requirements']=[{'legacy_flexible_shape':['retained',4]}]; self.publish(contract)

    def test_legacy_closed_contract(self):
        contract=self.contract(); contract['new_adaptive_field']={}; path=self.root/'contract.json'; save(path,contract); self.assertRaisesRegex(ValueError,'extra',authoring.begin,path,self.root/'run')

    def test_missing_interpreter_child(self):
        command=[str(self.root/'absent-python'),'-B','-X','utf8','helper.py']; self.assertRaises(FileNotFoundError,subprocess.run,command,env={'PATH':''},timeout=120)

class LedgerResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs): super().__init__(*args,**kwargs); self.rows=[]
    def addSuccess(self,test): super().addSuccess(test); self.rows.append({'id':test.id(),'status':'PASS'})
    def addFailure(self,test,err): super().addFailure(test,err); self.rows.append({'id':test.id(),'status':'FAIL','detail':self._exc_info_to_string(err,test)})
    def addError(self,test,err): super().addError(test,err); self.rows.append({'id':test.id(),'status':'ERROR','detail':self._exc_info_to_string(err,test)})
    def addSkip(self,test,reason): super().addSkip(test,reason); self.rows.append({'id':test.id(),'status':'NOT_RUN','detail':reason})

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Independent)
    result=unittest.TextTestRunner(verbosity=2,resultclass=LedgerResult).run(suite)
    report_name=PLATFORM+'-independent-results'+('-native-root' if external_fixtures else '')+'.json'
    save(RUN/'reports'/report_name,{'platform':platform.platform(),'python':sys.version,'fixture_root':str(FIXTURES),'source_root':str(BUILDER),'target_digest':'ecb5f8056f18e1d9889de0c829a7e8e48a6feafe1b8f29bc09718d226eb20099','tests_run':result.testsRun,'results':result.rows})
    sys.exit(not result.wasSuccessful())
