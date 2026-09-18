"""Bind unchanged real producer artifacts into fresh consumer contexts."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
from prepare_trials import RUN,PROJECT,CODEX,put,ref,binding

def prepare(ident,mode,producer):
    case=RUN/'trials'/ident;project=case/'project'
    producer_project=RUN/'trials'/producer/'project'
    producer_attempt=RUN/'trials'/producer/('attempt-002' if producer=='N01' else 'attempt-001')
    receipt=json.loads((producer_attempt/'result.json').read_bytes())
    if receipt['outcome']!='PASS' or not receipt['input_unchanged']:raise ValueError('Unqualified producer')
    paths=['AGENTS.md','input/request.md','docs/cli-contract.md','backlog/STORY-010.story.md']
    if mode=='qa':paths+=['docs/restore-guide.md']
    if mode=='resume':paths+=['evidence/story-create/STORY-010-session.md']
    for rel in paths:
        src=producer_project/rel;dest=project/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
        assert src.read_bytes()==dest.read_bytes()
    package='story-create' if mode=='resume' else 'dev' if mode=='dev' else 'qa'
    package_source=RUN/'source' if mode=='resume' else PROJECT/'.agents/skills'/package
    shutil.copytree(package_source,project/'.agents/skills'/package)
    if mode=='resume':put(project/'.agents/devforgeai/project-binding.json',binding(project))
    (project/'.trial-output').mkdir()
    scope={
      'resume':'Resume the completed story-authoring task using evidence/story-create/STORY-010-session.md and the actual existing STORY-010. This is a relocated disposable copy; the selected current project is this directory and its current binding is supplied. Preserve completed story and source bytes. Report the actual remaining work, if any; no new outcome is selected. Do not modify related records.',
      'dev':'This is the separately selected implementation request. Implement only backlog/STORY-010.story.md, using input/request.md and docs/cli-contract.md as governing sources. Create docs/restore-guide.md and perform the specified documentation checks. This request authorizes the guide and evidence/dev/ writes; the fixture prior authoring-only task does not restrict this newly selected implementation. Keep all supplied source/story/package bytes unchanged. Do not execute the documented fictional product command.',
      'qa':'Independently assess the current docs/restore-guide.md against backlog/STORY-010.story.md and its input/request.md and docs/cli-contract.md sources. This is product documentation QA. Write evidence only under evidence/qa/ and the final response. Keep candidate/source/story/package bytes unchanged. Do not execute the documented fictional product command.'}[mode]
    prompt=f'Use the {package} skill at {(project/".agents/skills"/package/"SKILL.md").as_posix()}. Selected project: {project.as_posix()}.\n{scope}\nWork only inside this disposable project; no network, installs, other checkout access or additional agents.\n'
    put(case/'prompt.txt',prompt)
    requirements=['SC-015'] if mode=='resume' else ['SC-016']
    outputs=[{'path':'.trial-output/final.txt','kind':'exists','requirement_id':requirements[0]}]
    if mode=='dev':outputs.append({'path':'docs/restore-guide.md','kind':'exists','requirement_id':requirements[0]})
    plan={'schema_version':'trial-plan-v1','case_id':ident,'kind':'native','argv':[str(CODEX),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output/final.txt'),'-'],'cwd':str(project),'permitted_write_root':str(project),'inputs':[ref(p) for p in project.rglob('*') if p.is_file()],'prompt':ref(case/'prompt.txt'),'requirement_ids':requirements,'dependencies':[producer],'dependency_attempts':{producer:str(producer_attempt)},'timeout_seconds':600,'expected_outputs':outputs}
    put(case/'plan.json',plan)
    put(case/'expected.json',{'case_id':ident,'source_handoff':[{'source':ref(producer_project/p),'consumer':ref(project/p)} for p in paths],'expected':'No story duplication or source changes; unchanged actual producer is consumable from explicit inputs.' if mode=='resume' else 'Guide satisfies the producer story AC1-AC5; no invented runtime claims; source/story/candidate bytes preserved as applicable. QA identifies actual requirement coverage with evidence.','mode':mode})
    print('Prepared',ident,mode,'from',producer,'without changing its artifacts')

if __name__=='__main__':
    if sys.argv[1:] == ['initial']:
        prepare('N11','resume','N01');prepare('N12','dev','N01')
    elif sys.argv[1:] == ['qa']:
        prepare('N13','qa','N12')
    else:raise SystemExit('initial or qa')
