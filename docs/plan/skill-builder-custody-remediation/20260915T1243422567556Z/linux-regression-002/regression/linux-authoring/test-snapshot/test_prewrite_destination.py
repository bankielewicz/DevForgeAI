"""Independent actual-destination preservation at first stage recheck."""
import json
import unittest
import test_publication as t

class PrewriteDestination(unittest.TestCase):
    setUp=t.PublicationTests.setUp
    stage=t.PublicationTests.stage
    def test_first_prewrite_stage_drift_leaves_no_destination(self):
        self.stage()
        def drift(path):
            origin=json.loads((self.run/'origin.json').read_bytes())
            origin['unexpected']=True
            t.write_json(self.run/'origin.json',origin)
        result=t.authoring.publish(self.run,before_write=drift)
        self.assertEqual('BLOCKED',result['state'])
        self.assertEqual([],result['applied_paths'])
        self.assertFalse(self.target.exists(),'BLOCKED pre-write rejection must not leave an occupied destination')
        self.assertFalse((self.run/'authoring-baseline.json').exists())
