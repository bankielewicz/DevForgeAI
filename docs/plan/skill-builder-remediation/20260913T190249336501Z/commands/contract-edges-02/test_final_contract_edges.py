"""Required publication preservation and malformed legacy request scenarios."""
import contextlib
import copy
import io
import json
import sys
import types
import unittest
from unittest.mock import patch
import test_remediation as t
import test_legacy_maintenance as legacy
import authoring
import build_evidence as build
import generate_openai_yaml as metadata


class FinalEdges(unittest.TestCase):
    setUp = legacy.LegacyMaintenance.setUp
    tearDown = legacy.LegacyMaintenance.tearDown
    before = legacy.LegacyMaintenance.before

    def seed(self):
        c=t.contract(self.folder);c['change_paths']=['SKILL.md','notes.md']
        cp=t.put(self.folder/'contract.json',c);run=self.folder/'docs/plan/seed'
        authoring.begin(cp,run)
        t.put(run/'candidate/SKILL.md',b'original skill');t.put(run/'candidate/notes.md',b'original notes')
        self.assertEqual(authoring.publish(run)['state'],'AUTHORED')
        return c,run

    def test_owned_deletion(self):
        c,seed=self.seed();c.update(operation='edit',history_review='known',prior=t.ref(seed/'authoring-baseline.json'))
        cp=t.put(self.folder/'edit.json',c);run=self.folder/'docs/plan/edit';authoring.begin(cp,run)
        (run/'candidate/notes.md').unlink();self.before()
        self.assertEqual(authoring.publish(run)['state'],'AUTHORED')
        self.assertFalse((self.folder/'skills/sample/notes.md').exists())
        record=json.loads((run/'authoring-record.json').read_text())
        self.assertEqual(record['managed_paths'],['SKILL.md'])
        self.assertEqual((self.folder/'skills/sample/SKILL.md').read_bytes(),b'original skill')

    def test_out_of_scope_user_edit_keeps_prior_baseline(self):
        c,seed=self.seed();target=self.folder/'skills/sample'
        t.put(target/'notes.md',b'user notes')
        c.update(operation='edit',history_review='known',prior=t.ref(seed/'authoring-baseline.json'),change_paths=['SKILL.md'])
        cp=t.put(self.folder/'edit.json',c);run=self.folder/'docs/plan/edit';authoring.begin(cp,run)
        t.put(run/'candidate/SKILL.md',b'new skill');self.before()
        self.assertEqual(authoring.publish(run)['state'],'AUTHORED')
        self.assertEqual((target/'notes.md').read_bytes(),b'user notes')
        self.assertEqual((run/'baseline/notes.md').read_bytes(),b'original notes')
        self.assertEqual((seed/'baseline/notes.md').read_bytes(),b'original notes')

    def test_corrupted_capture_blocks_before_write(self):
        self.before()
        for name in ('before','contract'):
            project=self.folder/name;project.mkdir();c=t.contract(project);cp=t.put(project/'contract.json',c);run=project/'docs/plan/run'
            authoring.begin(cp,run);t.put(run/'candidate/SKILL.md',b'new')
            if name=='before':t.put(run/'before/unlisted.md',b'tamper')
            else:
                changed=copy.deepcopy(c);changed['authorization']='changed after intake';t.put(run/'contract.json',changed)
            with self.assertRaises(ValueError):authoring.publish(run)
            self.assertFalse((project/'skills/sample').exists())

    def test_invalid_legacy_revision_requests(self):
        hist=self.folder/'history';hist.mkdir()
        for name in ('B','C','N','after'):t.put(hist/name/'SKILL.md',b'base')
        base=dict(schema_version='1',run_id='r',baseline='B',current='C',candidate='N',after='after',required_paths=[],owned_paths=['SKILL.md'],prior_build=None,baseline_before=None,baseline_after=None)
        self.before()
        for mutation in (lambda c:c.update(schema_version='unknown'),lambda c:c.update(extra=True),lambda c:c.update(current='B'),lambda c:c.update(required_paths=['a','a']),lambda c:c.update(owned_paths=[]),lambda c:c.update(owned_paths=['../escape'])):
            request=copy.deepcopy(base);mutation(request);t.put(hist/'request.json',request)
            with self.assertRaises(ValueError):build.revision_plan(types.SimpleNamespace(snapshot_root=str(hist),request='request.json'))
        t.put(hist/'request.json',base);t.put(hist/'after/SKILL.md',b'drift')
        with self.assertRaises(ValueError):build.revision_plan(types.SimpleNamespace(snapshot_root=str(hist),request='request.json'))
        with self.assertRaises(ValueError):build.revision_plan(types.SimpleNamespace(snapshot_root=str(hist/'missing'),request='request.json'))

    def test_revision_required_user_deletion_conflict(self):
        hist=self.folder/'history';hist.mkdir()
        for name in ('B','C','N','after'):(hist/name).mkdir()
        for name in ('B','N'):t.put(hist/name/'SKILL.md',b'base')
        request=dict(schema_version='1',run_id='r',baseline='B',current='C',candidate='N',after='after',required_paths=['SKILL.md'],owned_paths=['SKILL.md'],prior_build=None,baseline_before=None,baseline_after=None,retry_of={'path':'previous.json','sha256':'0'*64})
        t.put(hist/'request.json',request);self.before()
        code,value=build.revision_plan(types.SimpleNamespace(snapshot_root=str(hist),request='request.json'))
        self.assertEqual((code,value['status']),(1,'CONFLICT'));self.assertEqual(value['applied_paths'],[])
        self.assertEqual(value['retry_of'],request['retry_of'])

    def test_spec_lookup_excluded_and_nested(self):
        self.before();args=types.SimpleNamespace(project_root=str(self.folder/'missing'),name='sample',spec=None)
        with self.assertRaises(ValueError):build.resolve_spec(args)
        args.project_root=str(self.folder)
        t.put(self.folder/'docs/plan',b'not a directory')
        with self.assertRaises(ValueError):build.resolve_spec(args)
        (self.folder/'docs/plan').unlink()
        t.put(self.folder/'docs/plan/backup/old.md',b'not selected')
        target=t.put(self.folder/'docs/plan/nested/spec.md',b'---\nskill_name: sample\n---\n')
        code,value=build.resolve_spec(args)
        self.assertEqual(code,0);self.assertEqual(value['path'],str(target));self.assertEqual(len(value['excluded_boundaries']),1)

    def test_metadata_invalid_requests(self):
        skill=self.folder/'sample';skill.mkdir();self.before()
        self.assertTrue(25<=len(metadata.generate_short_description('x'*200))<=64)
        self.assertTrue(25<=len(metadata.generate_short_description(''))<=64)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(metadata.write_openai_yaml(skill,'sample',['unknown=value']))
            for extra in ([],['--name','sample','--interface','unknown=value']):
                with patch.object(sys,'argv',['metadata',str(skill),*extra]):
                    with self.assertRaises(SystemExit) as ctx:metadata.main()
                    self.assertEqual(ctx.exception.code,1)
        self.assertFalse((skill/'agents/openai.yaml').exists())

    def test_metadata_concurrent_edit_preserved(self):
        skill=self.folder/'sample';path=t.put(skill/'agents/openai.yaml',b'interface:\n  display_name: Original\n')
        self.before();original=metadata.read_bytes;reads=[]
        def changed(p):
            reads.append(p)
            if len(reads)==2:t.put(path,b'interface:\n  display_name: User\n')
            return original(p)
        with patch.object(metadata,'read_bytes',changed):
            with self.assertRaises(ValueError):metadata.write_openai_yaml(skill,'sample',['display_name=Candidate'])
        self.assertEqual(path.read_bytes(),b'interface:\n  display_name: User\n')


if __name__=='__main__':unittest.main(verbosity=2)
