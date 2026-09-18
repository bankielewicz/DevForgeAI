"""Additional independently constructed lineage, set and custody scenarios."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_independent as base

base.FIXTURES = Path(base.external_fixtures) if base.external_fixtures else base.RUN / 'fixtures' / (base.PLATFORM+'-extended')
base.FIXTURES.mkdir(parents=True, exist_ok=True)
adaptive, authoring, save, sha, package = base.adaptive, base.authoring, base.save, base.sha, base.package

class Extended(base.Independent):
    def lineage(self):
        proposal,evidence,ref=self.proposal()
        core=self.root/'core/note-core'; core.mkdir(parents=True)
        (core/'SKILL.md').write_text('---\nname: note-core\ndescription: Notes\n---\n| ID | Requirement |\n| --- | --- |\n| R1 | Preserve note |\n| R2 | Preserve title |\n| R3 | Preserve date |\n',encoding='utf-8')
        rows,digest=package(core)
        parent={'name':'note-core','root':str(core),'manifest':save(self.root/'core-manifest.json',rows),'package_digest':digest}
        proposal['members']=proposal['members'][:1]
        member=proposal['members'][0]
        member.update(role='project_variant',parent_core=parent,requirement_ids=['R1','R2','R3'],lineage_delta=[{'requirement_id':'R'+str(i),'disposition':'retained','reason':'Preserve contract','replacement_requirement_ids':[]} for i in range(1,4)])
        proposal['requirements']=[{'id':'R'+str(i),'origin':'derived','statement':statement,'source_refs':[],'rationale':'Preserve selected parent','verification':'Inspect note'} for i,statement in enumerate(['Preserve note','Preserve title','Preserve date'],1)]
        return proposal,core

    def test_extra_lineage_complete(self):
        proposal,core=self.lineage(); before=package(core); adaptive.Reader().record(proposal); self.assertEqual(before,package(core))

    def test_extra_lineage_missing_row(self):
        proposal,core=self.lineage(); proposal['members'][0]['lineage_delta'].pop(); self.assertRaisesRegex(ValueError,'incomplete parent',adaptive.Reader().record,proposal)

    def test_extra_lineage_unauthorized_removed(self):
        proposal,core=self.lineage(); proposal['members'][0]['lineage_delta'][2]['disposition']='removed'; self.assertRaisesRegex(ValueError,'current user',adaptive.Reader().record,proposal)

    def test_extra_lineage_modified(self):
        proposal,core=self.lineage(); proposal['members'][0]['lineage_delta'][1].update(disposition='modified',replacement_requirement_ids=['R2']); proposal['requirements'][1]['statement']='Preserve full title'; before=package(core); adaptive.Reader().record(proposal); self.assertEqual(before,package(core))

    def test_extra_parent_missing_index(self):
        root=self.root/'core'; root.mkdir(); (root/'SKILL.md').write_text('No explicit requirements'); self.assertRaisesRegex(ValueError,'empty parent',adaptive.Reader().requirement_index,root)

    def retained(self):
        proposal,evidence,ref=self.proposal()
        for member in proposal['members']:
            root=Path(member['target_root']); root.mkdir(parents=True)
            (root/'SKILL.md').write_text('---\nname: '+member['name']+'\ndescription: Notes\n---\nWrite notes.\n')
            rows,digest=package(root)
            member.update(action='retain',existing_package={'name':member['name'],'root':str(root),'manifest':save(self.root/(member['id']+'-manifest.json'),rows),'package_digest':digest})
        proposal['state']='NO_CHANGE'
        selection=self.selection(proposal)
        selection_ref=save(self.root/'selection.json',selection)
        result={'schema_version':'set-authoring-v1','run_id':'case','selection':selection_ref,'ordered_member_ids':['A','B','C'],'members':[{'member_id':member['id'],'status':'RETAINED','authoring_record':None,'validation_request':None,'package':member['existing_package'],'reason':'Existing unchanged package','applied_paths':[]} for member in proposal['members']],'state':'NO_CHANGE','validation_status':'NOT_PERFORMED','testing_status':'NOT_PERFORMED','issues':[]}
        return proposal,selection,result

    def request(self,result,ids=None):
        ids=ids or ['A','B','C']
        return {'schema_version':'set-validation-request-v1','run_id':'case','selection':result['selection'],'set_authoring':save(self.root/'set-authoring.json',result),'scope':'full_set' if len(ids)==3 else 'eligible_subset','members':[{'member_id':row['member_id'],'package':row['package'],'request':None,'adaptive_descriptor':None} for row in result['members'] if row['member_id'] in ids],'handoffs':[],'omitted_member_ids':[x for x in ['A','B','C'] if x not in ids],'omitted_handoff_ids':[],'permission':'Assessment only; no external effects'}

    def test_extra_retained_set_full(self):
        _,_,result=self.retained(); request=self.request(result); adaptive.Reader().record(result); adaptive.Reader().record(request)

    def test_extra_subset_independent(self):
        _,_,result=self.retained(); request=self.request(result,['C']); adaptive.Reader().record(request)

    def test_extra_subset_dependency_rejected(self):
        _,_,result=self.retained(); request=self.request(result,['B']); self.assertRaisesRegex(ValueError,'dependency closed',adaptive.Reader().record,request)

    def test_extra_subset_false_full(self):
        _,_,result=self.retained(); request=self.request(result,['C']); request['scope']='full_set'; self.assertRaisesRegex(ValueError,'scope mismatch',adaptive.Reader().record,request)

    def test_extra_result_wrong_order(self):
        _,_,result=self.retained(); result['ordered_member_ids']=['B','A','C']; self.assertRaisesRegex(ValueError,'order',adaptive.Reader().record,result)

    def test_extra_authored_baseline_edit(self):
        first=self.publish(self.contract(),'first'); contract=self.contract('edit'); contract['prior']={'path':str(first/'authoring-baseline.json'),'sha256':sha((first/'authoring-baseline.json').read_bytes())}; contract['history_review']='Verified authored prior'; second=self.publish(contract,'second'); record=json.loads((second/'authoring-record.json').read_bytes()); self.assertEqual(record['prior_origin']['kind'],'authored'); self.assertEqual(record['authoring_state'],'AUTHORED')

    def test_extra_explicit_adoption_then_edit(self):
        target=self.root/'skills/note'; target.mkdir(parents=True); (target/'SKILL.md').write_text('---\nname: note\ndescription: Note\n---\nOriginal.\n'); before=package(target); contract=self.contract('adopt',target); path=self.root/'adopt-contract.json'; save(path,contract); run=self.root/'docs/plan/skill-authorings/note/adopt'; authoring.begin(path,run); self.assertEqual(authoring.publish(run)['state'],'AUTHORED'); self.assertEqual(package(target),before); next_contract=self.contract('edit'); next_contract.update(prior={'path':str(run/'authoring-baseline.json'),'sha256':sha((run/'authoring-baseline.json').read_bytes())},history_review='Verified explicit adoption'); edit=self.publish(next_contract,'edit'); self.assertEqual(json.loads((edit/'authoring-record.json').read_bytes())['prior_origin']['kind'],'adopted')

    def test_extra_user_edit_conflict(self):
        first=self.publish(self.contract(),'first'); target=self.root/'skills/note'; (target/'SKILL.md').write_text('User modified note\n'); contract=self.contract('edit'); contract.update(prior={'path':str(first/'authoring-baseline.json'),'sha256':sha((first/'authoring-baseline.json').read_bytes())},history_review='Verified baseline'); path=self.root/'edit-contract.json'; save(path,contract); run=self.root/'docs/plan/skill-authorings/note/edit'; authoring.begin(path,run); (run/'candidate/SKILL.md').write_text('Different candidate\n'); result=authoring.publish(run); self.assertEqual(result['state'],'BLOCKED'); self.assertEqual((target/'SKILL.md').read_text(),'User modified note\n'); self.assertFalse((run/'authoring-baseline.json').exists())

    def test_extra_concurrent_drift_preserved(self):
        target=self.root/'skills/note'; target.mkdir(parents=True); (target/'SKILL.md').write_text('Original'); contract=self.contract('edit'); path=self.root/'contract.json'; save(path,contract); run=self.root/'docs/plan/skill-authorings/note/drift'; authoring.begin(path,run); (run/'candidate/SKILL.md').write_text('Candidate'); (target/'SKILL.md').write_text('Concurrent user edit'); result=authoring.publish(run); self.assertIn(result['state'],('BLOCKED','PARTIAL')); self.assertEqual(result['applied_paths'],[]); self.assertEqual((target/'SKILL.md').read_text(),'Concurrent user edit'); self.assertFalse((run/'authoring-baseline.json').exists())

if __name__=='__main__':
    suite=unittest.TestSuite(Extended(name) for name in unittest.defaultTestLoader.getTestCaseNames(Extended) if name.startswith('test_extra_'))
    result=unittest.TextTestRunner(verbosity=2,resultclass=base.LedgerResult).run(suite)
    report_name=base.PLATFORM+'-extended-results'+('-native-root' if base.external_fixtures else '')+'.json'
    save(base.RUN/'reports'/report_name,{'fixture_root':str(base.FIXTURES),'source_root':str(base.BUILDER),'target_digest':'ecb5f8056f18e1d9889de0c829a7e8e48a6feafe1b8f29bc09718d226eb20099','tests_run':result.testsRun,'results':result.rows})
    sys.exit(not result.wasSuccessful())
