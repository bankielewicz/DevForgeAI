"""Maintenance regressions. Fixtures/oracles belong to this run, not the skill."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from evidence import RUN, ROOT, PACKAGE, manifest, dump
sys.path.insert(0, str(PACKAGE / 'scripts'))
import adaptive
import authoring

AUDIT = ROOT / 'docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z'
ATTEMPT = RUN / 'trials' / os.environ.get('REMEDIATION_ATTEMPT', 'unspecified')


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    path.write_bytes(data)
    return path


def ref(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def contract(project, operation='create'):
    return {'schema_version': 'authoring-contract-v1', 'run_id': 'trial', 'project_root': str(project), 'target_root': str(project/'skills/sample'), 'target_name': 'sample', 'operation': operation, 'authorization': 'Create or edit this synthetic sample only.', 'history_review': 'no_known_history', 'change_paths': ['SKILL.md'], 'requirements': [{'arbitrary_legacy_object': {'nested': True}}], 'capabilities': [], 'expected_outputs': [], 'side_effects': [], 'inputs': [], 'known_issues': []}


def adopted(project):
    target = project/'skills/sample'
    put(target/'SKILL.md', b'baseline\n')
    hist = project/'history'
    put(hist/'snapshot/SKILL.md', b'baseline\n')
    spec = put(hist/'spec.md', b'Explicit historical requirement R1.\n')
    rows = manifest(hist/'snapshot')
    sm = put(hist/'snapshot-manifest.json', {'schema_version':'1','files':rows})
    mm = put(hist/'managed-manifest.json', {'schema_version':'1','files':rows})
    def relative_ref(path):
        return dict(ref(path), path=path.relative_to(hist).as_posix())
    rb = put(hist/'readback.json', {'schema_version':'1','run_id':'old1','target_root':str(target),'before':rows,'after':rows,'spec_before_sha256':ref(spec)['sha256'],'spec_after_sha256':ref(spec)['sha256'],'outcome':'UNCHANGED'})
    record = {'schema_version':'1','record_kind':'adoption','run_id':'old1','target_name':'sample','target_root':str(target),'project_root':str(project),'captured_at_utc':'2026-09-12T00:00:00Z','historical_origin':'unknown','snapshot_root':'snapshot','snapshot_manifest':relative_ref(sm),'managed_paths':['SKILL.md'],'retained_user_paths':[],'origin_spec':relative_ref(spec),'authorization':{'instruction':'Explicitly adopt sample SKILL.md only','target_root':str(target),'managed_manifest_sha256':ref(mm)['sha256'],'origin_spec_sha256':ref(spec)['sha256']},'prior_evidence':[],'quality_evidence':[],'source_readback':relative_ref(rb),'recording_state':'ADOPTED','managed_manifest':relative_ref(mm),'origin_spec_input':{'resolved_path':str(spec),'bytes':spec.stat().st_size,'sha256':ref(spec)['sha256']}}
    origin = put(hist/'adoption.json', record)
    pointer = {'schema_version':'2','run_id':'old1','target_name':'sample','origin':dict(kind='adopted',**relative_ref(origin)),'baseline':[{'path':'SKILL.md','sha256':rows[0]['sha256']}]}
    return hist, pointer


class Regression(unittest.TestCase):
    def setUp(self):
        self.folder = ATTEMPT/self._testMethodName
        self.folder.mkdir(parents=True, exist_ok=False)

    def capture_before(self):
        self.before = manifest(self.folder)
        dump(ATTEMPT/'receipts'/(self._testMethodName+'-before.json'), self.before)

    def tearDown(self):
        dump(ATTEMPT/'receipts'/(self._testMethodName+'-after.json'), manifest(self.folder))

    def intake(self, mutation=None, valid=False):
        c = contract(self.folder)
        if mutation:
            mutation(c)
        path = put(self.folder/'contract.json', c)
        run = self.folder/'docs/plan/run'
        self.capture_before()
        if valid:
            self.assertEqual(authoring.begin(path, run)['state'], 'STAGED')
        else:
            with self.assertRaises(ValueError):
                authoring.begin(path, run)
            self.assertFalse(run.exists())
            self.assertEqual(manifest(self.folder), self.before)
        self.assertFalse((self.folder/'skills/sample').exists())

    def pointer(self, mutation=None, valid=False):
        hist, pointer = adopted(self.folder)
        if mutation:
            mutation(pointer)
        c = contract(self.folder, 'edit')
        c.update(prior=ref(put(hist/'pointer.json', pointer)), legacy_root=str(hist), history_review='known')
        path = put(self.folder/'contract.json', c)
        before = manifest(hist)
        target_before = manifest(self.folder/'skills/sample')
        run = self.folder/'docs/plan/run'
        self.capture_before()
        if valid:
            self.assertEqual(authoring.begin(path, run)['state'], 'STAGED')
        else:
            with self.assertRaises(ValueError):
                authoring.begin(path, run)
            self.assertFalse(run.exists())
        self.assertEqual(before, manifest(hist))
        self.assertEqual(target_before, manifest(self.folder/'skills/sample'))

    def linked(self, mutation=None, valid=False):
        source = AUDIT/'fixtures/extended-04/valid/set.json'
        result = json.loads(source.read_text())
        row = next(r for r in result['members'] if r['authoring_record'])
        record = json.loads(Path(row['authoring_record']['path']).read_text())
        request = json.loads(Path(row['validation_request']['path']).read_text())
        if mutation:
            mutation(record, request, self.folder)
        ap = put(self.folder/'authoring-record.json', record)
        request['authoring_record'] = ref(ap)
        qp = put(self.folder/'validation-request.json', request)
        put(self.folder/'publication-readback.json', {'state':'PUBLISHED','authoring_record':ref(ap),'request':ref(qp)})
        row.update(authoring_record=ref(ap), validation_request=ref(qp))
        put(self.folder/'set.json', result)
        self.capture_before()
        reader = adaptive.Reader()
        if valid:
            reader.record(result)
            reader.readback()
        else:
            with self.assertRaises(ValueError):
                reader.record(result)
        self.assertEqual(manifest(self.folder), self.before)

    def exclusion(self, name, blocked):
        target = self.folder/'package'
        put(target/'nested'/name, b'SYNTHETIC; NOT A REAL PRIVATE KEY\n')
        self.capture_before()
        capture = adaptive.runtime.Capture()
        opened = []
        original = Path.open
        def tracking(path, *args, **kwargs):
            opened.append(path)
            return original(path, *args, **kwargs)
        with patch.object(Path, 'open', tracking):
            if blocked:
                with self.assertRaises(adaptive.runtime.BindingError) as ctx:
                    capture.inventory(target)
                self.assertEqual(ctx.exception.reason, 'UNSAFE_PATH')
                self.assertEqual(opened, [])
            else:
                rows = capture.inventory(target)
                self.assertEqual([r['path'] for r in rows], ['nested/'+name])
                self.assertEqual(opened, [target/'nested'/name])


def install(name, fn):
    setattr(Regression, 'test_'+name, fn)


install('F02_valid', lambda self: self.intake(valid=True))
install('F02_unknown', lambda self: self.intake(lambda c: c.update(unlisted_field=True)))
install('F02_optional_valid', lambda self: self.intake(lambda c: c.update(purpose='Example', activation={'free':True}, recovery=[1,False], dependencies=[{'arbitrary':1}], operational_constraints=[None]), valid=True))
install('F02_bad_optional_ref', lambda self: self.intake(lambda c: c.update(retry_of={'path':'x','sha256':'wrong'})))
install('F02_bad_optional_type', lambda self: self.intake(lambda c: c.update(dependencies=False)))
install('F02_missing', lambda self: self.intake(lambda c: c.pop('requirements')))
install('F02_duplicate_paths', lambda self: self.intake(lambda c: c.update(change_paths=['SKILL.md','SKILL.md'])))
install('F04_valid', lambda self: self.pointer(valid=True))
for name, mutation in {
    'wrong_name': lambda p: p.update(target_name='wrong-skill'),
    'wrong_run': lambda p: p.update(run_id='wrong-run'),
    'extra': lambda p: p.update(unlisted=True),
    'missing': lambda p: p.pop('run_id'),
    'duplicate': lambda p: p['baseline'].append(copy.deepcopy(p['baseline'][0])),
    'digest': lambda p: p['origin'].update(sha256='0'*64),
    'baseline': lambda p: p['baseline'][0].update(sha256='0'*64),
}.items():
    install('F04_'+name, lambda self, m=mutation: self.pointer(m))

install('F01_valid', lambda self: self.linked(valid=True))
for name, mutation in {
    'quality': lambda a,q,p: a.update(validation_status='PASS',testing_status='PASS'),
    'kind': lambda a,q,p: a.update(record_kind='unrelated'),
    'request_kind': lambda a,q,p: q.update(record_kind='unrelated'),
    'request_name': lambda a,q,p: q.update(target_name='wrong'),
    'request_root': lambda a,q,p: q.update(target_root=str(p/'unrelated')),
    'request_run': lambda a,q,p: q.update(authoring_run_id='wrong'),
    'request_project': lambda a,q,p: q.update(project_root=str(p)),
    'request_type': lambda a,q,p: q.update(changed_paths=False),
    'request_paths': lambda a,q,p: q.update(changed_paths=[]),
    'request_manifest': lambda a,q,p: q.update(target_manifest=ref(put(p/'wrong-manifest.json', {'schema_version':'1','files':[],'package_digest':q['package_digest']}))),
    'record_manifest': lambda a,q,p: a.update(delivered_manifest=ref(put(p/'wrong-manifest.json', {'schema_version':'1','files':[],'package_digest':q['package_digest']}))),
    'extra': lambda a,q,p: q.update(extra=True),
}.items():
    install('F01_'+name, lambda self, m=mutation: self.linked(m))

for name in ['id_rsa','id_dsa','id_ecdsa','id_ed25519','id_ecdsa_sk','id_ed25519_sk','identity.pfx','identity.p12','identity.ppk','ID_RSA','IDENTITY.PFX','private.pem','private.key','.env']:
    install('F03_excluded_'+name.replace('.','_'), lambda self,n=name: self.exclusion(n, True))
for name in ['public.pub','certificate.crt','certificate.cer','id_rsa.pub','normal.txt']:
    install('F03_permitted_'+name.replace('.','_'), lambda self,n=name: self.exclusion(n, False))


if __name__ == '__main__':
    unittest.main(verbosity=2)
