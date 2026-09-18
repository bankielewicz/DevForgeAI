"""Independent known-good and seeded-defect controls for mechanical grading."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from graders import grade_story

GOOD='''---
id: STORY-010
type: documentation
status: Backlog
sprint: Backlog
format_version: "0.1.0"
depends_on: []
pr_merged: false
---
## Description
Document the no-write dry-run contract.
## Acceptance Criteria
### AC#1: State preserved
```xml
<acceptance_criteria id="AC1"><given>A dry-run</given><when>The operator reads the guide</when><then>Destinations remain unchanged</then></acceptance_criteria>
```
## Technical Specification
```yaml
technical_specification:
  format_version: "2.0"
  components: []
  business_rules: []
  non_functional_requirements: []
```
No executable components: this story changes documentation only.
## Definition of Done
- [ ] Review documentation against the source.
'''
EXPECTED={'id':'STORY-010','type':'documentation','required_sections':['Description','Acceptance Criteria','Technical Specification','Definition of Done'],'required_literals':['dry-run','unchanged']}

class GraderTests(unittest.TestCase):
    def test_good(self):self.assertEqual(grade_story(GOOD,EXPECTED),[])
    def test_missing_section(self):self.assertIn('section_missing:Definition of Done',grade_story(GOOD.replace('## Definition of Done','## Omitted'),EXPECTED))
    def test_malformed_xml(self):self.assertIn('xml_invalid',grade_story(GOOD.replace('</then>','</wrong>'),EXPECTED))
    def test_duplicate_ac(self):self.assertIn('ac_duplicate:AC1',grade_story(GOOD+GOOD[GOOD.index('```xml'):GOOD.index('## Technical Specification')],EXPECTED))
    def test_checked_future_work(self):self.assertIn('premature_completion',grade_story(GOOD.replace('- [ ]','- [x]'),EXPECTED))
    def test_wrong_id(self):self.assertIn('metadata:id',grade_story(GOOD.replace('STORY-010','STORY-011'),EXPECTED))
    def test_duplicate_yaml(self):self.assertIn('frontmatter_invalid',grade_story(GOOD.replace('type: documentation','type: feature\ntype: documentation'),EXPECTED))
    def test_unfilled_template(self):self.assertIn('template_placeholder',grade_story(GOOD+'\n<Selected outcome>\n',EXPECTED))
    def test_wrong_technical_version(self):self.assertIn('technical_version',grade_story(GOOD.replace('"2.0"','"1.0"'),EXPECTED))
    def test_empty_then(self):self.assertIn('ac_empty:then',grade_story(GOOD.replace('Destinations remain unchanged',''),dict(EXPECTED,required_literals=[])))
    def test_no_ac(self):self.assertIn('ac_missing',grade_story(GOOD[:GOOD.index('```xml')],dict(EXPECTED,required_sections=[],required_literals=[])))
    def test_missing_frontmatter(self):self.assertIn('frontmatter_missing',grade_story('no metadata',EXPECTED))
    def test_scalar_frontmatter(self):self.assertIn('frontmatter_invalid',grade_story('---\nscalar\n---\n',EXPECTED))
    def test_missing_literal(self):self.assertIn('literal_missing:unchanged',grade_story(GOOD.replace('unchanged','preserved'),EXPECTED))
    def test_unresolved_implements(self):self.assertIn('implements_unresolved:GHOST',grade_story(GOOD.replace('id="AC1"','id="AC1" implements="GHOST"'),EXPECTED))
    def test_data_is_not_executed(self):self.assertEqual(grade_story(GOOD+'\nQuoted source command: touch forbidden.txt\n',EXPECTED),[])

if __name__=='__main__':unittest.main(verbosity=2)
