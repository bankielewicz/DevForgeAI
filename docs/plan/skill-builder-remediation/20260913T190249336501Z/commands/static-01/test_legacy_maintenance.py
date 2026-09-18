"""Additional legacy history, evidence and scaffolding compatibility scenarios."""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import types
import unittest
from unittest.mock import patch
import test_remediation as t
import authoring
import build_evidence as build
import custody
import init_skill
import generate_openai_yaml as metadata


class LegacyMaintenance(unittest.TestCase):
    def setUp(self):
        self.folder = t.RUN/'legacy-trials'/os.environ.get('REMEDIATION_ATTEMPT','legacy-01')/self._testMethodName
        self.folder.mkdir(parents=True, exist_ok=False)

    def tearDown(self):
        t.dump(self.folder.parent/'receipts'/(self._testMethodName+'-after.json'), t.manifest(self.folder))

    def before(self):
        t.dump(self.folder.parent/'receipts'/(self._testMethodName+'-before.json'), t.manifest(self.folder))

    def history(self, count=1):
        hist, pointer = t.adopted(self.folder)
        ar = {k:v for k,v in pointer['origin'].items() if k != 'kind'}
        previous = pointer['origin']
        def relative_ref(path):
            return dict(t.ref(path), path=path.relative_to(hist).as_posix())
        for index in range(count):
            run = hist/('generated'+str(index))
            data = ('generated '+str(index)+'\n').encode()
            baseline = t.put(run/'baseline/SKILL.md', data)
            spec = hist/'spec.md'
            cp = t.put(run/'build-contract.json', {'schema_version':'1','mode':'spec_build','target_name':'sample','inputs':[dict(id='S1',path='spec.md',resolved_path=str(spec),role='spec',bytes=spec.stat().st_size,sha256=t.ref(spec)['sha256'])],'authorization':{'instruction':'Synthetic authorized revision','inputs':[{'id':'S1','sha256':t.ref(spec)['sha256']}]},'artifacts':[{'path':'SKILL.md'}]})
            ep = t.put(run/'observation.json', {'schema_version':'1','run_id':'gen'+str(index),'target_name':'sample','outputs':[{'path':'SKILL.md','sha256':t.ref(baseline)['sha256']}]})
            record = {'schema_version':'2','run_id':'gen'+str(index),'mode':'spec_build','target_name':'sample','builder_manifest_sha256':'0'*64,'contract_sha256':t.ref(cp)['sha256'],'inputs':[{'id':'S1','sha256':t.ref(spec)['sha256']}],'dependencies':[],'outputs':[{'path':'SKILL.md','sha256':t.ref(baseline)['sha256'],'ownership':'generated','baseline_path':baseline.relative_to(hist).as_posix(),'baseline_sha256':t.ref(baseline)['sha256']}],'mappings':[{'requirement_id':'R1','artifact_paths':['SKILL.md'],'evidence_ids':['E1']}],'evidence':[dict(id='E1',**relative_ref(ep))],'prior_origin':previous,'adoption_origin':ar,'result':'COMPLETE'}
            op = t.put(run/'provenance.json', record)
            previous = dict(kind='generated',**relative_ref(op))
        t.put(self.folder/'src/agents/skills/sample/SKILL.md', data)
        return hist, record, op

    def generated(self, count=1, mutation=None):
        hist, record, op = self.history(count)
        if mutation:
            mutation(record)
            t.put(op, record)
        c = t.contract(self.folder, 'edit')
        c.update(target_root=str(self.folder/'src/agents/skills/sample'), prior=t.ref(op), legacy_root=str(hist), history_review='known')
        cp = t.put(self.folder/'contract.json',c)
        before = t.manifest(hist)
        self.before()
        run = self.folder/'docs/plan/edit'
        if mutation:
            with self.assertRaises((ValueError, KeyError)):
                authoring.begin(cp,run)
            self.assertFalse(run.exists())
        else:
            self.assertEqual(authoring.begin(cp,run)['state'],'STAGED')
            self.assertEqual(authoring.publish(run)['state'],'AUTHORED')
            new = json.loads((run/'authoring-record.json').read_text())
            self.assertEqual(new['testing_status'],'NOT_PERFORMED')
            self.assertEqual(new['prior_origin']['kind'],'legacy_generated')
        self.assertEqual(t.manifest(hist),before)

    def test_generated_after_adoption(self):
        self.generated()

    def test_second_generated_after_adoption(self):
        self.generated(2)

    def test_adoption_plan(self):
        hist,pointer = t.adopted(self.folder)
        record = json.loads((hist/'adoption.json').read_text())
        t.put(hist/'request.json',{'operation':'adopt','record':record})
        args = types.SimpleNamespace(snapshot_root=str(hist),request='request.json')
        self.before()
        before = t.manifest(hist)
        code,value = build.adoption_plan(args)
        self.assertEqual((code,value['recording_state']),(0,'ADOPTED'))
        self.assertEqual(before,t.manifest(hist))
        record['authorization']['managed_manifest_sha256']='0'*64
        t.put(hist/'request.json',{'operation':'adopt','record':record})
        code,value=build.adoption_plan(args)
        self.assertEqual((code,value['status']),(1,'INVALID_EVIDENCE'))

    def revision(self, version, b, c, n, expected, owned=True, required=False):
        if version=='2':
            hist,pointer=t.adopted(self.folder)
            prior=pointer['origin']
            origin={k:v for k,v in prior.items() if k!='kind'}
            pp=t.put(hist/'pointer.json',pointer)
            extras={'prior_origin':prior,'adoption_origin':origin,'baseline_before':dict(t.ref(pp),path='pointer.json')}
        else:
            hist=self.folder/'history';hist.mkdir()
            extras={'prior_build':None,'baseline_before':None}
        for name,data in [('B',b),('C',c),('N',n),('after',c)]:
            (hist/name).mkdir()
            if data is not None:t.put(hist/name/'SKILL.md',data)
        request=dict(schema_version=version,run_id='revision',baseline='B',current='C',candidate='N',after='after',required_paths=['SKILL.md'] if required else [],owned_paths=['SKILL.md'] if owned else [],baseline_after=None,**extras)
        t.put(hist/'request.json',request)
        self.before()
        before=t.manifest(hist)
        code,value=build.revision_plan(types.SimpleNamespace(snapshot_root=str(hist),request='request.json'))
        self.assertEqual(value.get('rows',[{}])[0].get('action',value['status']),expected)
        self.assertEqual(before,t.manifest(hist))
        return code,value

    def test_revision_adopted(self):
        self.assertEqual(self.revision('2',b'baseline\n',b'baseline\n',b'new\n','USE_NEW')[0],0)

    def test_input_range(self):
        source=t.put(self.folder/'source.txt','abcdef'.encode())
        args=types.SimpleNamespace(file=str(source),id='S1',snapshot_path='source.txt',role='source',start_byte=1,end_byte=4)
        self.before()
        code,value=build.input_record(args)
        self.assertEqual(value['source_ref']['sha256'],build.sha(b'bcd'))
        args.end_byte=20
        with self.assertRaises(ValueError):build.input_record(args)
        args.id='not valid'
        with self.assertRaises(ValueError):build.input_record(args)

    def test_parsers_and_paths(self):
        self.before()
        for reader in (build.json_value,custody.strict_json,authoring.parse):
            for raw in ('{"a":1,"a":2}','NaN','1e999'):
                with self.assertRaises(ValueError):reader(raw)
            self.assertEqual(reader('{"a":1.25}'),{'a':1.25})
        for path in ('../x','a/../b','/absolute','x\\y','C:/x','backups/x'):
            with self.assertRaises(ValueError):build.relative_path(path)
            with self.assertRaises(ValueError):custody.bounded_path(self.folder,path)
        self.assertEqual(custody.bounded_path(self.folder,'.',allow_dot=True),self.folder)

    def test_scaffolding_resources(self):
        self.before()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(init_skill.parse_resources('scripts,scripts,assets,references'),['scripts','assets','references'])
            with self.assertRaises(SystemExit):init_skill.parse_resources('invalid')
            for examples in (False,True):
                parent=self.folder/str(examples)
                result=init_skill.init_skill('sample',str(parent),['scripts','assets','references'],examples,['default_prompt=Use $sample'])
                self.assertIsNotNone(result)
                self.assertEqual((result/'scripts/example.py').exists(),examples)
                self.assertIn('default_prompt',(result/'agents/openai.yaml').read_text())

    def test_metadata_errors_and_preservation(self):
        self.before()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(metadata.format_display_name('openai-api-and-github'),'OpenAI API and GitHub')
            for name in ('A','A'*55,'A'*61,'A'*80):
                self.assertTrue(25 <= len(metadata.generate_short_description(name)) <= 64)
            for override in ('bad','=value','unknown=value'):
                self.assertEqual(metadata.parse_interface_overrides([override]),(None,None))
            self.assertIsNone(metadata.read_frontmatter_name(self.folder))
            for content in (b'none',b'---\n[]\n---\n',b'---\nname: []\n---\n',b'---\nname: [\n---\n'):
                t.put(self.folder/'SKILL.md',content)
                self.assertIsNone(metadata.read_frontmatter_name(self.folder))
            t.put(self.folder/'SKILL.md',b'---\nname: sample\n---\n')
            self.assertEqual(metadata.read_frontmatter_name(self.folder),'sample')
            self.assertIsNone(metadata.write_openai_yaml(self.folder,'sample',['short_description=too short']))
            path=metadata.write_openai_yaml(self.folder,'sample',[])
            original=path.read_bytes()
            with patch.object(metadata,'read_bytes',side_effect=[original,b'concurrent']):
                with self.assertRaises(ValueError):metadata.write_openai_yaml(self.folder,'sample',['display_name=Changed'])
            self.assertEqual(path.read_bytes(),original)


for name,mutation in {
    'target':lambda r:r.update(target_name='wrong'),
    'kind':lambda r:r['prior_origin'].update(kind='unknown'),
    'adoption_digest':lambda r:r['adoption_origin'].update(sha256='0'*64),
    'contract_digest':lambda r:r.update(contract_sha256='0'*64),
    'input_digest':lambda r:r['inputs'][0].update(sha256='0'*64),
    'baseline_digest':lambda r:r['outputs'][0].update(baseline_sha256='0'*64),
    'evidence_digest':lambda r:r['evidence'][0].update(sha256='0'*64),
    'mapping':lambda r:r['mappings'][0].update(artifact_paths=['unknown']),
    'mapping_evidence':lambda r:r['mappings'][0].update(evidence_ids=['unknown']),
    'result':lambda r:r.update(result='FAILED'),
}.items():
    setattr(LegacyMaintenance,'test_generated_invalid_'+name,lambda self,m=mutation:self.generated(mutation=m))

for name,b,c,n,expected,owned,required in [
    ('unchanged',b'base',b'base',b'new','USE_NEW',True,False),
    ('already_new',b'base',b'new',b'new','KEEP_CURRENT',True,False),
    ('keep_user',b'base',b'user',b'base','KEEP_CURRENT',True,False),
    ('conflict',b'base',b'user',b'new','CONFLICT',True,False),
    ('occupied',None,b'user',b'new','CONFLICT',False,False),
    ('missing_required',b'base',b'base',None,'SPEC_GAPS',True,True),
]:
    setattr(LegacyMaintenance,'test_revision_'+name,lambda self,b=b,c=c,n=n,e=expected,o=owned,r=required:self.revision('1',b,c,n,e,o,r))


if __name__=='__main__':unittest.main(verbosity=2)
