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
from fixture_data import file_ref, files, sha, write_json


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


if __name__=='__main__':unittest.main()
