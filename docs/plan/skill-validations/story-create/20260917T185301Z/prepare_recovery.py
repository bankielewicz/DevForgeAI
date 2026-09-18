"""Predeclare implicit selection and interrupted-batch recovery observations."""
import json
from pathlib import Path
import shutil
from prepare_trials import RUN,CODEX,put,ref,binding

def main():
    for ident in ['N14','N15']:
        case=RUN/'trials'/ident;project=case/'project'
        if ident=='N14':
            source=RUN/'trials/N06/project'
            shutil.copytree(source,project)
            prompt='Create a documentation story from input/request.md in backlog/. Selected project: '+project.as_posix()+'. Work only in this disposable project; preserve supplied inputs, do not install anything or access external services.\n'
            expected={'zero_stories':True,'binding_absent':True,'discovery':'Look for actual implicit selection and skill-entrypoint reads; output resemblance alone is insufficient.'}
            requirements=['AV-F03','SC-003']
        else:
            source=RUN/'trials/N02/project'
            result=json.loads((RUN/'trials/N02/attempt-001/result.json').read_bytes())
            assert result['timeout'] and result['cleanup']=='VERIFIED'
            shutil.copytree(source,project)
            # New operational identity belongs only to this disposable copy.
            path=project/'.agents/devforgeai/project-binding.json'
            path.write_text(json.dumps(binding(project),indent=2),encoding='utf-8')
            # A genuine input change after the retained checkpoint, before resumption.
            with (project/'input/epic.md').open('a',encoding='utf-8') as stream:stream.write('\nConcurrent operator note: preserve silver heron 42.\n')
            prompt='Use the story-create skill at '+(project/'.agents/skills/story-create/SKILL.md').as_posix()+'. Selected current project: '+project.as_posix()+'. This is a relocated disposable copy of an interrupted story batch. Resume using evidence/story-create/20260917-epic4/session.md, current input/epic.md and existing delivered stories. The prior process timed out and cleanup was verified; no actor is still running. Finish authorized remaining planning links and report unresolved outcomes. Preserve already delivered stories and current source content. Only this project is writable; no external services, installs or other checkout access.\n'
            expected={'existing_stories_unchanged':True,'no_duplicate_stories':True,'pending_links':'Actual existing STORY-010 and STORY-011 linked once where still needed.','source_drift':'Detect the changed epic and retain both Copper owl 73 and silver heron 42.','blocked_outcome':'EP-B remains unresolved; no full-epic implementation claim.','recovery_only':'Does not upgrade timed-out N02 to PASS.'}
            requirements=['SC-014','SC-015','AV-W02']
        put(case/'prompt.txt',prompt)
        immutable=[p for p in project.rglob('*') if p.is_file() and not (ident=='N15' and (p==project/'input/epic.md' or p.is_relative_to(project/'evidence')))]
        plan={'schema_version':'trial-plan-v1','case_id':ident,'kind':'native','argv':[str(CODEX),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output/final.txt'),'-'],'cwd':str(project),'permitted_write_root':str(project),'inputs':[ref(p) for p in immutable],'prompt':ref(case/'prompt.txt'),'requirement_ids':requirements,'dependencies':[],'timeout_seconds':600,'expected_outputs':[{'path':'.trial-output/final.txt','kind':'exists','requirement_id':requirements[0]}]}
        put(case/'plan.json',plan)
        put(case/'expected.json',{'case_id':ident,'oracle':expected,'inputs':[ref(p) for p in project.rglob('*') if p.is_file()]})
        print('Prepared',ident)

if __name__=='__main__':main()
