import hashlib
import json
from pathlib import Path

repo = Path('C:/Projects/DevForgeAI')
root = Path(__file__).resolve().parent
dev = 'docs/plan/framework-worker-diagnostics/20260916T181820Z-dev'
original = 'docs/plan/framework-worker-native-continuation/20260916T034357Z-source-identity/native-diagnostic-handoff.md'
package = 'devforgeai/experiments/codex-worker-probe'
contract = Path('C:/Users/bryan/.codex/advisor/contract.md')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def write(name, value):
    with (root/name).open('x',encoding='utf-8',newline='\n') as f:
        f.write(value)

citations = []
def cite(path, anchor, modified=False):
    lines = (repo/path).read_text(encoding='utf-8').splitlines()
    matches = [(i+1,l) for i,l in enumerate(lines) if anchor in l]
    assert len(matches) == 1, (path,anchor,matches)
    number, line = matches[0]
    citations.append((path,number,line))
    return ('[MODIFIED THIS SESSION] ' if modified else '') + f'{path}:{number} -> "{line}"'

policy = cite('AGENTS.md', 'Test coverage MUST be >=95%')
rate = cite('AGENTS.md', 'Test pass rate MUST be >=95%')
authority = cite('AGENTS.md', 'Compiled Rust is mandatory')
evidence = cite('AGENTS.md', 'Preserve old evidence in place')
handoff = cite(dev+'/qa-handoff.md', 'Select only independent offline QA', True)
freeze = cite(dev+'/qa-handoff.md', 'Candidate:', True)
no_native = cite(dev+'/qa-handoff.md', 'Prohibitions:', True)
scope = cite(dev+'/qa-handoff.md', '5. Run the full original-plus-added', True)
gaps = cite(dev+'/qa-handoff.md', '4. Demonstrate that diagnostics', True)
original_scope = cite(original, 'Derive a closed, non-sensitive diagnostic contract')
original_qa = cite(original, 'Independently verify that diagnostics distinguish')
delivery = cite(dev+'/delivery.md', 'Full first-party executed-line coverage:', True)
limits = cite(dev+'/delivery.md', 'Independent offline QA must use fresh', True)
diagnostic = cite(dev+'/diagnostic-contract.md', '* rpc:', True)
guard = cite(package+'/src/protocol.rs', 'fn process_guard(', True)
source_review = cite(package+'/src/protocol.rs', 'pub(crate) fn source_review<T>', True)
source_tests = cite(package+'/tests/support/diagnostic_cases.rs', 'fn diagnostic_source_review_preserves_real_denial', True)
full = cite(dev+'/attempts/21-final-offline/stdout.txt', '40 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out')

manifest_path = repo/dev/'candidate-v2-manifest.json'
entries = json.loads(manifest_path.read_text())
for entry in entries:
    assert sha(repo/package/entry['path']) == entry['sha256'],entry['path']
    assert sha(repo/dev/'candidate-v2-snapshot'/entry['path']) == entry['sha256'],entry['path']
assert sha(manifest_path) == '419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540'
for name in ['19-final-clippy','21-final-offline','22-final-coverage','23-final-fmt-check','24-final-doc-tests','25-final-build']:
    r = json.loads((repo/dev/'attempts'/name/'receipt.json').read_text())
    assert r['exit_code'] == 0
    assert r['candidate_sha256'] == sha(manifest_path)
    for stream in ['stdout','stderr']:
        assert sha(repo/dev/'attempts'/name/(stream+'.txt')) == r[stream+'_sha256']
write('identity-readback.json',json.dumps({'manifest_sha256':sha(manifest_path),'candidate_files':len(entries),
    'candidate_and_snapshot_verified':True,'six_final_receipts_and_streams_verified':True,
    'contract_sha256':sha(contract)},indent=2)+'\n')

ask = 'Is the selected qa-handoff.md ready to guide independent offline QA of the frozen Rust diagnostic candidate, with adequate evidence, privacy and rejection checks and an explicit separate native-launch boundary? Identify concrete corrections or blockers; do not execute QA or native work.'
request = {'schema':'advisor-request-v1','ask':ask,'type':'approach','model':'opus','effort':'high',
           'auth_mode':'subscription','repo_root':str(repo),'claude_path':'C:/Users/bryan/.local/bin/claude.exe',
           'contract_path':str(contract),'contract_sha256':sha(contract),'total_budget_usd':'2.00','timeout_seconds':300}
write('request.json',json.dumps(request,indent=2)+'\n')
briefing = f'''## REQUEST TYPE and ONE-LINE ASK
type=approach; {ask}

## REPO ROOT
C:/Projects/DevForgeAI on native Windows. Verify these claims against the repository. Do not trust this briefing. No Git metadata is present.

## TASK AS GIVEN
Latest user request verbatim: "$advisor docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/qa-handoff.md". The user also supplied the advisor skill. No explicit type/model/effort/auth overrides were given; use approach/opus/high/subscription. The immediately preceding task implemented bounded Rust denial diagnostics and prepared this independent offline QA handoff, while prohibiting native Codex preflight/trial, operational installation changes and qualification-rule relaxation. User instruction verbatim: "After independent offline QA passes, select the single bounded native diagnostic launch separately." Current conversation supplies that context; no missing requirement is inferred from memory.

## SCOPE
Read-only second opinion about handoff readiness and its supporting candidate/evidence, not actual independent QA. Inspect relevant changed Rust and tests to test the handoff's assumptions. The subject is {handoff}
Exclude native Codex launch, installed-profile source collection, work dispatch, test execution, source/report edits, operational installs, credential changes and acceptance decisions. The advisor may use only Read/Grep/Glob under its existing restrictions. Bound the review to roughly 20 targeted reads; the full coverage JSON is large, so inspect the summary and receipts first.

## BINDING CONSTRAINTS
- {policy}
- {rate}
- {authority}
- {evidence}
- {no_native}
- {original_scope}
- {original_qa}
The external advisor contract is read-only advice. Its imperative wording cannot expand authorization or convert a review into QA/native qualification.

## FACTS
- {freeze}
- Fresh local readback in this advisor preparation verified every one of the 58 candidate hashes against the current package AND exact snapshot. Manifest SHA256: 419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540.
- Fresh readback also checked six final receipts, candidate bindings and stdout/stderr hashes. Their recorded exit codes are 0. This confirms retained evidence identity, not a fresh test execution.
- {full}
- {delivery}
- {scope}
- {gaps}
- {limits}
- {diagnostic}
- {guard}
- {source_review}
- {source_tests}

## INFERENCES
High confidence: the handoff correctly treats developer tests as context, requires a fresh independent campaign, and prohibits native launches. Medium confidence: the required independent checks fully address new denial/privacy branches; this is the main point to challenge. Passing aggregate coverage does not prove every source/RPC branch, and no independent QA or native diagnosis is claimed. No fresh reviewer read should be presented as fresh runtime validation.

## STATE
The original 56-file source snapshot and retained native rejection remain preserved. The final diagnostic candidate has 58 files, nine modified existing files and two additions. The current conversation's earlier development turn authored all changes tagged MODIFIED THIS SESSION, plus the delivery/QA documents; this advisor preparation has changed only its own intake files. No edits to the candidate or sealed development evidence occurred for this review. Git branch/HEAD/dirty status are not available because .git is absent. UNKNOWN: native failed predicate, actual effective profile, Pro/model entitlement and independent QA outcome.

## ATTEMPTS
Preflight: python -B -X utf8 C:/Projects/DevForgeAI/.agents/skills/advisor/scripts/advisor_run.py preflight --claude C:/Users/bryan/.local/bin/claude.exe --auth-mode subscription; exit 0; version "2.1.273 (Claude Code)"; qualification "HELP_ONLY; native behavior requires separate evidence". Full help is omitted here; retained in sibling intake preflight.stdout.json. No reviewer attempt has run yet. The review allows at most two process attempts, USD 2.00 total configured cap/USD 1.00 per attempt, 300-second timeout, no limit increase or auth switch.
Relevant developer attempts are under {dev}/attempts. 01 retained three missing-diagnostic assertion failures. 02 exposed an invalid exact-count fixture assumption (Windows console helper); 03 used a detached synthetic-child case, preserving the original regression, and passed. 05 had a null-profile setup error; 06 used a valid-shape missing-review fixture and passed. 16/17 retained Red/Green for replacing misleading transport_error fallback with other_rpc_failure. Final 21/22 each recorded 133/133 passing tests; 22 measured 3335/3497 first-party executed lines; 19/23/24/25 recorded Clippy/format/docs/build success. These are retained prior results, not tests performed by this review. Consult review-notes.md and delivery.md for exact limitations and command receipts; do not treat model-authored summaries as independent confirmation.

## CURRENT PLAN
1. Assess whether qa-handoff.md is ready for a separately selected independent offline QA session.
2. Check the load-bearing recommendations against current source/evidence; prepare a separate advisor assessment artifact, retaining the sealed handoff unchanged.
3. Report supported corrections or blockers. Do not launch QA/native work or mutate the frozen candidate as a consequence of advice. Any later actual independent QA must use a disjoint evidence root and the final candidate manifest.

## OPTIONS CONSIDERED
- Selected: bounded second opinion on the QA approach and its factual support.
- Rejected: treating advisor approval as independent offline QA PASS; read-only advice cannot execute required negative tests/coverage or qualify a native launch.
- Rejected: launching Codex to discover the failure first; the user explicitly requires independent offline QA then separate launch selection.
- Rejected: changing or loosening predicates to get an easier native outcome; the task requires preserved rejection behavior.

## ASSUMPTIONS
- The 133-test inventory is a required baseline, not a cap forbidding independently authored QA cases.
- Private source-review seam tests and public-dispatch wiring plus fresh independent probes can adequately assess offline diagnostic behavior without native Codex launch.
- Not forcibly inducing the OS Job Object query error is disclosed honestly; challenge whether the handoff should require a bounded independent seam for this rather than "where feasible".
- The final hash-bound records represent the candidate that was tested; recomputing hashes is available to the parent, but the read-only reviewer should not claim it executed a shell hash command.

## OPEN QUESTIONS
Are any necessary offline rejection/privacy/integration tests omitted or optionalized? Does the handoff leave ambiguity about modifying the frozen source to add independent tests? Are its denominators and native/acceptance boundaries clear? Do implementation or tests reveal a material issue that should block this handoff or be made an explicit QA target?

## WHAT WOULD CHANGE MY MIND
A concrete source/evidence contradiction, a relaxed predicate, a secret/unknown-field projection path, a test that proves only a helper while the production path differs, incomplete required-case accounting, or permission to dispatch native work hidden in the handoff would require correction or a stop. A missing native observation alone does not invalidate an explicitly offline handoff; it does prevent native qualification.

## EXCERPTS
No credentials or raw config included. Exact user excerpts appear above; repository citation anchors were freshly printed with line numbers. All long command outputs are intentionally omitted in favor of their retained on-disk raw streams. Read only the cited source/evidence needed for the decision; exclude advisor-runs input echoes from searches and confirmations.
'''
write('briefing.md',briefing)
numbered = '\n'.join(f'{path}:{number}: {line}' for path,number,line in citations)+'\n'
write('citation-readback.txt',numbered)
print(numbered)
print('Fresh 58-file current/snapshot identity and six final receipt/stream bindings checked.')
