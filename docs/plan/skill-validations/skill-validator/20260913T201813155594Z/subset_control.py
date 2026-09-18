"""Independent eligible-subset control; synthetic retention records, no authoring."""
import json
import sys
from harness import RUN, TARGET, read, save, ref, execute, inventory
from probes import record_fixture

root,unused,counts=record_fixture('H11','pass')
original=json.loads(read(root/'inputs/selection.json'))
auth=original['authorization']
evidence=save(root/'inputs/project.json',dict(schema_version='project-evidence-v1',run_id='project',project_root=str(root),scope_roots=[str(root)],inputs=[auth],facts=[],exclusions=[],complete=True,capabilities=[],gaps=[]))
requirement=dict(id='R1',origin='derived',statement='Assess retained local responsibilities.',source_refs=[],rationale='Controlled selection/reduction fixture.',verification='Read preserved member and integration records.')
members=[dict(id=m['member_id'],name=m['package']['name'],role='core',action='retain',target_root=m['package']['root'],existing_package=m['package'],parent_core=None,responsibility='Retained local '+m['member_id'],exclusions=['External effects'],triggers=['Selected local request'],near_misses=['Installation'],requirement_ids=['R1'],fact_ids=[],rationale='Existing ordinary skill retained for structural record control.',depends_on=m['depends_on'],capabilities=[],lineage_delta=[]) for m in original['members']]
proposal=save(root/'inputs/proposal.json',dict(schema_version='adaptation-proposal-v1',run_id='proposal',mode='propose',project_evidence=ref(evidence),prior_proposal=None,requirements=[requirement],members=members,handoffs=original['handoffs'],gaps=[],state='NO_CHANGE'))
selection=save(root/'inputs/selected.json',dict(schema_version='adaptation-selection-v1',proposal=ref(proposal),member_ids=['A','B'],destinations=[dict(member_id=m['id'],target_root=m['target_root']) for m in members],authorization=auth,permitted_effects=['Synthetic read-only checks']))
authored=save(root/'inputs/retained.json',dict(schema_version='set-authoring-v1',run_id='retained',selection=ref(selection),ordered_member_ids=['A','B'],members=[dict(member_id=m['id'],status='RETAINED',authoring_record=None,validation_request=None,package=m['existing_package'],reason='Retained controlled fixture, no authoring execution claimed.',applied_paths=[]) for m in members],state='NO_CHANGE',validation_status='NOT_PERFORMED',testing_status='NOT_PERFORMED',issues=[]))
request=save(root/'inputs/request.json',dict(schema_version='set-validation-request-v1',run_id='subset',selection=ref(selection),set_authoring=ref(authored),scope='eligible_subset',members=[dict(member_id='A',package=original['members'][0]['package'],request=None,adaptive_descriptor=None)],handoffs=[],omitted_member_ids=['B'],omitted_handoff_ids=['transfer'],permission='Synthetic input, no external effects.'))
full=json.loads(read(root/'records/set-assessment.json'))
empty=save(root/'inputs/empty.jsonl',{})
# Use a real empty JSONL file, not a JSON object; no candidate executes setup code.
from harness import write
empty=write(root/'inputs/no-integration.jsonl',b'')
full.update(input=ref(request),scope='eligible_subset',members=full['members'][:1],integration_checks=ref(empty),omitted_member_ids=['B'],omitted_handoff_ids=['transfer'],required_total=29,required_evaluated=29)
save(root/'subset-records/set-assessment.json',full)
save(RUN/'expectations-H11-before-execution.json',dict(case_id='H11',expected_exit=0,expected_outcome='PASS',required_evaluated=29,required_total=29,omitted_members=['B'],omitted_handoffs=['transfer'],oracle='Builder 5.3: explicit dependency-closed eligible subset. Original full set remains unassessed.',fixture=inventory(root)))
r=execute('H11',[sys.executable,'-B','-X','utf8',str(TARGET/'scripts/adaptive_observe.py'),'records','--run-root',str(root/'subset-records')],root)
save(RUN/'results/H11.json',dict(case_id='H11',finding='QA-02',expected_exit=0,actual_exit=r['exit'],matched=r['exit']==0 and r['fixture_unchanged'],evidence=ref(RUN/'commands/H11/receipt.json',RUN)))
print('H11',r['exit'])
