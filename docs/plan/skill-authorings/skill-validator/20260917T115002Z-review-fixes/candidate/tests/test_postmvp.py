"""Requirement-derived checks for SVE-01 through SVE-10; real subprocesses only."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import skill_format
import text_resources


def skill_format_rows(metadata):
    return [(row[0], row[2]) for row in skill_format.advisory_checks(metadata) if not row[1]]


class MetadataRegressionTests(unittest.TestCase):
    def test_optional_constraints_are_not_lost_in_package_parser(self):
        for field in ('compatibility: ""', 'metadata: {version: 1}',
                      'allowed-tools: [1]', 'effort: ultra', 'shell: fish',
                      'disable-model-invocation: maybe',
                      'description: ' + 'x' * 1025):
            source = '---\nname: example\ndescription: Task\n' + field + '\n---\nDo work.'
            if field.startswith('description:'):
                source = source.replace('description: Task\n', '')
            with self.subTest(field=field[:45]), self.assertRaises(ValueError):
                text_resources.frontmatter(source)

    def test_name_boundary_and_malformed_keys(self):
        for name in ('Upper', 'a--b', '-a', 'a-', 'x' * 65):
            with self.subTest(name=name), self.assertRaises(ValueError):
                text_resources.frontmatter(f'---\nname: {name}\ndescription: Task\n---\n')
        for source in ('? [a, b]\n: x', '1: value', 'name: a\nname: b'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                text_resources.yaml_mapping(source)

    def test_valid_boundaries_and_unicode_content(self):
        source = '---\r\nname: ' + 'x' * 64 + '\r\ndescription: ' + 'é' * 1024
        source += '\r\ncompatibility: ' + 'y' * 500 + '\r\nmetadata: {version: "1"}\r\n---\r\nText Ω'
        self.assertEqual(text_resources.frontmatter(source)['metadata'], {'version': '1'})

    def test_claude_code_optional_field_shapes_are_accepted(self):
        # Claude Code documents a YAML list for tool grants, which the Agent Skills
        # specification does not. Rejecting it here would fail ordinary Claude Code
        # packages, including this repository's own skills.
        source = ('---\nname: example\ndescription: Task\n'
                  'allowed-tools:\n  - Read\n  - Bash(python:*)\n'
                  'disallowed-tools: Write Edit\n'
                  'model: inherit\neffort: high\nshell: powershell\n'
                  'context: fork\nagent: Explore\n'
                  'disable-model-invocation: true\nuser-invocable: false\n'
                  'paths:\n  - "src/**"\n'
                  '---\nDo work.\n')
        meta = text_resources.frontmatter(source)
        self.assertEqual(['Read', 'Bash(python:*)'], meta['allowed-tools'])
        divergent = dict(skill_format_rows(meta))
        self.assertIn('portable_tool_list', divergent)

    def test_organization_advice_does_not_fail_large_or_cyclic_skill(self):
        import standards_observe
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/'references').mkdir()
            (root/'SKILL.md').write_text('[A](references/a.md)\n' + 'A line\n'*501)
            (root/'references/a.md').write_text('[Root](../SKILL.md)')
            value=standards_observe.organization(root)
            self.assertTrue(value['over_500_lines'])
            self.assertTrue(value['cycles'])
            self.assertEqual(value['authority'],'NONE')

    def test_organization_cli_preserves_unicode_on_legacy_windows_pipe(self):
        with tempfile.TemporaryDirectory(prefix='standards Ω ') as folder:
            root=Path(folder)
            (root/'SKILL.md').write_text('[Details](Ω.md)',encoding='utf-8')
            (root/'Ω.md').write_text('Details',encoding='utf-8')
            environment=dict(os.environ,PYTHONIOENCODING='cp1252')
            result=subprocess.run([sys.executable,'-B',str(SCRIPTS/'standards_observe.py'),'--source',str(root)],
                                  env=environment,capture_output=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stdout)
            value=json.loads(result.stdout)
            self.assertIn('Ω.md',json.dumps(value,ensure_ascii=False))


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='validator Ω ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'project'; self.project.mkdir()
        self.module = SCRIPTS / 'trial_runner.py'
        self.assertTrue(self.module.is_file(), 'SVE-04 requires a reusable trial runner')
        spec = importlib.util.spec_from_file_location('trial_runner', self.module)
        self.runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.runner)

    def plan(self, code="print('done')", **updates):
        source = self.project / 'actor.py'; source.write_text(code, encoding='utf-8')
        import hashlib
        value = dict(schema_version='trial-plan-v1', case_id='case-1', kind='utility',
                     argv=[sys.executable, '-B', '-X', 'utf8', str(source)],
                     cwd=str(self.project), permitted_write_root=str(self.project),
                     inputs=[dict(path=str(source), sha256=hashlib.sha256(source.read_bytes()).hexdigest())],
                     prompt=None, requirement_ids=['SVE-07'], dependencies=[], expected_outputs=[])
        value.update(updates)
        path = self.root / 'plan.json'; path.write_text(json.dumps(value), encoding='utf-8')
        return path

    def execute(self, path):
        attempt = self.root / 'attempt-001'
        self.runner.seal(path, attempt)
        return attempt, self.runner.run(attempt)

    def test_actual_output_and_default_budgets(self):
        path = self.plan("from pathlib import Path; Path('answer.txt').write_text('42')",
                         kind='native', expected_outputs=[dict(path='answer.txt', kind='text', value='42', requirement_id='SVE-07')])
        attempt, receipt = self.execute(path)
        self.assertEqual(receipt['timeout_seconds'], 600)
        self.assertEqual(receipt['outcome'], 'PASS')
        self.assertEqual(self.runner.check_attempt(attempt)['outcome'], 'PASS')
        with self.assertRaises(ValueError): self.runner.run(attempt)

    def test_zero_exit_does_not_prove_delivery(self):
        _, receipt = self.execute(self.plan(expected_outputs=[dict(path='missing.txt', kind='exists', requirement_id='SVE-07')]))
        self.assertEqual(receipt['exit_code'], 0)
        self.assertEqual(receipt['outcome'], 'FAIL')
        self.assertEqual(receipt['timeout_seconds'], 120)

    def test_timeout_preserves_output_and_cleanup(self):
        attempt, receipt = self.execute(self.plan("import time; print('partial', flush=True); time.sleep(30)", timeout_seconds=0.4))
        self.assertEqual(receipt['outcome'], 'NOT_RUN')
        self.assertTrue(receipt['timeout'])
        self.assertEqual(receipt['cleanup'], 'VERIFIED')
        self.assertIn('partial', (attempt / 'stdout.txt').read_text())
        self.assertEqual(self.runner.check_attempt(attempt)['outcome'], 'NOT_RUN')

    def test_plan_and_input_drift_before_launch(self):
        path = self.plan(); attempt = self.root / 'attempt'
        self.runner.seal(path, attempt)
        path.write_text(path.read_text() + ' ')
        with self.assertRaises(ValueError): self.runner.run(attempt)
        self.assertFalse((attempt / 'started.json').exists())

    def test_stale_sealed_fixture(self):
        path = self.plan(); attempt = self.root / 'attempt'
        self.runner.seal(path, attempt)
        (self.project / 'actor.py').write_text('changed')
        with self.assertRaises(ValueError): self.runner.run(attempt)

    def test_interrupted_attempt_is_not_replayed(self):
        path = self.plan(); attempt = self.root / 'attempt'
        self.runner.seal(path, attempt)
        (attempt / 'started.json').write_text('{}')
        with self.assertRaises(ValueError): self.runner.run(attempt)
        self.assertEqual(self.runner.check_attempt(attempt)['outcome'], 'NOT_RUN')

    def test_artifact_drift_invalidates_readback(self):
        attempt, _ = self.execute(self.plan("from pathlib import Path; Path('a').write_text('ok')", expected_outputs=[dict(path='a', kind='text', value='ok', requirement_id='SVE-07')]))
        (self.project / 'a').write_text('wrong')
        with self.assertRaises(ValueError): self.runner.check_attempt(attempt)

    def test_json_oracle_and_manual_obligation(self):
        attempt, receipt = self.execute(self.plan("from pathlib import Path; Path('a').write_text('{\"x\": 3}')", requirement_ids=['SVE-07', 'SVE-08'], expected_outputs=[dict(path='a', kind='json', value={'x': 3}, requirement_id='SVE-07'), dict(path='a', kind='manual', requirement_id='SVE-08')]))
        self.assertEqual(receipt['output_checks'][0]['result'], 'PASS')
        self.assertEqual(receipt['outcome'], 'NOT_RUN')

    def test_invalid_plans_never_launch(self):
        for override in ({'timeout_seconds':True}, {'timeout_seconds':0}, {'timeout_seconds':float('inf')},
                         {'argv':'echo bad'}, {'expected_outputs':[dict(path='../escape',kind='exists',requirement_id='SVE-07')]},
                         {'requirement_ids':[]}, {'kind':'invented'}, {'dependencies':['case-1']}):
            with self.subTest(override=override), self.assertRaises(ValueError):
                self.runner.seal(self.plan(**override), self.root / 'invalid')

    def test_independent_case_remains_counted_with_blocked_case(self):
        attempt, _ = self.execute(self.plan())
        cases = [dict(case_id='case-1',attempt=str(attempt),dependencies=[]),
                 dict(case_id='blocked',attempt=None,dependencies=[])]
        summary = self.runner.summarize(cases)
        self.assertEqual(summary['required_total'], 2)
        self.assertEqual(summary['passed'], 1)
        self.assertEqual(summary['outcome'], 'INCOMPLETE')
        with self.assertRaises(ValueError): self.runner.summarize(cases + [cases[0]])

    def test_receipt_fields_cannot_discard_evidence(self):
        attempt, _ = self.execute(self.plan())
        original = (attempt / 'result.json').read_bytes()
        for key, value in [('streams', []), ('schema_version', 'invalid'), ('timeout_seconds',999),
                           ('exit_code',False), ('elapsed_seconds',-999)]:
            receipt = json.loads(original); receipt[key] = value
            (attempt / 'result.json').write_text(json.dumps(receipt))
            with self.subTest(key=key), self.assertRaises(ValueError): self.runner.check_attempt(attempt)
        (attempt / 'result.json').write_bytes(original)

    def test_side_effects_are_observed(self):
        _, receipt = self.execute(self.plan("from pathlib import Path; Path('additional').write_text('created')"))
        self.assertIn('additional', receipt.get('changed_paths', []))

    def test_dependency_inventory_cannot_be_dropped(self):
        first, _ = self.execute(self.plan())
        path = self.plan(); value = json.loads(path.read_text()); value['case_id']='dependent'
        value['dependencies']=['case-1']; value['dependency_attempts']={'case-1':str(first)}
        # Preserve original plan bytes for the first case.
        first_plan = self.root / 'first-plan.json'
        first_plan.write_bytes((first / 'plan.json').read_bytes())
        # Use a distinct fixture input and new plan, without changing prior inputs.
        path.write_bytes(first_plan.read_bytes())
        dependent_plan=self.root/'dependent.json'; dependent_plan.write_text(json.dumps(value))
        second=self.root/'attempt-002'; self.runner.seal(dependent_plan,second); self.runner.run(second)
        with self.assertRaises(ValueError):
            self.runner.summarize([dict(case_id='dependent',attempt=str(second),dependencies=[])])

    def test_empty_native_oracle_and_preexisting_outputs_are_rejected(self):
        (self.project/'old.txt').write_text('already here')
        for index, override in enumerate(({'kind':'native'}, {'expected_outputs':[dict(path='old.txt',kind='exists',requirement_id='SVE-07')]})):
            with self.subTest(override=override), self.assertRaises(ValueError):
                self.runner.seal(self.plan(**override),self.root/f'attempt-{index}')

    def test_exact_json_type_not_python_boolean_equivalence(self):
        _, result=self.execute(self.plan("from pathlib import Path; Path('a').write_text('true')",expected_outputs=[dict(path='a',kind='json',value=1,requirement_id='SVE-07')]))
        self.assertEqual(result['outcome'],'FAIL')

    def test_stdout_tampering_and_input_drift_after_execution(self):
        attempt,_=self.execute(self.plan())
        (attempt/'stdout.txt').write_text('forged')
        with self.assertRaises(ValueError): self.runner.check_attempt(attempt)

    def test_failed_cli_and_closed_stdin(self):
        _, result=self.execute(self.plan("import sys; print(sys.stdin.read()); sys.exit(3)"))
        self.assertEqual(result['exit_code'],3)
        self.assertEqual(result['outcome'],'NOT_RUN')

    def test_prompt_is_literal_stdin(self):
        import hashlib
        prompt=self.root/'prompt.txt';prompt.write_text('literal $() `quoted` Ω',encoding='utf-8')
        _, result=self.execute(self.plan("import sys; from pathlib import Path; Path('a').write_bytes(sys.stdin.buffer.read())",prompt={'path':str(prompt),'sha256':hashlib.sha256(prompt.read_bytes()).hexdigest()},expected_outputs=[dict(path='a',kind='text',value=prompt.read_text(encoding='utf-8'),requirement_id='SVE-07')]))
        self.assertEqual(result['outcome'],'PASS')

    def test_receipt_chronology_cannot_be_reversed(self):
        attempt,_=self.execute(self.plan())
        result=json.loads((attempt/'result.json').read_text());result['ended_at']='2000-01-01T00:00:00+00:00'
        (attempt/'result.json').write_text(json.dumps(result))
        with self.assertRaises(ValueError): self.runner.check_attempt(attempt)

    def test_cli_help_invalid_and_successful_readback(self):
        for command in ('seal','run','check','summary'):
            result=subprocess.run([sys.executable,'-B',str(self.module),command,'--help'],capture_output=True,timeout=20)
            self.assertEqual(result.returncode,0)
        result=subprocess.run([sys.executable,'-B',str(self.module),'check','--attempt',str(self.root/'absent')],capture_output=True,timeout=20)
        self.assertEqual(result.returncode,2)
        path=self.plan(); attempt=self.root/'cli-attempt'
        commands=[['seal','--plan',str(path),'--attempt',str(attempt)],['run','--attempt',str(attempt)],['check','--attempt',str(attempt)]]
        for args in commands:
            result=subprocess.run([sys.executable,'-B',str(self.module),*args],capture_output=True,timeout=20)
            self.assertEqual(result.returncode,0,result.stdout)
        inventory=self.root/'cases.json';inventory.write_text(json.dumps([dict(case_id='case-1',attempt=str(attempt),dependencies=[])]))
        result=subprocess.run([sys.executable,'-B',str(self.module),'summary','--cases',str(inventory)],capture_output=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stdout)

    def test_native_spawn_failure_is_unperformed(self):
        _,result=self.execute(self.plan(argv=[str(self.root/'missing-program.exe')]))
        self.assertEqual(result['exit_code'],70)
        self.assertEqual(result['outcome'],'NOT_RUN')

    def test_input_mutation_during_trial_is_not_qualified(self):
        _,result=self.execute(self.plan("from pathlib import Path; Path(__file__).write_text('changed')"))
        self.assertFalse(result['input_unchanged'])
        self.assertEqual(result['outcome'],'NOT_RUN')

    def test_invalid_json_and_wrong_text_are_failed_outputs(self):
        _,result=self.execute(self.plan("from pathlib import Path; Path('a').write_text('not json')",expected_outputs=[dict(path='a',kind='json',value={},requirement_id='SVE-07'),dict(path='a',kind='text',value='different',requirement_id='SVE-07')]))
        self.assertEqual(result['outcome'],'FAIL')
        self.assertTrue(all(v['result']=='FAIL' for v in result['output_checks']))

    def test_plan_containment_unknown_fields_and_duplicate_assertions(self):
        output=dict(path='a',kind='exists',requirement_id='SVE-07')
        for index, updates in enumerate(({'unknown':1},{'inputs':[]},{'cwd':str(self.root)},
                                        {'expected_outputs':[output,output]}, {'prompt':{'path':'relative','sha256':'bad'}},
                                        {'dependencies':['other']}, {'dependency_attempts':{'other':'no'}})):
            with self.subTest(updates=updates),self.assertRaises(ValueError):
                self.runner.seal(self.plan(**updates),self.root/f'bad-{index}')
        path=self.plan()
        with self.assertRaises(ValueError): self.runner.seal(path,self.project/'evidence')

    def test_utility_failure_overrides_incomplete_in_summary(self):
        attempt,_=self.execute(self.plan(expected_outputs=[dict(path='a',kind='exists',requirement_id='SVE-07')]))
        value=self.runner.summarize([dict(case_id='case-1',attempt=str(attempt),dependencies=[]),dict(case_id='pending',attempt=None,dependencies=[])])
        self.assertEqual(value['outcome'],'FAIL')


if __name__ == '__main__': unittest.main()
