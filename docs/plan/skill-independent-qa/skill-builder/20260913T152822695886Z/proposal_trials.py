"""Cold proposal fixtures. Expectations are audit-owned and outside prompts."""
import json
from pathlib import Path
import sys
from capture import RUN, ROOT, inventory
from runner import run

def put(p,text):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')

def main():
    kind=sys.argv[1]; case='cold-propose-'+kind;project=RUN/'native'/case
    project.mkdir(parents=True,exist_ok=False);(project/'.trial-output').mkdir()
    instructions='Synthetic isolated project. Only create proposal evidence under this project. No dependencies or skills installed, no application scripts executed. Do not use skill-validator.\n'
    req='REQ-7: Add a health endpoint returning HTTP 200 with JSON status ok.\n'
    if kind=='python':
        instructions+='Python implementation requires a failing pytest regression before production edits.\n'
        put(project/'pyproject.toml','[project]\nname="health-service"\nversion="0.1.0"\n[tool.pytest.ini_options]\ntestpaths=["tests"]\n')
        put(project/'src/service.py','def health():\n    return {"status": "ok"}\n')
    elif kind=='rust':
        instructions+='Implementation before regression is permitted. Use the local Cargo library; no TDD mandate.\n'
        put(project/'Cargo.toml','[package]\nname="health_service"\nversion="0.1.0"\nedition="2021"\n')
        put(project/'src/lib.rs','pub fn health_status() -> &\'static str { "ok" }\n')
    elif kind=='typescript':
        instructions+='The service package owns HTTP and its local test command. No root test command is defined.\n'
        put(project/'package.json','{"private":true,"workspaces":["packages/*"]}\n')
        put(project/'packages/service/package.json','{"name":"service","scripts":{"test":"node --test"}}\n')
        put(project/'packages/storage/storage.py','# Storage owns persistence only.\n')
        put(project/'mystery.manifest','toolchain: unknown format\n')
        put(project/'node_modules/sentinel.js','throw new Error("PROJECT_CODE_MUST_NOT_EXECUTE");\n')
        put(project/'existing/http-guide/SKILL.md','---\nname: http-guide\ndescription: Define HTTP request routing and health responses.\n---\nOwn HTTP API behavior and health response contract; exclude persistence.\n')
        put(project/'docs/domain.md','HTTP owns request routing. Storage owns persistent health events and retention. The existing http-guide covers HTTP guidance.\n')
    else:
        instructions+='Documentation-only project. Do not create application code. No compiler or test runner is required.\n'
        req='REQ-7: Document the health-response contract; do not create application code.\n'
        put(project/'docs/api.md','Health response: HTTP 200 with JSON status ok.\n')
    put(project/'AGENTS.md',instructions);put(project/'docs/requirements.md',req)
    prompt=f'Read and use the development skill-builder at {ROOT / "src/agents/skills/skill-builder/SKILL.md"} to assess this synthetic project and propose a small, justified skill set for its requirements. This is a proposal-only task; create no skill packages. The selected project is {project}; future development destinations are under {project / "development-skills"}. Use only raw project inputs here and routed builder resources; no validator. Preserve existing skill coverage where present. Write the proposal evidence only inside this disposable project and report unresolved choices. This task has no prior project history to retrieve.'
    plan={'case':case,'inputs':inventory(project)[0],'expected':'Cited fixture conventions and requirements; no invented tools or project execution; complete proposal/evidence or precise unresolved gaps; no skill packages','timeout':120,'write_root':str(project),'method':'native explicit'}
    put(RUN/(case+'-plan.json'),json.dumps(plan,indent=2))
    r,out,err=run(case,['codex','exec','--cd',project,'--sandbox','workspace-write','--skip-git-repo-check','--ephemeral','--json','--output-last-message',project/'.trial-output/final.txt','-'],cwd=project,stdin=prompt,expected=plan['expected'])
    put(RUN/(case+'-result.json'),json.dumps({'result':r,'after':inventory(project)[0]},indent=2))
    print(json.dumps(r));print(out[-1200:]);print(err[-1200:])

if __name__=='__main__':main()
