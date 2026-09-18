"""Record primary-validator semantic adjudication and deterministic templates."""
import datetime as dt
import json
import re
from pathlib import Path
from bootstrap import RUN, ROOT, AUTHOR, write, ref

def main():
    spec=(RUN/'inputs/qa-skill-spec.md').read_text(encoding='utf-8')
    matches=[]
    for section,name in [('10.1','qa-report-template.md'),('10.2','qa-fix-template.md')]:
        block=spec.split('### '+section,1)[1].split('```markdown\n',1)[1].split('```',1)[0]
        actual=(RUN/'source/assets'/name).read_text(encoding='utf-8')
        matches.append({'template':name,'same_text_after_newline_normalization':actual==block,'specification':ref('inputs/qa-skill-spec.md'),'actual':ref('source/assets/'+name)})
    write('observations/template-comparison.json',matches)
    notes={
      'QA-001':('references/intake-planning.md','Explicit selected product QA scope, positive modes and excluded repair/skill-validation/install/deploy/research routing; discovery does not expand story selection.'),
      'QA-002':('SKILL.md','Defaults to plan, bars tests/builds/executable harnesses during planning, honors host Plan mode, and requires selected plan/candidate/effects for execute or retest.'),
      'QA-003':('references/intake-planning.md','Mandatory project/specification/scope/rules and optional handoff/baseline/results/checkpoint inputs are separated; missing candidate is a planning prerequisite, not fabricated readiness.'),
      'QA-004':('references/intake-planning.md','Literal output precedence and full components bound before writes; tools, layout and platform discovered; no intrinsic Git/MCP/framework or checkout relocation requirement.'),
      'QA-005':('references/intake-planning.md','Dirty/untracked Git or no-Git manifest, source/artifact correspondence, supplied evidence provenance and command effect inspection are explicit.'),
      'QA-006':('references/intake-planning.md','Every selected clause inventoried; duplicate IDs source-qualified; dependency context does not select dependency deliverables.'),
      'QA-007':('references/intake-planning.md','Conflicting or missing oracles, SLOs and prerequisites are owned decisions; no speculative requirements or root causes.'),
      'QA-008':('references/intake-planning.md','Cases carry criterion, fixture, environment, procedure, independent expected result, actual field, cleanup and evidence; metrics do not substitute for acceptance traceability.'),
      'QA-009':('references/intake-planning.md','Inspect assertion claims and plan justified negative controls in disposable copies without rewriting product or requiring exhaustive mutation testing.'),
      'QA-010':('references/execution-integrity.md','Mock decorators including aliases/wrappers/analogous attributes fail; syntax/import inspection required; vendor/text controls excluded; unknown dynamic code remains incomplete.'),
      'QA-011':('references/execution-integrity.md','Vacuous assertions, swallowed failures, fake boundaries, denominator manipulation, unjustified exclusions and altered expectations require evidence-backed failure; ordinary setup is distinguished.'),
      'QA-012':('assets/test-plan-template.md','Template has identities, criterion/case maps, risk, tools, effect boundaries, oracles, metrics, cleanup, entry/exit rules and handoff; ready steps cannot have unresolved slots.'),
      'QA-013':('references/execution-integrity.md','Reread selected plan/candidate; stop affected checks on drift; only authorized independent QA tests/fixtures and disposable instrumentation may be written.'),
      'QA-014':('references/execution-integrity.md','Real build/function/contract/integration behavior selected from actual specifications; help or compilation is not complete behavior.'),
      'QA-015':('references/execution-integrity.md','Relevant unit/regression/consumer/platform cases required and platform evidence kept distinct.'),
      'QA-016':('references/execution-integrity.md','Specification-driven recovery/security/performance/usability; actual rendered UI evidence distinct from CLI; missing budgets not invented.'),
      'QA-017':('references/execution-integrity.md','Receipts identify case/attempt, command/cwd/platform, fixtures/timing/exit/raw evidence/cleanup; statuses and retries preserved, no skipped credit.'),
      'QA-018':('references/assessment.md','Independent >=95% executed-line and required-unit floors, stricter policy, predeclared first-party/unit denominators, integer exact comparison, no rounding or retry/category inflation.'),
      'QA-019':('references/assessment.md','Confirmed failure dominates missing evidence; PASS needs all mandatory obligations and both metrics; no phase/release authority claim.'),
      'QA-020':('references/reporting-handoff.md','Required report template bound to actual plan/candidate/specification and read back at literal selected destination.'),
      'QA-021':('assets/qa-fix-template.md','Distinct complete fix packet captures exact clause, reproduction, expected/actual evidence, scope, correction, preservation and retest oracle; dev owns remediation.'),
      'QA-022':('references/reporting-handoff.md','OPEN/FIX_REPORTED/VERIFIED_FIXED/REOPENED states; only independently selected QA retest closes findings; preserve original evidence.'),
      'QA-023':('references/reporting-handoff.md','All outcomes end in actual paths, project/environment, next owner/action and usable prompt where appropriate.'),
      'QA-024':('references/reporting-handoff.md','Eight-field resolved dev prompt, actual host discovery, no guessed namespaces/install/auto-send, pending prerequisite when unavailable, conversation not shell syntax.'),
      'QA-025':('references/reporting-handoff.md','All nine resources have consumers; checkpoints own only recorded processes/state; final external manifest avoids circular report/fix hashes while preserving literal paths.'),
      'QA-026':('SKILL.md','Entrypoint preserves separate package validation ownership; authoring notes and bound manual packet assign evaluation to validator. Bundle execution is assessed separately in QV-21.')}
    rows=[]
    for rid,(path,reason) in notes.items():
        text=(RUN/'source'/path).read_text(encoding='utf-8')
        lines=text.splitlines()
        line=next((i for i,l in enumerate(lines,1) if rid in l),1)
        rows.append({'requirement':rid,'static_result':'PASS','subject_path':path,'locator':{'line_start':line,'line_end':min(len(lines),line+3)},'reason':reason,'evidence':[ref('source/'+path),ref('inputs/qa-skill-spec.md')]})
    write('observations/requirement-review.json',rows)
    write('observations/semantic-adjudication.json',{'reviewer':'primary validator; independent of authoring, not independent external security certification','placeholder_candidate':{'subject':'references/reporting-handoff.md','excerpt':'Do not emit `TODO`, `<project>`, guessed commands, or other unresolved placeholders','classification':'useful_instruction','disposition':'not a defect; the quoted tokens are forbidden runtime output, not unfinished instructions'},'snapshot_name':{'helper_result':'NOT_RUN','disposition':'source snapshot directory intentionally named source; bound original qa identity matches name: qa'},'unicode':'No candidates in complete captured text','resources':'All four references and three templates are reachable through explicit consumers; agents/openai.yaml is host metadata; no orphan file','ceremonial_review':[{'excerpt':'Both first-party executed-line coverage and required **unit-test** pass rate must meet >=95%','classification':'useful_instruction','reason':'Changes verdict by independently measurable thresholds; no framework enforcement claimed.'},{'excerpt':'Do not automatically invoke dev or another QA session.','classification':'useful_instruction','reason':'Preserves separate user-selected handoff and authorization.'},{'excerpt':'Publish the plan/report/fix at their bound output paths, read actual bytes back, and hash final versions.','classification':'useful_instruction','reason':'Concrete output delivery and byte-identity verification.'}],'security_scope':'Read all runtime text and declared effects; no executable runtime scripts, credential calls, deserialization or fixed network endpoints. Native adversarial decision trial is separately scoped; no exhaustive security claim.','context':'51,863 package bytes across nine files; no required token budget. Installed tiktoken encoding unavailable locally; no download.'})
    publication=json.loads((AUTHOR/'publication-readback.json').read_text())
    baseline=json.loads((AUTHOR/'authoring-baseline.json').read_text())
    manifest=json.loads((AUTHOR/'baseline-manifest.json').read_text())
    source=json.loads((RUN/'source-manifest.json').read_text())
    write('observations/publication-binding.json',{'state_matches':publication['state']=='PUBLISHED','package_matches':publication['package_digest']==source['package_digest'],'baseline_target_matches':baseline['target_root']==source['root'],'baseline_files_match':manifest['files']==source['files'],'reference_validation':'Every explicit custody Ref was read/hash-verified and captured by inputs/bootstrap.py; capture-index binds exact originals. No builder invoked.','history_kind':'authoring-v1 baseline; not legacy generated/adopted history'})
    print('Static requirements',len(rows),'templates',matches)

if __name__=='__main__':main()
