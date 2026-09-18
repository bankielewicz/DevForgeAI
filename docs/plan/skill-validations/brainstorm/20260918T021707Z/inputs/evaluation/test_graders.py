import unittest
from graders import grade_brief, SECTIONS

def valid():
    front = '---\nformat_version: brainstorm-brief-v1\nbrief_id: library\nrevision: 1\nupdated_at_utc: "2026-09-18T02:00:00Z"\ndisposition: READY_FOR_PRD\nsupersedes: null\n---\n'
    return (front + '\n'.join('## '+name+'\nIndependent synthetic content.\n' for name in SECTIONS)).encode()

class GraderTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual([], grade_brief(valid()))

    def test_reject_extra_metadata(self):
        data=valid().replace(b'brief_id: library',b'unknown: true\nbrief_id: library')
        self.assertIn('Metadata fields must match the six-field contract', grade_brief(data))

    def test_invalid_revision(self):
        for revision in (b'0',b'-1',b'true',b'"1"'):
            with self.subTest(revision=revision):
                self.assertTrue(grade_brief(valid().replace(b'revision: 1',b'revision: '+revision)))

    def test_invalid_id(self):
        for ident in (b'../escape',b'-start',b'x'*65):
            with self.subTest(ident=ident):
                self.assertTrue(grade_brief(valid().replace(b'brief_id: library',b'brief_id: '+ident)))

    def test_duplicate_metadata(self):
        self.assertTrue(grade_brief(valid().replace(b'revision: 1',b'revision: 1\nrevision: 2')))

    def test_timestamp(self):
        for stamp in (b'not-time',b'2026-02-31T12:00:00Z',b'2026-09-18T02:00:00+03:00'):
            with self.subTest(stamp=stamp):
                self.assertTrue(grade_brief(valid().replace(b'2026-09-18T02:00:00Z',stamp)))

    def test_disposition(self):
        self.assertTrue(grade_brief(valid().replace(b'READY_FOR_PRD',b'READY_FOR_IMPLEMENTATION')))

    def test_sections(self):
        for section in SECTIONS:
            with self.subTest(section=section):
                self.assertTrue(grade_brief(valid().replace(('## '+section).encode(),b'### Missing')))

    def test_unfilled_template(self):
        self.assertTrue(grade_brief(valid().replace(b'Independent synthetic content.',b'{{fill-me}}',1)))

    def test_supersedes(self):
        for prev in (b'"C:/outside/brief.md"',b'"../outside.md"',b'true'):
            with self.subTest(prev=prev):
                self.assertTrue(grade_brief(valid().replace(b'supersedes: null',b'supersedes: '+prev)))

    def test_bad_encoding_and_yaml(self):
        for data in (b'\xff',b'---\n[broken\n---\n',b'No header'):
            with self.subTest(data=data):
                self.assertTrue(grade_brief(data))

    def test_successor_requires_prior(self):
        self.assertTrue(grade_brief(valid().replace(b'revision: 1',b'revision: 2')))

if __name__ == '__main__':
    unittest.main()
