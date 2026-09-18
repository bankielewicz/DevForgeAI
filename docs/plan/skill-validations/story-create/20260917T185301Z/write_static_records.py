"""Create schema-1 records in a disjoint capsule; preserve raw attempts in place."""
import hashlib
import json
from pathlib import Path
import shutil

RAW=Path(__file__).resolve().parent
ROOT=RAW.with_name(RAW.name+'-records')

def copy(relative):
    src=RAW/relative;dest=ROOT/relative
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as stream:stream.write(src.read_bytes())
    assert dest.read_bytes()==src.read_bytes()

def write(relative,value):
    dest=ROOT/relative;dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('x',encoding='utf-8',newline='\n') as stream:json.dump(value,stream,indent=2,ensure_ascii=False);stream.write('\n')

def ref(relative):
    return {'path':relative,'sha256':hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()}

def main():
    original=json.loads((RAW/'source-manifest.json').read_bytes())
    current=json.loads((ROOT/'source-manifest.json').read_bytes())
    assert original['package_digest']==current['package_digest'] and original['files']==current['files']
    for relative in ['rule-set.json','sources.json','guidance/openai-build-skills.md','semantic-review.md','evaluator/references/adaptive-validation.md']:
        copy(relative)
    for path in (RAW/'inputs').rglob('*'):
        if path.is_file():copy(path.relative_to(RAW).as_posix())
    spec='inputs/repository/docs/plan/skill-authorings/story-create/20260917T182711Z-02/contract.json'
    write('origin-record.json',dict(schema_version='1',run_id=RAW.name,target_name='story-create',original_source_root=original['root'],manifest=ref('source-manifest.json'),specification=ref(spec),origin_kind='existing_spec',history_kind='observed',prior_evidence=ref('inputs/repository/docs/plan/skill-authorings/story-create/20260917T182711Z-02/authoring-record.json'),completeness='complete',uncertainties=['Authored 0.1.0 baseline is custody, not generated/adopted quality history.','Raw execution evidence remains in sibling run; this capsule binds retained copies without reinterpreting target/fixture JSON as schema-1 records.'],source_readback_state='NOT_RUN',historical_origin='Verified authored import; legacy generated/adopted quality history not claimed.'))
    specs=[
      ('W01','SKILL.md','Runtime prerequisite','Selected project and loaded package','Binding inputs and actual host Python','Observe binding before effects','MATCH/BOUND or named nonzero stop','W02','Stop product effects, report setup prerequisite','Bound task or explicit missing prerequisite'),
      ('W02','references/intake-and-scope.md','Inputs and scope','Binding match and authorized task','Request, current instructions, selected sources and story roots','Resolve scope, metadata, paths and collision-free identity','Concrete selected inputs/defaults or named decision','W03,W04,W05,W06,W07','Preserve inputs; ask material question; continue independent work','Scoped story task, proposal, or missing-input report'),
      ('W03','references/batch-and-dependencies.md','Select outcomes and decompose','Selected epic/batch/gap outcomes','Canonical clauses, existing stories and dependencies','Group outcomes and map ownership/ACs/dependency DAG','Selected complete outcome inventory with blockers','W07','Block dependents; preserve and continue independent members','Batch/proposal accounts for every selected outcome'),
      ('W04','references/architecture-seeds.md','Architecture seed ingestion','Selected architecture or seed','Raw HTML data island and documented schema','Validate data and map only selected seed with provenance','Unambiguous mapped seed; order not fabricated dependency','W03 or W07','Reject duplicate/malformed/unknown schema or seed','Grounded story task or precise input rejection'),
      ('W05','references/recommendations-and-gaps.md','Select and read the original entries','Selected QA/RCA recommendations','Actual source schema, IDs, cycle, evidence and verification','Validate full entries and preserve semantics and conditional RCA provenance','Each requested ID accounted for; exact REC-to-AC mapping','W03 or W07','Report invalid/unknown/closed entries before dependent writes','Grounded follow-up stories or empty/rejected input report'),
      ('W06','references/recommendations-and-gaps.md','Provenance and source-specific fields','Selected deferred obligation','Source story/epic, exact clause, gap ID and deferral/blocking facts','Verify actual uncovered obligation and avoid duplicate work','Source-grounded tracking outcome without closure claim','W03 or W07','Retain unresolved source/verification decisions','Tracking story or exact unresolved gap'),
      ('W07','references/acceptance-criteria.md','AC form','Resolved selected outcome','Clause map and source facts','Write unique well-formed observable XML ACs including adverse cases','Every selected requirement has an AC or explicit gap','W08','Do not invent numeric targets or authorize descope','Measurable requirements and unresolved decisions'),
      ('W08','references/technical-specification.md','Structured technical block','ACs and actual project interfaces','Applicable components, data/API contracts and constraints','Define grounded technical/document obligations and bidirectional tests','Resolvable technical IDs and planned verification','W09 or W10','Keep missing contracts/metrics explicit; no ready claim','Technical specification or documented non-applicability'),
      ('W09','references/ui-specification.md','Interfaces and interaction','Selected UI behavior','Existing design, components, actions and selected standards','Describe states, interfaces, layout and accessibility','UI states map to ACs and future verification','W10','Record missing essential UI decision','Embedded UI specification or justified absence'),
      ('W10','references/story-contract.md','Version and canonical template','Draft content and applicable branches','Actual current template and SECTION_MANIFEST','Assemble one story with provenance and unchecked obligations','Complete applicable 0.1.0 document, nested technical 2.0','W11','Resolve accidental examples, missing sections and contradictions','Reviewable single-file story draft'),
      ('W11','references/delivery-and-resume.md','Write and read back','Authorized draft and literal free destination','Live input identities, binding and current output state','Exclusive-create and completely read back output','Written bytes and readback/content evidence','W12,W13,W14','Retain denied/partial/uncertain output; no overwrite/relocation','Delivered or explicitly partial/unsaved story'),
      ('W12','references/delivery-and-resume.md','Related-document updates','Story delivery established and links authorized','Fresh selected epic/sprint/recommendation records','Idempotent identity-keyed link updates with reread and readback','Actual one-row links and preserved unrelated content','W14','Stop drifted edit; report delivered story and pending link separately','Truthful linked or partially linked planning result'),
      ('W13','references/delivery-and-resume.md','Interruption and partial batches','Batch/interruption or selected resume','Actual session, inputs, outputs, binding and owned handles','Recheck drift and continue only authorized unfinished work','No duplicate effects; current decisions and next action recorded','W02,W11,W12,W14','Poll same live handle; preserve partial outputs and blockers','Recoverable batch state and exact remaining action'),
      ('W14','references/delivery-and-resume.md','Final report and next consumer','Selected work exhausted or explicit blockers','Actual paths, clause coverage and outstanding obligations','Return literal artifacts, states and manual consumer handoff','Fresh consumer can inspect unchanged artifact and sources','terminal','Report limitations and missing capabilities; do not auto-run consumer','Stories and honest authoring report; implementation/QA separate')
    ]
    steps=[]
    for ident,file,section,entry,inputs,action,completion,next_step,failure,terminal in specs:
        steps.append(dict(step_id=ident,entrypoint=dict(ref('source/'+file),locator=section),entry_conditions=entry,inputs=[inputs],executor='Primary skill actor; read-only binding Python helper only at W01',action=action,outputs=[completion],completion_evidence=[completion],next_branch_targets=next_step,failure_route=failure,terminal_user_outcome=terminal))
    write('workflow-map.json',dict(schema_version='1',run_id=RAW.name,target_name='story-create',steps=steps))
    print('Created static records and',len(steps),'workflow steps in',ROOT)

if __name__=='__main__':main()
