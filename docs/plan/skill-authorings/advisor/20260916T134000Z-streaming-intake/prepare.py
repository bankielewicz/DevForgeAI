"""Capture the selected authoring contract before staging; no product execution."""
import hashlib
import json
from pathlib import Path

ROOT = Path('C:/Projects/DevForgeAI')
HERE = Path(__file__).resolve().parent
def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
def ref(path):
    path = path.resolve()
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

capture = '''# Selected advisor progress integration

User request: "perhaps, the advisor skill needs a powershell harness such as the one provided by claude as an example. how to we integrate it into the advisor skill?"
User selection after the concrete integration proposal: "proceed".

Approved scope: develop src/agents/skills/advisor with a thin PowerShell 5.1/7 launcher and optional streaming progress in the existing Python runner, then independent skill-validator evaluation. Preserve operational .agents/skills/advisor, advisor-test.ps1, historical evidence and the Rust worker. Do not call Claude for the exhausted historical review. No installation or new paid model call is part of this deterministic implementation/validation.

The selected proposal keeps auth, attempt/budget limits, evidence and response validation in Python; uses stream-json --verbose for optional progress; keeps progress on stderr and final JSON on stdout; retains raw streams plus final result and response; versions new streaming receipts while reading v1; bounds execution through EOF/process exit/cleanup; rejects missing/duplicate/malformed terminal output; records costs even on budget failures without claiming independent billing enforcement. Distinguish process completion, structurally valid advice and reviewer verdict.

History inspected: initial skill-creator build and direct auth fix exist, but no compatible builder baseline or custody history. Contract history_review=no_known_history denotes that precise builder fact, not absence of known origin. Source and installed package matched 16/16 before this task. This is a focused observed edit, not whole-package adoption.

TDD and independent skill evaluation are explicitly selected together. Authoring records remain authoring-only; separate validation evidence binds exact resulting bytes. Python and PowerShell are skill support resources, never protected framework authority.
'''
(HERE / 'task-capture.md').write_text(capture, encoding='utf-8')
inputs = [ref(HERE/'task-capture.md'), ref(ROOT/'advisor-test.ps1'),
          ref(ROOT/'docs/plan/advisor-build/20260915-initial/report.md'),
          ref(ROOT/'docs/plan/advisor-auth-fix/20260916T033234Z/report.md'), ref(ROOT/'AGENTS.md')]
requirements = [
 ('AP-01', 'Thin PS5.1/7 launcher accepts Request, Briefing, RunDir, Reason, Python and ShowProgress, forwards exact arguments and exit status to Python without policy duplication.', ['scripts/advisor.ps1']),
 ('AP-02', 'Optional --show-progress uses stream-json --verbose; elapsed progress and periodic waiting messages go only to stderr. Default quiet json command and legacy v1 interpretation are preserved.', ['scripts/advisor_run.py','scripts/advisor_stream.py']),
 ('AP-03', 'Drain stdout/stderr concurrently, retain raw bytes, require one well-formed final result object last in the stream; reject malformed JSON, non-object events, missing or duplicate results and nonfinite/duplicate JSON values.', ['scripts/advisor_stream.py','scripts/advisor_run.py']),
 ('AP-04', 'A monotonic reviewer deadline includes pipe EOF and actual child exit. Timeout/cancellation cleanup is bounded by a separate 5-second ceiling; record direct-child and pipe cleanup observations without claiming detached-descendant qualification.', ['scripts/advisor_stream.py']),
 ('AP-05', 'Streaming attempts use advisor-execution-v2, retain raw stdout/stderr, parsed result.json when valid framing permits, response.md only for valid successful advice; verify all derived artifacts and transport observations on follow-up while accepting exact v1 history.', ['scripts/advisor_run.py']),
 ('AP-06', 'Nonzero exit, timeout, interruption, malformed stream or failed result never yields advice. Retain finite reported cost on failed terminal envelopes, compare with reserved cap and expose discrepancy; never reclaim budget or silently retry.', ['scripts/advisor_run.py']),
 ('AP-07', 'Preserve immutable requests, max-two attempts, restricted read-only flags and child-only auth filtering. Progress displays allowlisted event/tool metadata only, not model text, tool arguments, credential values or untrusted terminal escapes.', ['scripts/advisor_stream.py','scripts/advisor_run.py']),
 ('AP-08', 'Document development and operational commands, receipt compatibility, progress limitations and test denominator. Preserve existing tests; add Python JSONL cases and deterministic expected values plus targeted negative and real native subprocess tests.', ['SKILL.md','references/execution.md','references/evaluation.md','tests/test_streaming.py','evals/cases.jsonl','evals/case.schema.json','evals/run_evaluation.py','artifact-manifest.json'])]
behaviors = []
for ident, outcome, artifacts in requirements:
    behaviors.append({'id':ident, 'requirement_ids':[ident], 'trigger':'Selected advisor run or package verification',
        'inputs':['Immutable request and complete briefing; selected CLI presentation mode'],
        'completion':outcome, 'outputs':['Retained evidence or explicit failure with no valid advice'],
        'resource_paths':artifacts, 'prerequisites':['Native Windows, Python >=3.10; PowerShell 5.1 or 7 for wrapper'],
        'effects':['Fresh run evidence only; no parent environment, operational package or prior evidence edits'],
        'failure':'Retain failure evidence; never relax auth, flags, limits or validation.',
        'recovery':'Investigate preserved failure; only authorized remaining attempt may use same immutable request.'})
resources=[]
for path in sorted({p for _,_,paths in requirements for p in paths}):
    helper=path.startswith('scripts/') or path=='evals/run_evaluation.py'
    resources.append({'path':path,'kind':'helper' if helper else 'reference',
       'purpose':'Implement or explain the selected progress integration and evidence boundary',
       'load_when':'Advisor invocation or independent package evaluation',
       'helper_contract':{'inputs':'Explicit request/run/briefing/reason and optional progress; deterministic cases for evaluator',
          'outputs':'Final JSON on stdout, optional safe progress on stderr and retained evidence files',
          'runtime':'Windows Python >=3.10 standard library; launcher Windows PowerShell 5.1 or PowerShell 7',
          'effects':'One bounded subprocess attempt or deterministic evaluation; never framework acceptance',
          'errors':'Runner 0 valid response, 1 completed invalid/failed attempt, 2 blocked input/history; wrapper propagates child status',
          'reuse_reason':'Centralize validation/evidence and avoid duplicating policy in shell'} if helper else None})
design={'schema_version':'authoring-design-v1','target_name':'advisor','source_refs':inputs,
 'behaviors':behaviors,'resources':resources,
 'adverse_conditions':[{'id':'NEG-'+ident,'behavior_id':ident,'condition':'Invalid input, interrupted/failed execution or mismatched evidence',
      'expected_observation':'Explicit retained failure, no fabricated advice or implicit retry', 'requirement_basis':outcome} for ident,outcome,_ in requirements],
 'execution_limits':[{'behavior_id':'AP-04','seconds':300,'kind':'specified_requirement','source_basis':'Existing advisor default request timeout; selected request may explicitly use 1..1800 seconds'},
                     {'behavior_id':'AP-04','seconds':5,'kind':'execution_ceiling','source_basis':'Bounded helper cleanup ceiling selected for this implementation; uncertain cleanup is reported, never passed'}],
 'open_questions':[]}
save('workflow-design.json',design)
paths=sorted({p for _,_,ps in requirements for p in ps})
save('authoring-contract.json',{'schema_version':'authoring-contract-v1','run_id':'20260916T134000Z-streaming',
 'project_root':str(ROOT),'target_root':str(ROOT/'src/agents/skills/advisor'),'target_name':'advisor','operation':'edit',
 'authorization':'User selected proceed for development-only streaming progress integration followed by independent skill-validator evaluation; no operational installation or paid reviewer invocation.',
 'history_review':'no_known_history','change_paths':paths,
 'requirements':[{'origin':'user','outcome':ident+': '+outcome,'artifacts':ps} for ident,outcome,ps in requirements],
 'capabilities':['Native PowerShell launch','Bounded Python streaming transport','Legacy-compatible evidence'],
 'expected_outputs':['Optional live stderr progress','Final JSON receipt','Raw streams and validated response'],
 'side_effects':['Create fresh review evidence and one read-only reviewer attempt when explicitly invoked'],
 'inputs':inputs+[ref(HERE/'workflow-design.json')],
 'known_issues':['No live Claude qualification selected; shell/subprocess validation uses synthetic native fixtures.',
                 'No independent billing enforcement; configured CLI caps and reported cost may differ.',
                 'No protected framework authority or operational installation in this assignment.']})
save('preservation-before.json',{'git_metadata_present':(ROOT/'.git').exists(),
 'operational':{p.relative_to(ROOT/'.agents/skills/advisor').as_posix():ref(p)['sha256'] for p in sorted((ROOT/'.agents/skills/advisor').rglob('*')) if p.is_file()},
 'example':ref(ROOT/'advisor-test.ps1')})
print(HERE/'authoring-contract.json')
