"""Contract checks and independent controls for the native Codex grading adapter."""
from pathlib import Path
import re, tempfile, unittest
from grade_contract_eval import frontmatter, runtime_identity, skill_reads, source_grade

PACKAGE=Path(__file__).resolve().parents[1]
REPO=PACKAGE.parents[2]
class SharedContracts(unittest.TestCase):
    def test_shared_identity(self):
        for rel in ['references/policy.md','references/defaults.md','scripts/validate_policy.py','references/schemas/policy.schema.json','references/schemas/common.schema.json']:
            with self.subTest(path=rel):
                self.assertEqual((PACKAGE/'skills/prd'/rel).read_bytes(),(PACKAGE/'skills/architecture'/rel).read_bytes())
    def test_reference_script_and_schema_identity(self):
        for skill in ['prd','architecture']:
            for rel in ['scripts/validate_policy.py','references/schemas/policy.schema.json','references/schemas/common.schema.json']:
                with self.subTest(skill=skill,path=rel):
                    self.assertEqual((PACKAGE/'skills'/skill/rel).read_bytes(),(REPO/'src/claude/DevForgeAI/skills'/skill/rel).read_bytes())
                    if '/schemas/' in rel:self.assertEqual((PACKAGE/'skills'/skill/rel).read_bytes(),(REPO/'src/schemas'/Path(rel).name).read_bytes())
    def test_complete_case_counts(self):
        for skill,count in [('prd',29),('architecture',16)]:
            self.assertEqual(len(list((PACKAGE/'evals'/skill).glob('*/prompt.md'))),count)
        self.assertTrue((PACKAGE/'evals/prd/ignores-unrelated-request/prompt.md').is_file())
        self.assertFalse((PACKAGE/'evals/prd/ignores-unrelated-request/scaffold.sh').exists())

class EvaluatorControls(unittest.TestCase):
    def test_exact_identity_good_and_negative_controls(self):
        self.assertTrue(runtime_identity('gpt-example','gpt-example'))
        for wrong in ['claude-example','gpt-other','unavailable','unknown',None]:
            self.assertFalse(runtime_identity(wrong,'gpt-example'))
        self.assertFalse(runtime_identity('unavailable','unavailable'))
    def test_claude_family_regex_is_not_a_codex_identity_oracle(self):
        self.assertIsNone(re.search(r'^  model: "claude-[a-z0-9][a-z0-9.-]*"','  model: "gpt-example"'))
        self.assertTrue(runtime_identity('gpt-example','gpt-example'))
    def test_inline_frontmatter_dashes_do_not_end_metadata(self):
        self.assertEqual(frontmatter('---\nid: PRD-001\n# --- prd-specific ---\nstage: mvp\n---\nbody')['stage'],'mvp')
    def test_load_is_exact_successful_candidate_read(self):
        root=Path('/tmp/isolated/devforgeai')
        item={'id':'read','type':'commandExecution','exitCode':0,'cwd':'/tmp/isolated/project',
              'command':'cat ../devforgeai/skills/prd/SKILL.md','aggregatedOutput':'---\nname: prd\n---',
              'commandActions':[{'type':'read','path':'../devforgeai/skills/prd/SKILL.md'}]}
        self.assertTrue(skill_reads([item],'prd',root))
        self.assertFalse(skill_reads([{**item,'exitCode':1}],'prd',root))
        self.assertFalse(skill_reads([item],'prd',Path('/tmp/another/devforgeai')))
        self.assertFalse(skill_reads([{**item,'aggregatedOutput':'catalog entry prd'}],'prd',root))
    def test_absent_file_never_passes_negative_regex(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);g=p/'grader.md'
            g.write_text('---\ntype: regex\ntarget: {path: missing.md}\nmatch: not_contains\n---\nwrong\n')
            self.assertFalse(source_grade(g,p,'',{'arm':'plugin'},[],[])['passed'])
if __name__=='__main__':unittest.main()
