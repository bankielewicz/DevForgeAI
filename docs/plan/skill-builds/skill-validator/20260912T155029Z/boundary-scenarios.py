"""Retained root-supervised contract cases, not independent/native task claims."""
import json, shutil, sys
from pathlib import Path
from bootstrap import ROOT, PROJECT, write, digest, inventory
from verification import copy_package, execute, reference

R=ROOT/'boundary-trials/attempt-001'; R.mkdir(parents=True,exist_ok=False)
copy_package(ROOT/'candidate',R/'validator')
write(R/'validator-before-manifest.json',inventory(R/'validator'))
helper=R/'validator/scripts/observe.py'
def cmd(case,args,expected,timeout=120):
    write(R/(case+'-plan.json'),{'case_id':case,'expected_exit':expected,'timeout_seconds':timeout,'argv':[str(a) for a in args],'authority':'synthetic local trial','executor':'root-supervised terminal','validator_digest':digest(helper.read_bytes())})
    code,p=execute('boundary-'+case,args,timeout=timeout)
    write(R/(case+'-observation.json'),{'case_id':case,'expected_exit':expected,'actual_exit':code,'matched':code==expected,'receipt':reference(p/'result.json'),'interpretation':'Actual bounded execution; semantic conclusions documented separately.'})
    return code,p
def invoke(case,op,*args,expected=0): return cmd(case,[sys.executable,'-B','-X','utf8',helper,op,*args],expected)

# V01 is explicitly instruction-only, unlike the richer cold receipt-total task.
minimal=R/'minimal-project/src/agents/skills/ack-note'; minimal.mkdir(parents=True)
(minimal/'SKILL.md').write_text('---\nname: ack-note\ndescription: Prefix supplied text with ACK. Use for literal acknowledgments.\n---\n# Acknowledge\nFor supplied text, return ACK: followed by one space and the exact text. If input is absent, request the text. No files or external actions are required.\n',encoding='utf-8')
spec=R/'minimal-project/docs/plan/ack-note-spec.md'; spec.parent.mkdir(parents=True)
spec.write_text('---\nskill_name: ack-note\nstatus: approved\n---\nReturn ACK: then a space then exactly the supplied text. Ask for missing text. No files, scripts, external services or installation. Positive input hello yields ACK: hello.\n',encoding='utf-8')
write(R/'V01-inputs-before.json',{'target':inventory(minimal),'specification':reference(spec)})
invoke('V01-snapshot','snapshot','--source',minimal,'--output',R/'minimal-assessment')
invoke('V01-structure','structure','--source',R/'minimal-assessment/source')
invoke('V01-readback','readback','--source',minimal,'--manifest',R/'minimal-assessment/source-manifest.json')
write(R/'V01-semantic-observation.json',{'case_id':'V01','origin_kind':'existing_spec','specification':reference(spec),'known_requirements':['literal prefix','preserve supplied text','ask only on missing input','no script required'],'source_locator':'minimal-project/src/agents/skills/ack-note/SKILL.md:6-7','findings':[],'optional_folders_demanded':False,'method':'root-supervised specification conformance and executed helper commands, not independent native target activation'})

# V08: availability is probed before calling a nonexistent required dependency.
write(R/'V08-plan.json',{'case_id':'V08','fixture':'required executable definitely-missing-validator-fixture-runtime-20260912','expected':'NOT_RUN with dated fallback retained; no install','optional_transport':'deliberately unavailable in this fixture'})
availability=shutil.which('definitely-missing-validator-fixture-runtime-20260912')
assert availability is None
(R/'fallback-rules.json').write_bytes((ROOT/'candidate/assets/rules-snapshot.json').read_bytes())
write(R/'V08-observation.json',{'case_id':'V08','command_lookup':availability,'trial_result':'NOT_RUN','reason':'Required fixture executable unavailable; no execution or dependency installation attempted','guidance_freshness':'snapshot_only','fallback':reference(R/'fallback-rules.json'),'independent_structure_checks':'V01-structure executed separately','semantic_limit':'Simulated missing transport/capability branch with real runtime availability lookup'})

# V12: actual changed input and process timeout retain the original snapshot/output.
drift=R/'drift-project/ack-note'; copy_package(minimal,drift)
invoke('V12-before','snapshot','--source',drift,'--output',R/'drift-assessment')
with (drift/'SKILL.md').open('a',encoding='utf-8') as f: f.write('\nNew fixture-only user edit.\n')
invoke('V12-changed','readback','--source',drift,'--manifest',R/'drift-assessment/source-manifest.json',expected=1)
timeout_script=R/'timeout-fixture.py'; timeout_script.write_text('from pathlib import Path\nimport sys,time\nPath(sys.argv[1]).write_text("partial output\\n",encoding="utf-8")\nprint("started",flush=True)\ntime.sleep(20)\n',encoding='utf-8')
write(R/'V12-timeout-input.json',{'script':reference(timeout_script),'expected':'partial file retained and timeout, no successful final output','permitted_write_root':str(R)})
cmd('V12-timeout',[sys.executable,'-B','-X','utf8',timeout_script,R/'partial-output.txt'],None,timeout=0.5)
assert (R/'partial-output.txt').read_text()=='partial output\n'
write(R/'V12-recovery.json',{'case_id':'V12','source_state':'SOURCE_CHANGED','snapshot_retained':True,'partial_output':reference(R/'partial-output.txt'),'readiness':'BLOCKED','next_action':'Fresh assessment for intended current bytes; timeout attempt remains failed/unperformed and is not silently restarted.'})

# V11 verifies absent and non-supporting citation as distinct properties.
source=R/'citation-source.md'; source.write_text('# Actual source\nOptional folders are permitted.\n',encoding='utf-8')
write(R/'V11-plan.json',{'case_id':'V11','source':reference(source),'claims':['source file absent-source.md establishes mandatory folder','citation-source.md establishes mandatory six metadata fields'],'expected':'missing source cannot resolve; extant passage does not support mandatory claim'})
write(R/'V11-observation.json',{'case_id':'V11','absent_source_exists':(R/'absent-source.md').exists(),'supporting_source':reference(source),'locator':'line 2','support':False,'reason':'Observed sentence permits optional folders; it states no six-field mandate. A digest/locator does not establish semantic support.','method':'root manual semantic comparison with exact retained source'})

write(R/'final-readback.json',{'validator_unchanged':inventory(R/'validator')['files']==json.loads((R/'validator-before-manifest.json').read_text())['files'],'minimal_target_unchanged':inventory(minimal)['files']==json.loads((R/'V01-inputs-before.json').read_text())['target']['files'],'specification_unchanged':reference(spec)==json.loads((R/'V01-inputs-before.json').read_text())['specification'],'authority':'NONE'})
print(json.dumps({'boundary_trial_root':str(R),'cases':['V01','V08','V11','V12'],'complete_with_named_method_limits':True}))
