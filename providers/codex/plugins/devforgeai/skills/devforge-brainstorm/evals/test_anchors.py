"""Discriminating anchor/legacy-locator fixtures for revision 003."""
import importlib.util
import unittest
from pathlib import Path
import check_anchors as checks

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('delivery_check',ROOT/'scripts/delivery_check.py')
delivery=importlib.util.module_from_spec(spec);spec.loader.exec_module(delivery)

def handoff():
    pairs=zip(checks.REQUIRED,['STATE-001','IO-001','CHANGES-001','VERIFY-001','NEXT-001','PROMPT-001','CUSTODY-001'])
    return '# Handoff\n\n'+'\n\n'.join('## '+title+' ['+identity+']' for title,identity in pairs)+'\n'

class Anchors(unittest.TestCase):
    def test_valid_missing_and_duplicate(self):
        text=handoff();self.assertEqual(checks.check_headings(text,True)['result'],'PASS')
        self.assertEqual(checks.check_headings(text.replace(' [IO-001]',''),True)['result'],'FAIL')
        self.assertEqual(checks.check_headings(text.replace('[IO-001]','[STATE-001]'),True)['duplicate_ids'],['STATE-001'])
        self.assertEqual(checks.check_headings(text.replace('## Resume and custody [CUSTODY-001]',''),True)['result'],'FAIL')

    def test_explicit_anchor_and_fenced_example(self):
        text=handoff().replace('## You are here [STATE-001]','<a id="STATE-001"></a>\n\n## You are here')
        text+='\n```markdown\n## Example without ID\n```\n'
        self.assertEqual(checks.check_headings(text,True)['result'],'PASS')
        self.assertEqual(checks.check_headings(text.replace('## You are here','## You are here [WRONG-001]'),True)['result'],'FAIL')

    def test_template_tables_and_outcome_scope(self):
        text=(ROOT/'assets/handoff.md').read_text()
        self.assertEqual(checks.check_headings(text,True)['result'],'PASS')
        self.assertEqual(checks.check_template_tables(text)['result'],'PASS')
        self.assertEqual(delivery.outcomes(text)['result'],'PASS')
        self.assertEqual(checks.check_template_tables(text.replace('| Order | Task |','| Sequence | Task |'))['result'],'FAIL')
        self.assertEqual(delivery.outcomes(text.replace('| NOT_RUN |','| Recorded externally |'))['result'],'FAIL')

    def test_legacy_rows_are_not_section_ids(self):
        legacy='# Ledger\n\n## Ideas and alternatives\n\n| Idea ID | Idea |\n| --- | --- |\n| IDEA-001 | First |\n| IDEA-002 | Second |\n'
        selected=['IDEA-001','IDEA-002']
        valid=checks.check_source_locators(legacy,[],selected,selected)
        self.assertEqual((valid['result'],valid['actual_section_ids']),('PASS',[]))
        self.assertEqual(checks.check_source_locators(legacy,selected,selected,selected)['result'],'FAIL')
        self.assertEqual(checks.check_source_locators(legacy,[],selected,['IDEA-001'])['lost_selected_rows'],['IDEA-002'])
        self.assertEqual(checks.check_source_locators(legacy,[],['IDEA-999'],['IDEA-999'])['result'],'FAIL')

if __name__=='__main__':unittest.main()
