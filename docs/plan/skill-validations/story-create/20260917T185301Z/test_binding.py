"""Independent tests of the captured story-create runtime helper."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_trials import binding, RUN

spec=importlib.util.spec_from_file_location('binding_target',RUN/'source/scripts/check_project_binding.py')
target=importlib.util.module_from_spec(spec)
spec.loader.exec_module(target)

class BindingTests(unittest.TestCase):
    def setUp(self):
        (RUN/'test-work').mkdir(exist_ok=True)
        self.root=Path(tempfile.mkdtemp(prefix=self._testMethodName+'-',dir=RUN/'test-work'))
        self.skill=self.root/'.agents/skills/story-create'
        shutil.copytree(RUN/'source',self.skill)
        self.record=self.root/'.agents/devforgeai/project-binding.json'
        self.record.parent.mkdir(parents=True)
        self.value=binding(self.root)
        self.save()

    def save(self):
        self.record.write_text(json.dumps(self.value),encoding='utf-8')

    def assert_result(self,exit_code,reason,skill=None):
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        code,result=target.observe(self.root,skill or self.skill)
        self.assertEqual((code,result['reason_code']),(exit_code,reason))
        self.assertEqual(result['status'],'MATCH' if code==0 else 'UNAVAILABLE' if code==2 else 'MISMATCH')
        self.assertNotIn(self.value['project_id'],json.dumps(result))
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after,'Read-only helper modified fixture')
        return result

    def test_valid_binding(self):
        result=self.assert_result(0,'BOUND')
        self.assertEqual(result['package_digest'],self.value['bindings'][0]['package_digest'])

    def test_missing_binding(self):
        self.record.unlink()
        self.assert_result(1,'MISSING_BINDING')

    def test_json_rejections(self):
        for raw in ['{','{"x":1,"x":2}','{"x":NaN}','{"x":1e309}','[]','null']:
            with self.subTest(raw=raw):
                self.record.write_text(raw,encoding='utf-8')
                self.assert_result(1,'INVALID_BINDING')

    def test_wrong_root(self):
        self.value['project_root']=str(self.root.parent)
        self.save()
        self.assert_result(1,'ROOT_MISMATCH')

    def test_unselected(self):
        self.value['bindings'][0]['selected']=False
        self.save()
        self.assert_result(1,'NOT_SELECTED')

    def test_wrong_role(self):
        self.value['bindings'][0]['role']='expertise'
        self.save()
        self.assert_result(1,'ROLE_MISMATCH')

    def test_stale_digest(self):
        self.value['bindings'][0]['package_digest']='0'*64
        self.save()
        self.assert_result(1,'PACKAGE_CHANGED')

    def test_changed_package(self):
        (self.skill/'references/story-contract.md').write_text('changed',encoding='utf-8')
        self.assert_result(1,'PACKAGE_CHANGED')

    def test_relocated_package(self):
        other=self.root/'different/story-create'
        shutil.copytree(self.skill,other)
        self.assert_result(1,'UNBOUND_SKILL',other)

    def test_malformed_binding_fields(self):
        original=copy.deepcopy(self.value)
        changes=[('extra',True),('revision',True),('revision',0),('project_id','not-a-uuid'),('updated_at_utc','2026-99-01T00:00:00Z'),('updated_at_utc','yesterday'),('project_root','relative'),('bindings',[])]
        for key,value in changes:
            with self.subTest(key=key,value=value):
                self.value=copy.deepcopy(original);self.value[key]=value;self.save()
                self.assert_result(1,'INVALID_BINDING')

    def test_duplicate_binding_rows(self):
        self.value['bindings'].append(copy.deepcopy(self.value['bindings'][0]));self.save()
        self.assert_result(1,'INVALID_BINDING')

    def test_bad_package_path(self):
        self.value['bindings'][0]['package_path']='.agents/skills/../story-create';self.save()
        self.assert_result(1,'UNSAFE_PATH')

    def test_missing_descriptor(self):
        (self.skill/'assets/devforgeai-skill.json').unlink()
        self.assert_result(1,'INVALID_BINDING')

    def test_descriptor_resource_escape(self):
        path=self.skill/'assets/devforgeai-skill.json'; value=json.loads(path.read_bytes())
        value['resource_roles'][0]['path']='../outside'
        path.write_text(json.dumps(value),encoding='utf-8')
        self.assert_result(1,'UNSAFE_PATH')

    def test_identity_mismatch(self):
        path=self.skill/'SKILL.md'
        path.write_text(path.read_text(encoding='utf-8').replace('name: story-create','name: someone-else'),encoding='utf-8')
        self.assert_result(1,'INVALID_BINDING')

    def test_ambiguous_core_variant(self):
        variant=self.root/'.agents/skills/story-variant';shutil.copytree(self.skill,variant)
        path=variant/'SKILL.md';path.write_text(path.read_text(encoding='utf-8').replace('name: story-create','name: story-variant'),encoding='utf-8')
        path=variant/'assets/devforgeai-skill.json';desc=json.loads(path.read_bytes())
        desc.update(name='story-variant',role='project_variant',parent_core={'name':'story-create','package_digest':self.value['bindings'][0]['package_digest'],'requirement_ids':['STC-001']})
        path.write_text(json.dumps(desc),encoding='utf-8')
        self.value['bindings'].append({'name':'story-variant','package_path':'.agents/skills/story-variant','package_digest':'0'*64,'role':'project_variant','selected':True});self.save()
        self.assert_result(1,'AMBIGUOUS_ROLE')

    def test_unselected_related_ignored(self):
        self.value['bindings'].append({'name':'unselected','package_path':'.agents/skills/unselected','package_digest':'0'*64,'role':'core','selected':False});self.save()
        self.assert_result(0,'BOUND')

    def test_selected_expertise_not_role_collision(self):
        self.value['bindings'].append({'name':'expertise','package_path':'.agents/skills/expertise','package_digest':'0'*64,'role':'expertise','selected':True});self.save()
        self.assert_result(0,'BOUND')

    def test_missing_selected_peer(self):
        self.value['bindings'].append({'name':'peer','package_path':'.agents/skills/peer','package_digest':'0'*64,'role':'core','selected':True});self.save()
        self.assert_result(1,'INVALID_BINDING')

    def test_excluded_material_rejected(self):
        for name in ['.env.secret','private.pem','id_ed25519','notes.backup','module.pyc','devforgeai_cli']:
            with self.subTest(name=name):
                p=self.skill/name;p.write_text('synthetic',encoding='utf-8')
                self.assert_result(1,'UNSAFE_PATH');p.unlink()

    def test_capture_budget(self):
        with patch.object(target,'MAX_BYTES',1):
            self.assert_result(2,'CAPTURE_LIMIT')
        with patch.object(target,'MAX_FILES',1):
            self.assert_result(2,'CAPTURE_LIMIT')

    def test_io_error_sanitized(self):
        with patch.object(target.Capture,'read',side_effect=PermissionError('synthetic confidential marker')):
            result=self.assert_result(2,'IO_ERROR')
            self.assertNotIn('confidential',json.dumps(result))

    def test_unexpected_value_error_sanitized(self):
        with patch.object(target,'descriptor',side_effect=TypeError('synthetic confidential marker')):
            self.assert_result(1,'INVALID_BINDING')

    def test_repeat_capture_detects_drift(self):
        capture=target.Capture();p=self.root/'sample.txt';p.write_text('one',encoding='utf-8')
        capture.read(p);p.write_text('two',encoding='utf-8')
        with self.assertRaisesRegex(target.BindingError,'PACKAGE_CHANGED'):capture.read(p)

    def test_binding_changed_during_observation(self):
        original=target.Capture.read
        count=0
        def read(capture,path):
            nonlocal count
            if Path(path)==self.record:
                count+=1
                if count==2:self.record.write_text('{}',encoding='utf-8')
            return original(capture,path)
        with patch.object(target.Capture,'read',read):
            code,result=target.observe(self.root,self.skill)
        self.assertEqual((code,result['reason_code']),(1,'PACKAGE_CHANGED'))

    def test_invalid_descriptor_contracts(self):
        original=json.loads((self.skill/'assets/devforgeai-skill.json').read_bytes())
        variants=[dict(original,name='a'*65),dict(original,parent_core={}),dict(original,required_capabilities=[]),dict(original,role='unknown')]
        for value in variants:
            with self.subTest(value=value):
                with self.assertRaises(target.BindingError):target.descriptor(value)

    def test_unsafe_relative_paths(self):
        for value in ['../outside','/outside','a\\b','C:/outside','a//b','a/./b','a\0b']:
            with self.subTest(value=value):
                with self.assertRaisesRegex(target.BindingError,'UNSAFE_PATH'):target.relpath(value)

    def test_safe_path_traversal(self):
        with self.assertRaisesRegex(target.BindingError,'UNSAFE_PATH'):target.safe_path(self.root/'..'/'outside')

    def test_cli_success(self):
        stream=io.StringIO()
        with patch.object(sys,'argv',['helper','--project-root',str(self.root),'--skill-root',str(self.skill)]),contextlib.redirect_stdout(stream):
            self.assertEqual(target.main(),0)
        value=json.loads(stream.getvalue());self.assertEqual(value['reason_code'],'BOUND')

    def test_cli_usage(self):
        with patch.object(sys,'argv',['helper']),contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:target.main()
        self.assertEqual(caught.exception.code,2)

if __name__=='__main__':unittest.main(verbosity=2)
