"""Independent contract expectations; deterministic checks never score semantics."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0,str(SCRIPTS))
import adaptive_contracts as contracts
import adaptive_observe as adaptive
import text_resources as text
import observe
import adaptive_fixtures as fixture


class AdaptiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='validator-adaptive-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_standalone_ordinary_and_topology(self):
        value = fixture.standalone(self.root)
        reader = contracts.Reader()
        reader.record(value)
        self.assertEqual(reader.intake(value),['A','B'])
        reader.readback()

    def test_complete_shared_request(self):
        value = fixture.shared(self.root)
        reader = contracts.Reader()
        reader.record(value)
        self.assertEqual(reader.intake(value),['A','B'])
        reader.readback()

    def test_versions_extra_keys_and_duplicate_keys(self):
        value = fixture.standalone(self.root)
        for field,new in [('schema_version','standalone-set-input-v9'),('extra',True),('run_id','bad/id')]:
            bad = {**value,field:new}
            with self.assertRaises(ValueError):
                contracts.Reader().record(bad)
        for raw in ('{"a":1,"a":2}','{"x":1e999}','{"x":NaN}'):
            with self.assertRaises(ValueError):
                observe.strict_json(raw)

    def test_exact_membership_omission_and_injection(self):
        value = fixture.shared(self.root)
        for mutate in (lambda x:x['members'].pop(),lambda x:x['members'].append(x['members'][0]),lambda x:x['members'][0].update(member_id='C'),lambda x:x.update(omitted_member_ids=['B'])):
            bad = copy.deepcopy(value)
            mutate(bad)
            with self.assertRaises(ValueError):
                contracts.Reader().record(bad)

    def test_stale_and_unexpected_package_files(self):
        value = fixture.standalone(self.root)
        package = Path(value['members'][0]['package']['root'])
        (package/'extra.txt').write_text('new bytes')
        with self.assertRaisesRegex(ValueError,'STALE_PACKAGE'):
            contracts.Reader().record(value)

    def test_reference_absolute_base_required(self):
        value = fixture.standalone(self.root)
        value['authorization']['path'] = 'authorization.txt'
        with self.assertRaisesRegex(ValueError,'absolute'):
            contracts.Reader().record(value)

    def test_dependency_cycles_and_missing_ids(self):
        for rows in ({'A':{'depends_on':['B']},'B':{'depends_on':['A']}},{'A':{'depends_on':['Z']}}):
            with self.assertRaises(ValueError):
                contracts.order(rows)

    def test_required_producer_dependency(self):
        value = fixture.standalone(self.root)
        value['members'][1]['depends_on'] = []
        with self.assertRaisesRegex(ValueError,'required producer'):
            contracts.Reader().record(value)

    def test_fail_precedes_unknown_and_advisory(self):
        a = text.check('AV-I01','SKILL.md','FAIL','Observed required defect.')
        b = text.check('AV-W01','SKILL.md','NOT_RUN','Unavailable native host.','unknown')
        c = text.check('AV-C01','SKILL.md','FAIL','Advisory only.',required=False)
        result = adaptive.reduction([a,b,c])
        self.assertEqual((result['outcome'],result['required_evaluated'],result['required_total'],result['unknown_applicability']),('FAIL',1,2,1))
        self.assertEqual(adaptive.reduction([b])['outcome'],'INCOMPLETE')
        c.update(applicability='not_applicable',result='NOT_APPLICABLE')
        self.assertEqual(adaptive.reduction([c])['outcome'],'NOT_APPLICABLE')

    def test_unicode_locations_preserved_and_unresolved(self):
        raw = 'مرحبا\nA\u202eB 👩\u200d💻\ufe0f\n'
        observed = text.candidates('SKILL.md',raw)
        bidi = next(x for x in observed if x['codepoint']=='U+202E')
        self.assertEqual((bidi['start_byte'],bidi['end_byte'],bidi['line'],bidi['column']),(len('مرحبا\nA'.encode()),len('مرحبا\nA\u202e'.encode()),2,2))
        self.assertTrue(all(x['disposition']=='unresolved' for x in observed))
        self.assertIn('U+200D',{x['codepoint'] for x in observed})

    def test_nfkc_command_candidate_and_safe_excerpt(self):
        observed = text.candidates('SKILL.md','Run `ｐython` with password=synthetic-secret.\n')
        self.assertTrue(any('NFKC' in x['reason'] for x in observed))
        self.assertTrue(all('secret' not in x['escaped_excerpt'] for x in observed))

    def test_multilingual_no_blanket_defect(self):
        self.assertEqual(text.candidates('SKILL.md','中文 العربية हिंदी café'),[])

    def test_inline_reference_images_and_anchors(self):
        content = '# Repeat\n# Repeat\nSetext\n------\n<span id="explicit"></span>\n'
        self.assertTrue({'repeat','repeat-1','setext','explicit'} <= text.anchors(content))
        source = '[one](ref.md#repeat-1) ![img][pic]\n[pic]: image.png\n```\n[ignored](absent)\n```\n'
        links,_ = text.links(source)
        self.assertEqual(len(links),2)
        self.assertEqual(text.resolve('SKILL.md',links[0][1],{'ref.md':content},{'ref.md','image.png'})[0],'resolved')
        self.assertEqual(text.resolve('SKILL.md','ref.md#other-renderer',{'ref.md':content},{'ref.md'})[0],'unsupported_anchor')

    def test_dynamic_outside_and_missing_distinguished(self):
        for target,expected in [('missing.md','missing'),('../outside.md','outside_scope'),('https://example.test/x','outside_scope'),('${dynamic}.md','dynamic')]:
            self.assertEqual(text.resolve('SKILL.md',target,{},set())[0],expected)

    def test_inline_code_and_balanced_parentheses_links(self):
        self.assertEqual(text.links('`[Example](missing.md)`')[0],[])
        self.assertEqual(text.links('[Guide](references/guide(v1).md)')[0],[(1,'references/guide(v1).md','link')])

    def test_raw_helper_cannot_hide_failure_or_adjudicate_candidates(self):
        row = text.check('AV-E01','records','FAIL','Seeded mismatch.')
        value = {'schema_version':'adaptive-check-observation-v1','command':'records','status':'OBSERVED','checks':[row],'observations':{'checked_records':[],'errors':['mismatch']},'limitations':['Limited structural evidence.']}
        fixture.write(self.root/'raw.json',value)
        self.assertTrue(adaptive.records(self.root)[1])

    def test_metadata_preserves_optional_and_rejects_duplicates(self):
        good = '---\nname: sample\ndescription: Work on the supplied input.\ncompatibility: Python\nmetadata:\n  category: testing\n---\n'
        self.assertEqual(text.frontmatter(good)['compatibility'],'Python')
        with self.assertRaises(Exception):
            text.frontmatter(good.replace('name: sample','name: sample\nname: duplicate'))

    def test_exact_counts_no_token_guess(self):
        package = fixture.package(self.root,'sample')
        path = Path(package['root'])/'SKILL.md'
        data = path.read_bytes()
        checks,observations,_ = text.package(path.parent)
        row = observations['context']['files'][0]
        self.assertEqual((row['bytes'],row['characters'],row['lines'],row['tokens']),(len(data),len(data.decode()),len(data.decode().splitlines()),None))
        self.assertEqual(next(x for x in checks if x['rule_id']=='AV-C01')['result'],'PASS')

    def test_invalid_utf8_is_not_skipped(self):
        package = fixture.package(self.root,'sample')
        (Path(package['root'])/'bad.md').write_bytes(b'\xff')
        checks,_,_ = text.package(package['root'])
        self.assertTrue(any(x['subject_path']=='bad.md' and x['result']=='FAIL' for x in checks))

    def test_placeholder_and_unlinked_license_not_auto_defects(self):
        package = fixture.package(self.root,'sample')
        root = Path(package['root'])
        (root/'LICENSE').write_text('Permission to use this fixture.\n')
        with (root/'SKILL.md').open('a') as stream:
            stream.write('\nExample literal `TODO` for parser tests.\nMUST verify the output schema before reporting.\n')
        checks,observations,_ = text.package(root)
        self.assertFalse(any(x['result']=='FAIL' for x in checks))
        self.assertEqual(next(x for x in observations['resources'] if x['path']=='LICENSE')['usage'],'unresolved_usage')

    def test_helper_usage_rejects_encoding_without_tokenizer(self):
        run = subprocess.run([sys.executable,'-B','-X','utf8',str(SCRIPTS/'adaptive_observe.py'),'package','--source',str(self.root),'--encoding','cl100k_base'],capture_output=True,timeout=30)
        self.assertEqual(run.returncode,2)
        self.assertFalse(run.stdout)

    def test_unknown_tokenizer_cannot_import_arbitrary_module(self):
        with self.assertRaises(ValueError):
            text.local_tokenizer('os','encoding')

    def test_new_records_do_not_recurse_into_fixture_authority(self):
        value = fixture.standalone(self.root/'inputs')
        fixture.write(self.root/'standalone-set-input.json',value)
        fixture.write(self.root/'trials/fixture/findings.json',{'schema_version':'evil'})
        checked,errors = adaptive.records(self.root)
        self.assertEqual(errors,[])
        self.assertEqual(checked,['standalone-set-input.json'])

    def test_check_reference_keeps_run_relative_base(self):
        raw = self.root/'observation.txt'
        raw.write_text('observed')
        row = text.check('AV-E01','SKILL.md','PASS','Observed bytes.')
        ref = fixture.reference(raw)
        row['evidence'] = [ref]
        with self.assertRaises(ValueError):
            adaptive.check_rows(json.dumps(row).encode(),self.root)
        ref['path'] = raw.name
        self.assertEqual(len(adaptive.check_rows(json.dumps(row).encode(),self.root)),1)

    def test_record_unknown_versions_and_unjustified_na(self):
        fixture.write(self.root/'new.json',{'schema_version':'adaptive-observations-v8'})
        self.assertTrue(adaptive.records(self.root)[1])
        row = text.check('AV-E01','SKILL.md','NOT_APPLICABLE','Unknown','unknown')
        with self.assertRaises(ValueError):
            adaptive.check_rows(json.dumps(row).encode(),self.root)

    def test_parent_requirement_inventory_not_heading_match(self):
        for text_value in ('# REQ-1\nTODO','# No inventory\n'):
            with self.assertRaises(ValueError):
                contracts.parent_requirements(text_value)
        rows = contracts.parent_requirements('| ID | Requirement |\n| --- | --- |\n| R1 | Preserve input bytes. |\n')
        self.assertEqual(rows['R1']['statement'],'Preserve input bytes.')

    def test_readback_detects_late_added_file(self):
        value = fixture.standalone(self.root)
        reader = contracts.Reader()
        reader.record(value)
        (Path(value['members'][0]['package']['root'])/'late.txt').write_text('drift')
        with self.assertRaisesRegex(ValueError,'SOURCE_CHANGED'):
            reader.readback()


if __name__ == '__main__':
    unittest.main()
