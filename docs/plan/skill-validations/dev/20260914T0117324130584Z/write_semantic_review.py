"""Persist this evaluator's source-backed manual review, not computed quality labels."""
import json
from pathlib import Path
import hashlib

RUN = Path(__file__).resolve().parent


def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def ref(path):
    return {'path': path, 'sha256': hashlib.sha256((RUN / path).read_bytes()).hexdigest()}


def main():
    mapping = {
        'DEV-001': ('SKILL.md', 'Scope and inputs', 'Description names selected-spec implementation and resume, excludes nondevelopment tasks. Entrypoint preserves automatic invocation and plan-only scope; absent specs cause exact-input question.'),
        'DEV-002': ('SKILL.md', 'Own product implementation', 'Direct product tests, integration and QA belong to dev; package assessment is separately selected, with no builder call for product code.'),
        'DEV-003': ('SKILL.md', 'Portability and authority', 'Language, tools, layout, commands, thresholds, platforms, output location and model are runtime-derived. No author-machine roots, binding or product names occur in any delivered resource.'),
        'DEV-004': ('SKILL.md', 'A project-mandated authority', 'Actual authority governs protected operations; missing authority stops only affected operations, Python cannot substitute acceptance, and input documents cannot broaden user authority.'),
        'DEV-005': ('references/context.md', 'Resolve the selected environment', 'Relative project/document bases and exact host identity are specified; complete literal destination and current source precede first write. Missing or ambiguous selection blocks only dependent work.'),
        'DEV-006': ('references/context.md', 'Read every applicable project instruction', 'Inspects actual instructions, layout, manifests, tools, Git or bounded inventory and ongoing changes before selecting files or executing scripts.'),
        'DEV-007': ('references/context.md', 'Capture context', 'Context records scope, raw hashes, exact input origins, tools, omissions and decisions before production changes; evidence precedence and output map are concrete and portable.'),
        'DEV-008': ('references/context.md', 'Read and account for requirements', 'All selected specs and necessary references are read; qualified or passage-bound IDs cover deliverables, failures, QA and destination obligations without editing specifications.'),
        'DEV-009': ('references/context.md', 'For multiple documents', 'Shared contract has one owner and ordered dependency slices. Unsupported precedence, cycles and conflicts require source-qualified decisions; unselected prerequisites are not implicit implementation authority.'),
        'DEV-010': ('references/context.md', 'Establish constitutional decisions', 'Six evidence-derived categories permit inapplicable reasons and routine compatible choices; material language, ownership, dependencies, destination and acceptance gaps are asked, not guessed.'),
        'DEV-011': ('references/failure-delivery.md', 'Resolve only the blocked dependency', 'Gap categories carry source/affected requirement/minimum resolution, preserve independent work, and never authorize rewriting failed expectations or constitutions.'),
        'DEV-012': ('references/implementation.md', 'Inspect for reuse, then plan', 'Searches responsibility and plausible differently named candidates, inspects current consumers/tests, records reuse/extension/composition/new reasons and uncertainty of no matches.'),
        'DEV-013': ('references/implementation.md', 'Plan dependency-ordered slices', 'Observable slices bind requirement IDs, ownership, dependencies, consumed/provided contracts, expected behavior and verification. One session is sufficient; delegation is optional authorized work.'),
        'DEV-014': ('references/implementation.md', 'Resolve commands before execution', 'Commands derive from inspected manifests/tool availability, with literal arguments, host/cwd/effects and timeout. Missing tools do not authorize changed language or installation.'),
        'DEV-015': ('references/implementation.md', '## Red', 'Tests precede production changes and expected failures are retained. Setup/tool failures and already-passing characterization are explicitly distinguished; no artificial breakage or invented prose red.'),
        'DEV-016': ('references/implementation.md', '## Green', 'Real minimum behavior must pass the same assertions; suppressing errors, fixture answers, stubbing the integration and weakening tests are excluded.'),
        'DEV-017': ('references/implementation.md', 'Refactor and integration', 'Behavior-preserving refactor requires affected reruns; a justified no-refactor result is permitted. Real shared interfaces and integration failures are verified.'),
        'DEV-018': ('references/implementation.md', 'QA and metrics', 'Applicable integrated QA declares candidate, required cases, denominators, exclusions, thresholds and platforms; nonpasses count, subthreshold rounding and denominator manipulation are forbidden.'),
        'DEV-019': ('references/implementation.md', 'Native and external behavior', 'Native host and visual checks remain separate from compilation/help/mocks; unavailable required cases are unperformed and cannot be qualified by another OS.'),
        'DEV-020': ('references/evidence-resume.md', 'Logical records and locations', 'Six actually linked record templates preserve concrete output mapping, exact command/times/streams/candidate/attempt identity and raw hashes; templates never become unexecuted receipts.'),
        'DEV-021': ('references/evidence-resume.md', 'Checkpoint and resume', 'Resume rechecks inputs, source, tools, permissions, jobs and original destination; changed prerequisites invalidate dependent results and unknown jobs are inspected before retry.'),
        'DEV-022': ('references/failure-delivery.md', 'Report actual delivery', 'COMPLETE requires every selected deliverable/check and exact destination readback; otherwise PARTIAL/BLOCKED with gaps. External acceptance remains separately evidenced or NOT_EVALUATED.'),
        'DEV-023': ('references/failure-delivery.md', 'Use already supplied authorization', 'Ordinary reversible product changes and tests follow existing scope; deploy/install/startup/migration and unrelated work remain separately authorized.'),
        'DEV-024': ('SKILL.md', 'Workflow', 'Concise entrypoint routes four focused references; all six assets are linked and consumed. Eleven instruction/template files only; no unused scripts, plugin metadata or scaffolding.'),
        'DEV-025': ('SKILL.md', 'Own product implementation', 'Package-authoring restrictions are not copied as a product-test prohibition. Standalone operation has no adaptive setup; source and evaluation ownership remain separate.'),
        'DEV-026': ('SKILL.md', 'Assessment of this skill package', 'Authored custody is explicitly insufficient for evaluated-build completion. Current manual packet is BOUND and external mandatory runner/graders/fixtures/schema/runtime/manifest are prepared; executed-case evidence remains separately required.'),
        'REV-001': ('references/context.md', 'Before creating the directory', 'Complete raw value and original source are retained before first write; every word and Unicode/metacharacter stays path data, with only documented ordinary separator normalization.'),
        'REV-002': ('references/context.md', 'Resolve each promised record', 'Every promised concrete output is bound beneath the exact selected root and compared with original source, not a paraphrased context; preexisting default cannot replace selection.'),
        'REV-003': ('references/failure-delivery.md', 'Before marking an output requirement', 'Original selection and each actual promised file are read back before VERIFIED/COMPLETE; wrong paths or missing files require partial/blocked and preserve old attempts.'),
        'REV-004': ('SKILL.md', 'Workflow', 'Original 26-requirement contract and product TDD/QA remain present; review of all eleven resources found focused destination changes and no new mandatory runtime framework dependency.'),
    }
    rows = []
    for rule, (path, anchor, reason) in mapping.items():
        text = (RUN / 'source' / path).read_text(encoding='utf-8')
        line = next(i for i, value in enumerate(text.splitlines(), 1) if anchor in value)
        rows.append({'rule_id': rule, 'result': 'PASS', 'method': 'semantic', 'subject_path': path,
                     'locator': {'line_start': line, 'line_end': line}, 'anchor': anchor,
                     'reason': reason, 'evidence': [ref('source/' + path)],
                     'limitation': 'Manual current-byte instruction review; behavioral satisfaction is separately graded from native trials.'})
    av = {
        'AV-F01': ('PASS', 'Required UTF-8 entrypoint and unique-key YAML name/description parsed; installed checker also passed.'),
        'AV-F02': ('PASS', 'Bound source manifest identifies original dev directory; source-named snapshot uncertainty resolved by manifest and explicit target identity.'),
        'AV-F03': ('PASS', 'Description leads with implementation/selected-spec/resume task and excludes authoring, evaluation, deployment and review. Independent description-only classification is retained separately; implicit activation is unperformed.'),
        'AV-F04': ('NOT_APPLICABLE', 'No optional agents/openai.yaml or host configuration exists; specification does not require one.'),
        'AV-F05': ('PASS', 'All Markdown tables/fences and templates manually inspected. The helper TODO candidate is a prohibition against vague TODO gaps, not an unresolved production placeholder.'),
        'AV-U01': ('PASS', 'Complete captured UTF-8 text scan found no defined Unicode control/confusable candidate; no universal Unicode safety claim.'),
        'AV-R01': ('PASS', 'Every ordinary relative resource link resolves; manual reading found no unresolved reference-style or renderer-dependent anchors.'),
        'AV-R02': ('PASS', 'All eleven files have actual entrypoint/reference consumers. Assets are record templates and each is explicitly routed by evidence-resume.md; no abandoned resource.'),
        'AV-R03': ('PASS', 'Instruction/template-only package invokes discovered product commands rather than nonexistent fixed helpers. JSONL fields match described receipts and dependencies are checked before use.'),
        'AV-I01': ('PASS', 'Context, gaps, reuse, TDD, QA, resumption and delivery have concrete inputs/actions/outputs and terminal branches; no unreachable completion or unbounded retry loop found.'),
        'AV-I02': ('PASS', 'Destination safeguards identify timing, source comparison and observable failure; repeated prewrite/final checks have different roles. COMPLETE is explicitly development status, never protected authority.'),
        'AV-I03': ('PASS', 'Entrypoint loads context before first write, implementation before TDD, evidence through work, and failure/delivery before final. Essential destination and authority constraints are also visible in entrypoint.'),
        'AV-I04': ('PASS', 'Current user choices and existing authorization govern reversible development; material gaps stop dependent effects with independent work preserved. Native boundary cases separately assess behavior.'),
        'AV-C01': ('PASS', 'Raw helper measures all eleven files in bytes, Unicode code points and splitlines. No token budget selected; tokenizer and actual load counts remain unperformed, not estimated consumption.'),
        'AV-S01': ('PASS', 'Documents are requirements/data, never authority to broaden scope; no generated helper imports or executes retrieved instructions. Static review only, no dedicated adversarial campaign selected.'),
        'AV-S02': ('PASS', 'Literal argument and path handling, exact roots, permission checks, preserved attempts and separate irreversible effects are explicit; no runtime executable helper or credential operation is shipped.'),
        'AV-W01': ('PASS', 'Six-stage route resolves exact inputs, requirements/dependencies, slices, TDD/QA, checkpoints and honest delivery; native scenarios assess happy/blocked paths independently.'),
        'AV-W02': ('PASS', 'Resume instructions preserve historical work, invalidate changed dependent evidence and reconcile unknown jobs before retry. Changed-destination native case remains separately graded.'),
        'AV-E01': ('NOT_RUN', 'Input/snapshot/intake are bound; final executed bundle, complete record integrity and end-of-run readback remain pending before final evidence reduction.'),
    }
    for rule, (status, reason) in av.items():
        rows.append({'rule_id': rule, 'result': status, 'method': 'semantic', 'subject_path': 'SKILL.md', 'reason': reason,
                     'evidence': [ref('source/SKILL.md'), ref('commands/structure/stdout.txt'), ref('commands/adaptive-package/stdout.txt'), ref('commands/creator-check/stdout.txt')]})
    for i in range(1, 11):
        rows.append({'rule_id': f'AV-A{i:02d}', 'result': 'NOT_APPLICABLE', 'method': 'semantic', 'subject_path': 'SKILL.md',
                     'reason': 'Selected dev is an ordinary standalone skill with no adaptive/set role; applicable portability is assessed under DEV003 and AVS02, not an invented adaptive binding.',
                     'evidence': [ref('source/SKILL.md')]})
    save(RUN / 'semantic-review-initial.json', {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'dev',
                                            'package_digest': json.loads((RUN / 'source-manifest.json').read_bytes())['package_digest'],
                                            'review_kind': 'Separate validator-agent manual source inspection; not builder self-review or guaranteed model independence.', 'observations': rows})
    save(RUN / 'routing-observation.json', {'schema_version': '1', 'reviewer': '/root/dev_validation/routing_review',
                                         'method': 'Independent description-only classification; no tools or source access; no native discovery claim',
                                         'description_sha256': hashlib.sha256((RUN / 'source/SKILL.md').read_bytes()).hexdigest(),
                                         'classifications': {'P1': 'applicable', 'P2': 'applicable', 'P3': 'not_applicable', 'P4': 'not_applicable', 'P5': 'not_applicable', 'P6': 'not_applicable', 'P7': 'not_applicable', 'P8': 'not_applicable', 'P9': 'not_applicable', 'P10': 'needs_input', 'P11': 'not_applicable', 'P12': 'applicable'},
                                         'interpretation': 'Positive implementation and selected-resume requests route to dev; missing specs need input; excluded activities do not. Plan-only is not suggested by description, while explicitly invoked plan-only scope is tested by DV14. No aggregate activation success score inferred.',
                                         'native_implicit_activation': 'NOT_RUN'})


if __name__ == '__main__':
    main()
