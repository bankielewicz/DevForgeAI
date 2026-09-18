"""Requirement-derived custody tests. No production edits or builder-authored oracles."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from prepare_validation import ROOT, put, sha
sys.path.insert(0,str(ROOT/'source/scripts'))
import authoring as a

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def ref(path): return {'path':str(path),'sha256':sha(path)}
class DesignTests(unittest.TestCase):
    def setUp(self):
        self.root=ROOT/'trials'/'independent-linux'/self._testMethodName
        self.root.mkdir(parents=True,exist_ok=False)
        self.target=self.root/'skills space Ω'/'sample-skill'
        self.run=self.root/'docs/plan/authoring/run1'
        self.input=self.root/'input'/'requirements.txt'
        self.input.parent.mkdir()
        self.input.write_text('R1: Return supplied text without modification. No runtime file or network effects.',encoding='utf-8')
        self.design=self.root/'input'/'design.json'
        self.value={'schema_version':'authoring-design-v1','target_name':'sample-skill','source_refs':[ref(self.input)],'behaviors':[{'id':'B1','requirement_ids':['R1'],'trigger':'User supplies text','inputs':['Supplied text'],'completion':'Return text exactly','outputs':['Chat response with supplied content'],'resource_paths':['SKILL.md'],'prerequisites':[],'effects':[],'failure':'Missing text: ask for it','recovery':'No persistent effects; user may supply text again'}],'resources':[{'path':'SKILL.md','kind':'instruction','purpose':'Transform supplied text','load_when':'Skill selected','helper_contract':None}],'adverse_conditions':[],'execution_limits':[],'open_questions':[]}
        self.contract=self.root/'input'/'contract.json'
        self.c={'schema_version':'authoring-contract-v1','run_id':'run1','project_root':str(self.root),'target_root':str(self.target),'target_name':'sample-skill','operation':'create','authorization':'Synthetic fixture authoring within this case only.','history_review':'no_known_history','change_paths':['SKILL.md'],'requirements':[{'origin':'user','outcome':'Return supplied text unchanged.','artifacts':['SKILL.md']}],'capabilities':[],'expected_outputs':[],'side_effects':[],'inputs':[],'known_issues':[]}
    def inputs(self,raw=None):
        if raw is None: write(self.design,self.value)
        else: self.design.write_bytes(raw)
        self.c['inputs']=[ref(self.input),ref(self.design)]
        write(self.contract,self.c)
    def stage(self,design=True):
        self.inputs()
        result=a.begin(self.contract,self.run,self.design if design else None)
        self.assertEqual(result['state'],'STAGED')
        (self.run/'candidate/SKILL.md').write_text('---\nname: sample-skill\ndescription: Return supplied text unchanged.\n---\nReturn supplied text exactly.\n',encoding='utf-8')
    def reject(self):
        self.inputs()
        with self.assertRaises((ValueError,OSError)): a.begin(self.contract,self.run,self.design)
        self.assertFalse(self.run.exists())
        self.assertFalse(self.target.exists())
    def blocked(self):
        result=a.publish(self.run)
        self.assertIn(result['state'],['BLOCKED','PARTIAL'])
        self.assertFalse((self.run/'publication-readback.json').exists())
        return result
    def test_valid_capture_and_publication(self):
        self.stage()
        capture=json.loads((self.run/'design-capture.json').read_bytes())
        self.assertEqual(capture['source_ref'],ref(self.design))
        self.assertEqual(capture['snapshot_ref'],ref(self.run/'inputs/1'))
        self.assertEqual(self.design.read_bytes(),(self.run/'inputs/1').read_bytes())
        self.assertEqual(a.publish(self.run)['state'],'AUTHORED')
        self.assertEqual((self.target/'SKILL.md').read_bytes(),(self.run/'candidate/SKILL.md').read_bytes())
        self.assertTrue((self.run/'publication-readback.json').exists())
        text=(self.run/'validator-request.md').read_text(encoding='utf-8')
        for content in [sha(self.design),str(self.input),'NOT_PERFORMED','Independently derive','not observed behavior','Source action: created']: self.assertIn(content,text)
    def test_wrong_target(self):
        self.value['target_name']='other'; self.reject()
    def test_unknown_root_field(self):
        self.value['surprise']=True; self.reject()
    def test_unknown_behavior_field(self):
        self.value['behaviors'][0]['surprise']=True; self.reject()
    def test_duplicate_behavior_id(self):
        self.value['behaviors'].append(copy.deepcopy(self.value['behaviors'][0])); self.reject()
    def test_duplicate_resource_path(self):
        self.value['resources'].append(copy.deepcopy(self.value['resources'][0])); self.reject()
    def test_duplicate_adverse_id(self):
        row={'id':'A1','behavior_id':'B1','condition':'Missing input','expected_observation':'Ask','requirement_basis':'R1'}
        self.value['adverse_conditions']=[row,row]; self.reject()
    def test_duplicate_question_id(self):
        row={'id':'Q1','question':'Which encoding?','owner':'user','affected_behavior_ids':['B1']}
        self.value['open_questions']=[row,row]; self.reject()
    def test_unknown_question_behavior(self):
        self.value['open_questions']=[{'id':'Q1','question':'Which encoding?','owner':'user','affected_behavior_ids':['MISSING']}]; self.reject()
    def test_undeclared_resource(self):
        self.value['behaviors'][0]['resource_paths']=['missing.md']; self.reject()
    def test_traversal_resource(self):
        self.value['resources'][0]['path']='../outside.md'; self.reject()
    def test_absolute_resource(self):
        self.value['resources'][0]['path']='C:/outside.md'; self.reject()
    def test_empty_array_member(self):
        self.value['behaviors'][0]['inputs']=['']; self.reject()
    def test_blank_completion(self):
        self.value['behaviors'][0]['completion']='  '; self.reject()
    def test_nonhelper_contract(self):
        self.value['resources'][0]['helper_contract']={k:'value' for k in ['inputs','outputs','runtime','effects','errors','reuse_reason']}; self.reject()
    def test_helper_missing_contract(self):
        self.value['resources'][0]['kind']='helper'; self.reject()
    def test_unknown_limit_behavior(self):
        self.value['execution_limits']=[{'behavior_id':'missing','seconds':120,'kind':'execution_ceiling','source_basis':'Trial'}]; self.reject()
    def test_boolean_seconds(self):
        self.value['execution_limits']=[{'behavior_id':'B1','seconds':True,'kind':'execution_ceiling','source_basis':'Trial'}]; self.reject()
    def test_nonfinite(self):
        self.inputs(json.dumps(self.value).replace('"open_questions": []','"open_questions": NaN').encode())
        with self.assertRaises(ValueError): a.begin(self.contract,self.run,self.design)
        self.assertFalse(self.run.exists())
    def test_duplicate_json_key(self):
        self.inputs(json.dumps(self.value).replace('"target_name":','"target_name":"x", "target_name":').encode())
        with self.assertRaises(ValueError): a.begin(self.contract,self.run,self.design)
        self.assertFalse(self.run.exists())
    def test_unselected_source(self):
        other=self.root/'other.txt'; other.write_text('Unselected',encoding='utf-8')
        self.value['source_refs']=[ref(other)]; self.reject()
    def test_unbound_design(self):
        self.inputs(); self.c['inputs']=[ref(self.input)]; write(self.contract,self.c)
        with self.assertRaises(ValueError): a.begin(self.contract,self.run,self.design)
        self.assertFalse(self.run.exists())
    def test_wrong_design_digest(self):
        self.inputs(); self.c['inputs'][1]['sha256']='0'*64; write(self.contract,self.c)
        with self.assertRaises(ValueError): a.begin(self.contract,self.run,self.design)
        self.assertFalse(self.run.exists())
    def test_original_design_changed(self):
        self.stage(); self.design.write_bytes(self.design.read_bytes()+b' '); self.blocked(); self.assertFalse(self.target.exists())
    def test_original_design_deleted(self):
        self.stage(); self.design.unlink(); self.blocked(); self.assertFalse(self.target.exists())
    def test_snapshot_changed(self):
        self.stage(); (self.run/'inputs/1').write_bytes(b'changed'); self.blocked(); self.assertFalse(self.target.exists())
    def test_snapshot_deleted(self):
        self.stage(); (self.run/'inputs/1').unlink(); self.blocked(); self.assertFalse(self.target.exists())
    def test_capture_changed(self):
        self.stage(); p=self.run/'design-capture.json'; p.write_bytes(p.read_bytes()+b' '); self.blocked()
    def test_capture_deleted(self):
        self.stage(); (self.run/'design-capture.json').unlink(); self.blocked()
    def test_binding_deleted(self):
        self.stage(); p=self.run/'origin.json'; value=json.loads(p.read_bytes()); del value['design_capture_ref']; write(p,value); self.blocked()
    def test_silent_legacy_downgrade(self):
        self.stage(); p=self.run/'origin.json'; value=json.loads(p.read_bytes()); value['design_capture_requested']=False; del value['design_capture_ref']; write(p,value); (self.run/'design-capture.json').unlink(); (self.run/'inputs/1').write_bytes(b'changed'); self.blocked()
    def test_legacy_design_shaped_input(self):
        self.stage(False); self.assertEqual(a.publish(self.run)['state'],'AUTHORED'); self.assertFalse((self.run/'design-capture.json').exists())
    def test_publication_interrupted(self):
        self.c['change_paths'].append('extra.txt'); self.stage(); (self.run/'candidate/extra.txt').write_text('second',encoding='utf-8')
        def fault(path):
            if path=='extra.txt': raise OSError('Independent simulated write interruption')
        result=a.publish(self.run,before_write=fault)
        self.assertEqual(result['state'],'PARTIAL'); self.assertEqual(result['applied_paths'],['SKILL.md']); self.assertTrue((self.target/'SKILL.md').exists()); self.assertFalse((self.run/'authoring-baseline.json').exists())
    def test_unchanged_authoring(self):
        self.target.mkdir(parents=True); (self.target/'SKILL.md').write_text('unchanged',encoding='utf-8'); self.c['operation']='edit'; self.inputs(); a.begin(self.contract,self.run,self.design)
        result=a.publish(self.run); self.assertEqual(result['state'],'AUTHORED'); self.assertEqual(result['applied_paths'],[])
        text=(self.run/'validator-request.md').read_text(encoding='utf-8'); self.assertIn('Source action: unchanged',text); self.assertIn('NOT_PERFORMED',text)
    def test_independent_validator_intake(self):
        self.stage(); self.assertEqual(a.publish(self.run)['state'],'AUTHORED')
        sys.path.insert(0,str(ROOT.parents[4]/'.agents/skills/skill-validator/scripts'))
        import authoring_intake
        request=self.run/'validation-request.json'
        self.assertEqual(authoring_intake.intake(request,sha(request))['status'],'BOUND')
        self.design.write_bytes(self.design.read_bytes()+b' ')
        with self.assertRaises(ValueError): authoring_intake.intake(request,sha(request))

if __name__=='__main__': unittest.main()
