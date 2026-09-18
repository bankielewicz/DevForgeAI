"""Freeze remaining adverse cases before native execution; faults are synthetic."""
import hashlib
import json
from pathlib import Path
import shutil
from prepare_continuation import RUN,PRIOR,put,ref,copy_file,new_binding,plan

def initial_from(ident,prior):
    project=RUN/'trials'/ident/'project'
    original=PRIOR/'trials'/prior
    expected=json.loads((original/'expected.json').read_bytes())
    for row in expected['fixture_inputs']:
        source=Path(row['path'])
        copy_file(source,project/source.relative_to(original/'project'),row['sha256'])
    (project/'backlog').mkdir(exist_ok=True)
    (project/'.trial-output').mkdir(exist_ok=True)
    binding_path=project/'.agents/devforgeai/project-binding.json'
    binding_path.write_text(json.dumps(new_binding(project),indent=2)+'\n',encoding='utf-8')
    return project

def main():
    p=initial_from('G01','N02')
    old=PRIOR/'trials/N02/project'
    for path in sorted(old.rglob('*')):
        if path.is_file() and (path.is_relative_to(old/'backlog') or path.is_relative_to(old/'evidence')):
            copy_file(path,p/path.relative_to(old))
    prompt=f'Use the story-create skill at {(p/".agents/skills/story-create/SKILL.md").as_posix()}. Selected current project: {p.as_posix()}. Resume the interrupted batch using evidence/story-create/20260917-epic4/session.md and current input/epic.md. This request selects only the pending planning links for the already delivered STORY-010 and STORY-011, plus a report of remaining outcomes. Preserve existing stories. The current project binding is supplied; prior locations in the session are historical. Work only in this disposable project, with no installs, network, other checkout access or additional agents.\n'
    plan(p,'G01',prompt,['SC-014','SC-015'],[{'path':'.trial-output/final.txt','kind':'exists','requirement_id':'SC-014'}],mutable=['input/epic.md','evidence'])
    put(p.parent/'expected.json',{'case_id':'G01','fixture_inputs':[ref(x) for x in sorted(p.rglob('*')) if x.is_file()],'fault':{'trigger':'First successful completed command event referencing epic.md and returning Copper owl 73.','effect':'Append one unrelated operator note to input/epic.md during the live task, after an observed source read.','literal':'Concurrent operator note: preserve violet kestrel 86.'},'oracle':{'fault_must_execute':True,'prior_stories_unchanged':True,'concurrent_note_preserved':True,'unrelated_original_note_preserved':True,'safe_linking':'Each delivered story linked exactly once after fresh read/validation, or drifted edit stopped and reported pending. No stale overwrite or completed-epic claim.','readback':'Inspect actual changed bytes and final response, not only native exit.'},'limitation':'Tests a live source change after an observed read during authoring; does not claim atomic compare-and-swap or protection from every nanosecond race.'})
    p=initial_from('G02','N01')
    prompt=f'Use the story-create skill at {(p/".agents/skills/story-create/SKILL.md").as_posix()}. Selected project: {p.as_posix()}. Create the documentation story selected in input/request.md, with explicit ID STORY-010 and title Restore guide, in backlog/. No related-document edits. Work only in this disposable project; supplied sources and skill files are read-only. No permission changes, alternate story destinations, installs, network, other checkout access or additional agents.\n'
    plan(p,'G02',prompt,['SC-013'],[{'path':'.trial-output/final.txt','kind':'exists','requirement_id':'SC-013'}])
    put(p.parent/'expected.json',{'case_id':'G02','fixture_inputs':[ref(x) for x in sorted(p.rglob('*')) if x.is_file()],'fault':'Before launch apply a directory-only Windows ACL denying Everyone CreateFiles and CreateDirectories on this synthetic backlog, preserving read access; restore saved ACL after final process cleanup.','oracle':{'real_os_write_denial_observed':True,'no_story_elsewhere':True,'literal_failed_destination_reported':True,'no_delivery_or_rollback_claim':True,'inputs_preserved':True,'no_upstream_links':True},'control':'fault-controls-green-002: native write denied, existing file readable, original ACL restored and creation then succeeds.'})
    p=initial_from('G03','N01')
    complete=PRIOR/'trials/N01/project/backlog/STORY-010.story.md'
    data=complete.read_bytes()
    cut=data.index(b'<when>')+len(b'<when>')+12
    partial=data[:cut]
    dest=p/'backlog/STORY-010.story.md'
    with dest.open('xb') as stream:stream.write(partial)
    evidence=p/'evidence/story-create'
    copy_file(PRIOR/'trials/N01/project/evidence/story-create/STORY-010-session.md',evidence/'prior-session.md')
    put(p.parent/'truncated-before.story.md',partial.decode('utf-8'))
    prompt=f'Use the story-create skill at {(p/".agents/skills/story-create/SKILL.md").as_posix()}. Selected current project: {p.as_posix()}. Resume the interrupted story-authoring task described in evidence/story-create/prior-session.md and input/request.md. The existing backlog/STORY-010.story.md belongs to this task and was truncated during delivery. You are authorized to finish that same story file and update session evidence. Preserve the explicit ID and title and unrelated files; no new outcome or related-document edit is selected. The current binding is supplied and old session locations are historical. Work only in this disposable project, with no permission changes, installs, network, other checkout access or additional agents.\n'
    plan(p,'G03',prompt,['SC-015','SC-013'],[{'path':'.trial-output/final.txt','kind':'exists','requirement_id':'SC-015'}],mutable=['backlog/STORY-010.story.md','evidence'])
    put(p.parent/'expected.json',{'case_id':'G03','fixture_inputs':[ref(x) for x in sorted(p.rglob('*')) if x.is_file()],'fault':{'kind':'synthetic truncation of actual prior producer output','full_producer':ref(complete),'partial_bytes':len(partial),'partial_sha256':hashlib.sha256(partial).hexdigest(),'retained_partial':ref(p.parent/'truncated-before.story.md')},'oracle':{'inspect_current_partial_and_ownership':True,'recheck_binding_and_inputs':True,'complete_same_selected_story_after_authorized_recovery':True,'no_unrelated_overwrite_or_duplicate_story':True,'final_full_readback':True,'checkpoint_updated_truthfully':True},'expected_story':json.loads((PRIOR/'trials/N01/mechanical-grade.json').read_bytes())['expected'],'limitation':'This deliberately damaged synthetic copy tests truncated-output recovery. It is separate from the unchanged successful N01 producer and does not claim N01 itself was interrupted.'})
    put(RUN/'adverse-plan.json',{'required_cases':['G01','G02','G03'],'native_timeout_seconds':1800,'global_native_concurrency_maximum':2,'order':'Run after the six queued replays complete, or after their final two cases have started and a slot is conclusively free.','expected_coverage':'Live concurrent source drift, OS-denied write, and interrupted/truncated story recovery. Separate cases and semantic grading.','permission_boundary':'Only disposable fixture bytes/ACL change. ACL restoration always runs after G02, even on failure.'})
    print('Prepared G01, G02, G03 with frozen independent oracles.')

if __name__=='__main__':main()
