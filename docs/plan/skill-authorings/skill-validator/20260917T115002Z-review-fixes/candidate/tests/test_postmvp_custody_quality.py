"""Adversarial custody controls: type, ownership, preservation and lineage invariants."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import custody
import graders
import build_evidence
import run_evaluation
from adoption_fixture import build_adoption, build_v2
from fixture_data import file_ref, files, sha, write_json, build_candidate, build_revision, PACKAGE


class CustodyQualityTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)

    def test_json_protocol_and_path_rejections(self):
        for module in (custody,graders,run_evaluation):
            for raw in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'):
                with self.subTest(module=module.__name__,raw=raw),self.assertRaises(ValueError):module.strict_json(raw)
        self.assertEqual(custody.strict_json('{"x":1.25}')['x'],1.25)
        with self.assertRaises(ValueError):custody.strict_json('{"x":1e999}')
        for module in (custody,graders):
            self.assertEqual(module.bounded_path(self.root,'.',allow_dot=True),self.root)
            for value in ('',3,'/absolute','a/../b','a\\b','backups/a'):
                with self.subTest(module=module.__name__,value=value),self.assertRaises(ValueError):module.bounded_path(self.root,value)
            for value in ('',3,None):
                with self.assertRaises(ValueError):module.nonempty(value)
            for value in ('A'*64,'x',3):
                with self.assertRaises(ValueError):module.sha(value)
            for value in (['a','a'],[3],'a'):
                with self.assertRaises(ValueError):module.strings(value)
            with self.assertRaises(ValueError):module.objects([3])
            with self.assertRaises(ValueError):module.indexed([{'id':'x'},{'id':'x'}],'id')

    def assert_invalid_adoption(self, mutate):
        record=build_adoption(self.root)
        mutate(record)
        for module in (custody,graders):
            problems=[]
            try:module.adoption_record(self.root,files(self.root),record,problems)
            except ValueError:continue
            self.assertTrue(problems,'Invalid adoption must not qualify')

    def test_adoption_record_identity_and_partition(self):
        variants=[lambda r:r.update(schema_version=1),lambda r:r.update(recording_state='invented'),
                  lambda r:r.update(target_name='../outside'),lambda r:r.update(target_root='C:/elsewhere'),
                  lambda r:r.update(captured_at_utc='2026-01-01T00:00:00'),
                  lambda r:r.update(snapshot_root='absent'),lambda r:r.update(retained_user_paths=[]),
                  lambda r:r.update(managed_paths=['notes.txt','SKILL.md']),
                  lambda r:r['origin_spec_input'].update(bytes=True),
                  lambda r:r['origin_spec_input'].update(bytes=10000),
                  lambda r:r['authorization'].update(target_root='different'),
                  lambda r:r.update(recording_state='INCOMPLETE'),
                  lambda r:r['quality_evidence'].append(r['quality_evidence'][0]),
                  lambda r:r['quality_evidence'][0].update(sha256='0'*64),
                  lambda r:r['origin_spec'].update(sha256='0'*64)]
        for index,change in enumerate(variants):
            with self.subTest(index=index):self.assert_invalid_adoption(change)

    def test_adoption_rebound_manifest_and_readback_tampering(self):
        edits=[('snapshot_manifest',lambda r:r.update(schema_version='2')),
               ('snapshot_manifest',lambda r:r['files'].pop()),
               ('managed_manifest',lambda r:r['files'].clear()),
               ('source_readback',lambda r:r.update(schema_version='2')),
               ('source_readback',lambda r:r.update(run_id='other')),
               ('source_readback',lambda r:r['after'].pop()),
               ('source_readback',lambda r:r.update(spec_after_sha256='0'*64))]
        for key,edit in edits:
            def mutate(record):
                path=self.root/record[key]['path'];value=json.loads(path.read_text());edit(value);write_json(path,value);record[key]=file_ref(self.root,path)
            with self.subTest(key=key,edit=edit):self.assert_invalid_adoption(mutate)

    def test_observed_rows_cannot_hide_duplicates_types_or_order(self):
        for module in (custody,graders):
            base={'path':'b','bytes':0,'sha256':'0'*64}
            for rows in ([base,base],[dict(base,bytes=True)],[dict(base,path='../a')],[base,dict(base,path='a')]):
                with self.subTest(module=module.__name__,rows=rows),self.assertRaises(ValueError):module.observed_rows(self.root,rows)

    def test_selected_handoff_checks_bound_review_and_targets(self):
        record=build_adoption(self.root);record['known_defects']=['fixture defect']
        packet=dict(schema_version='1',target_root=record['target_root'],
                    target_manifest_sha256=record['snapshot_manifest']['sha256'],
                    managed_manifest_sha256=record['managed_manifest']['sha256'],
                    origin_spec_sha256=record['origin_spec']['sha256'],review_policy='review-before-repair',
                    review_state='reviewed',builder_readiness='READY',selected_references=[record['quality_evidence'][0]])
        path=self.root/'packet.json';write_json(path,packet);record['handoff']=file_ref(self.root,path)
        for module in (custody,graders):
            problems=[];module.adoption_record(self.root,files(self.root),record,problems);self.assertEqual(problems,[])
        for key,value in [('schema_version','2'),('review_state','pending'),('target_root','other'),('target_manifest_sha256','0'*64),('selected_references',[])]:
            changed={**packet,key:value};write_json(path,changed);record['handoff']=file_ref(self.root,path)
            for module in (custody,graders):
                problems=[]
                try:module.adoption_record(self.root,files(self.root),record,problems)
                except ValueError:continue
                self.assertTrue(problems)

    def test_link_and_manifest_invalid_shapes(self):
        folder=self.root/'package';folder.mkdir();(folder/'detail.md').write_text('[unbound][reference]\n[x](file:///outside)\n[x](/absolute)')
        problems=graders.package_links(self.root,{'path':'package'})
        self.assertTrue(problems)
        with self.assertRaises(ValueError):graders.package_links(self.root,{'path':'package','extra':1})
        with self.assertRaises(ValueError):graders.manifest_accounting(self.root,{'source':'a'})
        with self.assertRaises(ValueError):graders.grade('absent',self.root,{})
        with self.assertRaises(ValueError):graders.grade('package_links',self.root,[])

    def test_evaluation_case_limits_and_shape(self):
        for data,profile in [(b'','legacy-import-v1'),(b'{}','legacy-import-v1'),(b'{}','unknown'),(b'x'*1048577,'legacy-import-v1'),(b'{}\n'*1001,'legacy-import-v1')]:
            with self.subTest(length=len(data),profile=profile),self.assertRaises(ValueError):run_evaluation.load_cases(data,profile)

    def test_historical_provenance_rejects_unbound_generation(self):
        build_revision(self.root)
        original=json.loads((self.root/'revision/previous-provenance.json').read_text())
        variants=[lambda r:r.update(result='PARTIAL'),lambda r:r.update(target_name='Invalid'),
                  lambda r:r.update(inputs=[]),lambda r:r.update(mappings=[]),
                  lambda r:r['outputs'][0].update(path='../escape'),
                  lambda r:r['outputs'][0].update(baseline_path='backups/a'),
                  lambda r:r['outputs'][0].update(ownership='unowned'),
                  lambda r:r['mappings'][0].update(artifact_paths=['unknown']),
                  lambda r:r['mappings'][0].update(evidence_ids=['unknown'])]
        for module in (custody,graders):
            self.assertTrue(module.prior_provenance_record(original))
            for change in variants:
                value=copy.deepcopy(original);change(value)
                with self.subTest(module=module.__name__,change=change),self.assertRaises(ValueError):module.prior_provenance_record(value)
            chained=copy.deepcopy(original);chained['prior_build']={'path':'earlier.json','sha256':'0'*64}
            self.assertEqual(module.prior_provenance_record(chained),module.prior_provenance_record(original))
            version2=copy.deepcopy(original);version2.pop('prior_build');version2.update(schema_version='2',adoption_origin={'path':'adoption.json','sha256':'0'*64},prior_origin={'kind':'invented','path':'earlier.json','sha256':'0'*64})
            with self.assertRaises(ValueError):module.prior_provenance_record(version2,'2')
            with self.assertRaises(ValueError):module.hash_rows([{'path':'a','sha256':'0'*64}]*2)

    def test_build_contract_obligations_cannot_be_removed(self):
        variants=[lambda c,p:c.update(schema_version='2'),lambda c,p:c.update(target_name='Invalid'),
                  lambda c,p:p.update(target_name='other'),lambda c,p:p.update(dependencies=[{'name':'unselected'}]),
                  lambda c,p:c.update(inputs=[]),lambda c,p:c['inputs'][0].update(path='trace/destination/SKILL.md'),
                  lambda c,p:c['inputs'][0].update(bytes=True),
                  lambda c,p:c['requirements'][0].update(origin='invented'),
                  lambda c,p:c['requirements'][0].update(source_refs=[]),
                  lambda c,p:c['requirements'][0].update(artifact_paths=['missing']),
                  lambda c,p:c['requirements'][0].update(verification=[]),
                  lambda c,p:p['outputs'][0].update(baseline_path='trace/destination/SKILL.md'),
                  lambda c,p:p['outputs'][0].update(ownership='unowned'),
                  lambda c,p:p['evidence'][0].update(sha256='0'*64),
                  lambda c,p:p.update(mappings=[])]
        for i,change in enumerate(variants):
            with self.subTest(variant=i):
                root=self.root/str(i);params=build_candidate(root,sha((PACKAGE/'evals/build-manifest.json').read_bytes()))
                self.assertEqual(graders.build_traceability(root,params['build_traceability'])['status'],'PASS')
                cp=root/'trace/evidence/build-contract.json';pp=root/'trace/evidence/build-provenance.json'
                contract=json.loads(cp.read_text());provenance=json.loads(pp.read_text());change(contract,provenance)
                write_json(cp,contract);provenance['contract_sha256']=sha(cp.read_bytes());write_json(pp,provenance)
                try:problems=graders.build_traceability(root,params['build_traceability'])
                except ValueError:continue
                self.assertEqual(problems['status'],'FAIL','Removed or changed obligation must be rejected')

    def test_build_evidence_json_and_specification_diagnostics(self):
        from types import SimpleNamespace
        for raw in ('{"a":1,"a":2}','{"a":NaN}','{"a":1e999}'):
            with self.assertRaises(ValueError):build_evidence.json_value(raw)
        for value in ('','/absolute','a//b','a/../b','backups/a',3):
            with self.assertRaises(ValueError):build_evidence.relative_path(value)
        spec=self.root/'spec.md'
        for content in ('---\nskill_name: [\n---\n','---\n- scalar\n---\n','---\nskill_name: 123\n---\n','---\nskill_name: a\nskill_name: b\n---\n'):
            spec.write_text(content)
            with self.subTest(content=content),self.assertRaises(ValueError):build_evidence.name_from_markdown(spec)
        for name in ('UPPER','a'*65):
            with self.assertRaises(ValueError):build_evidence.resolve_spec(SimpleNamespace(project_root=str(self.root),spec=None,name=name))
        with self.assertRaises(ValueError):build_evidence.resolve_spec(SimpleNamespace(project_root=str(spec),spec=None,name='valid'))
        (self.root/'docs').mkdir();(self.root/'docs/plan').write_text('not a directory')
        with self.assertRaises(ValueError):build_evidence.resolve_spec(SimpleNamespace(project_root=str(self.root),spec=None,name='valid'))
        with self.assertRaises(ValueError):build_evidence.inventory(self.root/'absent')

    def test_revision_preview_preserves_current_and_ownership(self):
        from types import SimpleNamespace
        changes=[lambda p:p.update(schema_version='unknown'),lambda p:p.update(current=p['baseline']),
                 lambda p:p.update(required_paths=['SKILL.md','SKILL.md']),lambda p:p.update(owned_paths=[]),
                 lambda p:p.update(required_paths=['missing.md'])]
        for i,change in enumerate(changes):
            root=self.root/str(i);plan=build_revision(root,status='PLANNED');change(plan);write_json(root/'request.json',plan)
            with self.subTest(variant=i):
                try:code,value=build_evidence.revision_plan(SimpleNamespace(snapshot_root=str(root),request='request.json'))
                except ValueError:continue
                self.assertEqual(code,1);self.assertEqual(value['status'],'SPEC_GAPS')

    def test_snapshot_limits_and_excluded_content(self):
        for module in (custody,graders):
            with self.assertRaises(ValueError):module.snapshot(self.root/'missing')
        excluded=self.root/'excluded';(excluded/'backups').mkdir(parents=True)
        for module in (custody,graders):
            with self.assertRaises(ValueError):module.snapshot(excluded)
        large=self.root/'large';large.mkdir()
        with (large/'large.bin').open('wb') as stream:stream.truncate(32*1024*1024+1)
        for module in (custody,graders):
            with self.assertRaises(ValueError):module.snapshot(large)
        with self.assertRaises(ValueError):build_evidence.inventory(large)
        with self.assertRaises(ValueError):build_evidence.read_bytes(large/'large.bin')


if __name__=='__main__':unittest.main()
