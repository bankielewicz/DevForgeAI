"""Negative custody, publication, CLI and capability scenarios."""
import contextlib
import copy
import io
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch
import test_remediation as t
import test_legacy_maintenance as legacy
import authoring
import build_evidence as build
import custody
import init_skill
import generate_openai_yaml as metadata


class Edges(unittest.TestCase):
    setUp=legacy.LegacyMaintenance.setUp
    tearDown=legacy.LegacyMaintenance.tearDown
    before=legacy.LegacyMaintenance.before

    def adoption(self, mutation=None, handoff_mutation=None):
        hist,pointer=t.adopted(self.folder)
        record=json.loads((hist/'adoption.json').read_text())
        def relative_ref(path):return dict(t.ref(path),path=path.relative_to(hist).as_posix())
        evidence=t.put(hist/'selected-report.json',{'observation':'Synthetic input; no authority'})
        record.update(prior_evidence=[relative_ref(evidence)],quality_evidence=[relative_ref(evidence)],known_defects=['Synthetic known limitation'])
        packet={'schema_version':'1','target_root':record['target_root'],'target_manifest_sha256':record['snapshot_manifest']['sha256'],'managed_manifest_sha256':record['managed_manifest']['sha256'],'origin_spec_sha256':record['origin_spec']['sha256'],'review_policy':'review-before-repair','review_state':'reviewed','selected_references':[relative_ref(evidence)],'builder_readiness':'Synthetic reviewed input only'}
        if handoff_mutation:handoff_mutation(packet)
        record['handoff']=relative_ref(t.put(hist/'handoff.json',packet))
        if mutation:mutation(record,hist,relative_ref)
        t.put(hist/'selected-adoption.json',record)
        self.before()
        files=custody.snapshot(hist);problems=[]
        if mutation or handoff_mutation:
            try:custody.adoption_record(hist,files,record,problems)
            except (ValueError,KeyError):pass
            else:self.assertTrue(problems,'invalid adoption silently accepted')
        else:
            custody.adoption_record(hist,files,record,problems)
            self.assertEqual(problems,[])

    def test_valid_handoff_with_known_defects(self):self.adoption()

    def test_cli_initializer_constraints(self):
        self.before()
        for name,extra in [('!!!',[]),('a'*65,[]),('sample',['--examples']),('sample',['--resources','invalid'])]:
            with patch.object(sys,'argv',['init_skill.py',name,'--path',str(self.folder),*extra]),contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:init_skill.main()
                self.assertEqual(ctx.exception.code,1)
        with patch.object(sys,'argv',['init_skill.py','Sample Name','--path',str(self.folder),'--resources','scripts','--examples']),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:init_skill.main()
            self.assertEqual(ctx.exception.code,0)
        self.assertTrue((self.folder/'sample-name/scripts/example.py').exists())

    def test_cli_metadata_explicit_policy(self):
        skill=self.folder/'sample';t.put(skill/'SKILL.md',b'---\nname: sample\n---\n')
        self.before()
        with patch.object(sys,'argv',['metadata',str(skill),'--allow-implicit-invocation','false']),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:metadata.main()
            self.assertEqual(ctx.exception.code,0)
        import yaml
        self.assertIs(yaml.safe_load((skill/'agents/openai.yaml').read_text())['policy']['allow_implicit_invocation'],False)
        for path in (self.folder/'missing',skill/'SKILL.md'):
            with patch.object(sys,'argv',['metadata',str(path)]),contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:metadata.main()
                self.assertEqual(ctx.exception.code,1)

    def test_initializer_io_failures(self):
        self.before()
        scenarios=[('directory', 'mkdir'),('entrypoint','write_text')]
        for name,method in scenarios:
            with patch.object(Path,method,side_effect=OSError('synthetic I/O failure')),contextlib.redirect_stdout(io.StringIO()):
                self.assertIsNone(init_skill.init_skill('sample',self.folder/name,[],False,[]))
        with patch.object(init_skill,'write_openai_yaml',side_effect=OSError('synthetic metadata error')),contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(init_skill.init_skill('sample',self.folder/'metadata',[],False,[]))
        with patch.object(init_skill,'create_resource_dirs',side_effect=OSError('synthetic resource error')),contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(init_skill.init_skill('sample',self.folder/'resource',['scripts'],False,[]))

    def test_spec_resolution_negative_inputs(self):
        project=self.folder
        self.before()
        args=types.SimpleNamespace(project_root=str(project),spec='missing.md',name=None)
        self.assertEqual(build.resolve_spec(args)[1]['reason_code'],'MISSING_INPUT')
        for content in (b'No frontmatter',b'---\nskill_name: [\n---\n',b'---\n[]\n---\n',b'---\nskill_name: 42\n---\n',b'---\nskill_name: a\nskill_name: b\n---\n'):
            p=t.put(project/'docs/plan/spec.md',content)
            if content==b'No frontmatter':self.assertIsNone(build.name_from_markdown(p))
            else:
                with self.assertRaises(ValueError):build.name_from_markdown(p)
        args.spec=None;args.name='Bad Name'
        with self.assertRaises(ValueError):build.resolve_spec(args)
        args.name='sample';t.put(project/'docs/plan/spec.md',b'---\nskill_name: sample\n---\n')
        with patch.object(build,'MAX_FILES',0):
            with self.assertRaises(ValueError):build.resolve_spec(args)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(build.main(['input-record','--id','invalid id','--file',str(project/'docs/plan/spec.md'),'--snapshot-path','spec.md']),2)

    def test_untrusted_custody_primitives(self):
        self.before()
        for fn,value in [(custody.nonempty,'  '),(custody.sha,'wrong'),(custody.strings,['a','a']),(custody.objects,[1])]:
            with self.assertRaises(ValueError):fn(value)
        with self.assertRaises(ValueError):custody.indexed([{'id':'same'},{'id':'same'}],'id')
        base={'path':'a','bytes':1,'sha256':'0'*64}
        for rows in ([base,base],[dict(base,bytes=True)],[dict(base,path='b'),base]):
            with self.assertRaises(ValueError):custody.observed_rows(self.folder,rows)
        with self.assertRaises(ValueError):custody.pointer_record(self.folder,{}, {'schema_version':'1','run_id':'x','target_name':'x','origin':{},'baseline':[]},[])

    def test_publish_drift_and_repeat_rejected(self):
        cp=t.put(self.folder/'contract.json',t.contract(self.folder));run=self.folder/'docs/plan/run'
        authoring.begin(cp,run);t.put(run/'candidate/SKILL.md',b'new\n')
        self.before()
        def concurrent(path):t.put(self.folder/'skills/sample'/path,b'external\n')
        result=authoring.publish(run,before_write=concurrent)
        self.assertEqual(result['state'],'PARTIAL')
        self.assertEqual(result['applied_paths'],[])
        self.assertEqual((self.folder/'skills/sample/SKILL.md').read_bytes(),b'external\n')
        with self.assertRaises(ValueError):authoring.publish(run)

    def test_input_custody_and_stale_publication(self):
        source=t.put(self.folder/'selected.md',b'original requirement')
        c=t.contract(self.folder);c['inputs']=[t.ref(source)]
        cp=t.put(self.folder/'contract.json',c);run=self.folder/'docs/plan/run'
        self.before();authoring.begin(cp,run)
        self.assertEqual((run/'inputs/0').read_bytes(),b'original requirement')
        t.put(run/'candidate/SKILL.md',b'new');source.write_bytes(b'changed requirement')
        result=authoring.publish(run)
        self.assertEqual(result['state'],'BLOCKED');self.assertEqual(result['applied_paths'],[])

    def test_intake_destinations_and_scope(self):
        self.before()
        cases=[('whitespace',lambda c:c.update(authorization=' ')),('name',lambda c:c.update(target_name='other')),('overlap',lambda c:c.update(target_root=str(self.folder))),('missing_edit',lambda c:c.update(operation='edit')),('occupied',lambda c:None),('adopt_prior',lambda c:c.update(operation='adopt',prior=t.ref(self.folder/'occupied/skills/sample/input.md')))]
        for name,change in cases:
            p=self.folder/name;p.mkdir();c=t.contract(p)
            if name in ('occupied','adopt_prior'):t.put(p/'skills/sample/input.md',b'input')
            change(c);cp=t.put(p/'contract.json',c)
            with self.assertRaises(ValueError):authoring.begin(cp,p/'docs/plan/run')
            self.assertFalse((p/'docs/plan/run').exists())
        p=self.folder/'outside';p.mkdir();cp=t.put(p/'contract.json',t.contract(p))
        with self.assertRaises(ValueError):authoring.begin(cp,p/'other/run')
        p=self.folder/'inside';p.mkdir();source=t.put(p/'skills/sample/input.md',b'input');c=t.contract(p,'edit');c['inputs']=[t.ref(source)];cp=t.put(p/'contract.json',c)
        with self.assertRaises(ValueError):authoring.begin(cp,p/'docs/plan/run')

    def test_corrupt_authored_history(self):
        c=t.contract(self.folder);cp=t.put(self.folder/'contract.json',c);run=self.folder/'docs/plan/seed'
        authoring.begin(cp,run);t.put(run/'candidate/SKILL.md',b'base');authoring.publish(run)
        pointer=json.loads((run/'authoring-baseline.json').read_text())
        record=json.loads((run/'authoring-record.json').read_text())
        publication=json.loads((run/'publication-readback.json').read_text())
        c.update(operation='edit',history_review='known',prior=t.ref(run/'authoring-baseline.json'))
        self.before()
        for name in ('pointer_identity','pointer_kind','publication','record_identity','baseline_ref','ownership','baseline_bytes','failed_publication'):
            p=copy.deepcopy(pointer);a=copy.deepcopy(record);r=copy.deepcopy(publication)
            if name=='pointer_identity':p['target_name']='wrong'
            if name=='pointer_kind':p['record_kind']='wrong'
            if name=='record_identity':a['run_id']='wrong'
            if name=='baseline_ref':a['baseline_manifest']=a['delivered_manifest']
            if name=='ownership':a['managed_paths']=[]
            if name=='baseline_bytes':t.put(run/'baseline/SKILL.md',b'changed')
            if name=='failed_publication':t.put(run/'publication-failure.json',{'state':'PARTIAL'})
            t.put(run/'authoring-record.json',a);p['authoring_record']=t.ref(run/'authoring-record.json')
            t.put(run/'authoring-baseline.json',p);c['prior']=t.ref(run/'authoring-baseline.json');r['baseline']=c['prior']
            if name=='publication':r['state']='FAILED'
            t.put(run/'publication-readback.json',r)
            if name=='baseline_ref':
                # In this no-user-edit seed, delivered and baseline manifests are equal.
                authoring.origin(c)
            else:
                with self.assertRaises(ValueError):authoring.origin(c)
            t.put(run/'baseline/SKILL.md',b'base')

    def test_runtime_io_and_internal_parse_failure(self):
        self.before()
        runtime=t.adaptive.runtime
        for exc,code,reason in [(PermissionError('SENSITIVE SYNTHETIC TEXT'),2,'IO_ERROR'),(ValueError('SENSITIVE SYNTHETIC TEXT'),1,'INVALID_BINDING')]:
            with patch.object(runtime,'safe_path',side_effect=exc):result,obs=runtime.observe(str(self.folder),str(self.folder))
            self.assertEqual((result,obs['reason_code']),(code,reason));self.assertNotIn('SENSITIVE',json.dumps(obs))

    def test_handoff_graph_semantics(self):
        original=t.AUDIT/'fixtures/followup-02/records/proposal.json'
        if not original.exists():
            original=t.AUDIT/'fixtures/followup-02/records/adaptation-proposal.json'
        proposal=json.loads(original.read_text())
        schema=t.put(self.folder/'contract-schema.json',{'type':'object'})
        proposal['handoffs']=[{'id':'H1','producer':'A','consumer':'B','artifact_role':'summary','format':'json','schema_ref':t.ref(schema),'contract':'An object summary','required':True,'failure_behavior':'block_consumer'}]
        self.before();t.adaptive.Reader().record(proposal)
        for name in ('endpoint','failure','dependency','schema'):
            value=copy.deepcopy(proposal)
            if name=='endpoint':value['handoffs'][0]['producer']='unknown'
            if name=='failure':value['handoffs'][0]['failure_behavior']='report_optional_absence'
            if name=='dependency':value['members'][1]['depends_on']=[]
            if name=='schema':value['handoffs'][0]['schema_ref']=t.ref(t.put(self.folder/'bad-schema.json',42))
            with self.assertRaises(ValueError):t.adaptive.Reader().record(value)


def readback_change(record,hist,relative_ref,key,value):
    rb=json.loads((hist/'readback.json').read_text());rb[key]=value
    record['source_readback']=relative_ref(t.put(hist/'readback-altered.json',rb))


for name,mutation in {
    'origin':lambda r,h,f:r.update(historical_origin='generated'),
    'state':lambda r,h,f:r.update(recording_state='INVALID'),
    'incomplete':lambda r,h,f:r.update(recording_state='INCOMPLETE'),
    'name':lambda r,h,f:r.update(target_name='../escape'),
    'root':lambda r,h,f:r.update(target_root=str(h)),
    'time':lambda r,h,f:r.update(captured_at_utc='2026-09-13T00:00:00'),
    'snapshot':lambda r,h,f:r.update(snapshot_root='missing'),
    'partition':lambda r,h,f:r.update(retained_user_paths=['SKILL.md']),
    'spec':lambda r,h,f:r['origin_spec'].update(sha256='0'*64),
    'bytes_boolean':lambda r,h,f:r['origin_spec_input'].update(bytes=True),
    'bytes_wrong':lambda r,h,f:r['origin_spec_input'].update(bytes=0),
    'duplicate_evidence':lambda r,h,f:r['prior_evidence'].append(copy.deepcopy(r['prior_evidence'][0])),
    'evidence_digest':lambda r,h,f:r['quality_evidence'][0].update(sha256='0'*64),
    'readback_version':lambda r,h,f:readback_change(r,h,f,'schema_version','2'),
    'readback_identity':lambda r,h,f:readback_change(r,h,f,'run_id','wrong'),
    'readback_bytes':lambda r,h,f:readback_change(r,h,f,'after',[]),
    'readback_spec':lambda r,h,f:readback_change(r,h,f,'spec_after_sha256','0'*64),
}.items():
    setattr(Edges,'test_adoption_invalid_'+name,lambda self,m=mutation:self.adoption(m))
for name,mutation in {
    'policy':lambda p:p.update(review_policy='automatic'),
    'state':lambda p:p.update(review_state='unreviewed'),
    'target':lambda p:p.update(target_root='unrelated'),
    'digest':lambda p:p.update(target_manifest_sha256='0'*64),
    'references':lambda p:p.update(selected_references=[]),
    'reference_digest':lambda p:p['selected_references'][0].update(sha256='0'*64),
}.items():
    setattr(Edges,'test_handoff_invalid_'+name,lambda self,m=mutation:self.adoption(handoff_mutation=m))


if __name__=='__main__':unittest.main(verbosity=2)
