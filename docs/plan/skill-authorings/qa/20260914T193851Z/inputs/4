"""Capture authoring inputs and requirements; no skill execution or quality checks."""
import re
import sys
from pathlib import Path

PROJECT = Path('C:/Projects/DevForgeAI')
HERE = Path(__file__).resolve().parent
RUN = HERE.with_name('20260914T193851Z')
BUILDER = PROJECT / '.agents/skills/skill-builder'
sys.path.insert(0, str(BUILDER / 'scripts'))
import authoring as custody

extension = PROJECT / 'docs/specs/qa-skill-postmvp-spec.md'
baseline = PROJECT / 'docs/specs/qa-skill-spec.md'
target = PROJECT / 'src/agents/skills/qa'
prior = PROJECT / 'docs/plan/skill-authorings/qa/20260914T1748018341005Z/authoring-baseline.json'
paths = list(custody.files(target))
request = HERE / 'user-request.txt'
request.write_bytes(b'$skill-builder C:\\Projects\\DevForgeAI\\docs\\specs\\qa-skill-postmvp-spec.md\n')
mapping = {
    'QAP-001': ['SKILL.md', 'references/intake-planning.md', 'agents/openai.yaml'],
    'QAP-002': ['SKILL.md', 'references/intake-planning.md'],
    'QAP-003': ['references/intake-planning.md', 'assets/test-plan-template.md'],
    'QAP-004': ['SKILL.md', 'references/intake-planning.md', 'references/execution-integrity.md'],
    'QAP-005': ['references/execution-integrity.md'],
    'QAP-006': ['references/execution-integrity.md', 'assets/qa-report-template.md', 'assets/qa-fix-template.md'],
    'QAP-007': ['references/assessment.md', 'assets/test-plan-template.md', 'assets/qa-report-template.md'],
    'QAP-008': ['SKILL.md', 'references/execution-integrity.md', 'assets/test-plan-template.md', 'assets/qa-report-template.md', 'assets/qa-fix-template.md'],
    'QAP-009': ['references/execution-integrity.md', 'references/intake-planning.md'],
    'QAP-010': ['SKILL.md', 'references/assessment.md', 'assets/qa-report-template.md', 'assets/test-plan-template.md'],
    'QAP-011': ['references/reporting-handoff.md', 'assets/test-plan-template.md', 'assets/qa-report-template.md', 'assets/qa-fix-template.md'],
    'QAP-012': ['SKILL.md', 'references/reporting-handoff.md'],
    'QAP-013': ['references/reporting-handoff.md', 'assets/test-plan-template.md'],
    'QAP-014': ['SKILL.md', 'references/reporting-handoff.md', 'manual-evaluation-obligations.md (external authoring input)'],
}
raw = custody.read_bytes(extension).decode('utf-8-sig')
requirements = []
for key, artifacts in mapping.items():
    heading = re.search(r'\*\*' + key + r'[^\n]+', raw).group(0)
    requirements.append({'origin': 'user specification', 'outcome': heading, 'artifacts': artifacts})
requirements.append({'origin': 'user specification', 'outcome': 'Retain all unamended QA-001 through QA-026 obligations and all QV-01 through QV-21 with explicit extension compatibility; later independent evaluation also covers QPV-01 through QPV-21.', 'artifacts': paths})
requirements.append({'origin': 'inferred implementation choice', 'outcome': 'Preserve existing nine-resource layout and supported metadata; change UI default prompt to request ordinary QA; add no runtime helper.', 'artifacts': paths})
expectations = HERE / 'manual-evaluation-obligations.md'
compatibility = raw.split('### MVP scenario compatibility\n', 1)[1].split('\n## 3.', 1)[0]
scenarios = raw.split('## 7. Required acceptance scenarios\n', 1)[1].split('\n## 8.', 1)[0]
expectations.write_text('# Later independent evaluation obligations\n\nThis is a manual requirements handoff, not an executable campaign or a result.\n\nRead both bound specifications. Preserve all MVP scenarios with the following amendments.\n\n' + compatibility + '\n\n## Extension scenarios\n' + scenarios + '\n\nBind exact delivered skill and both spec bytes to a Python JSONL runner, deterministic graders, independent fixtures, expected results, schema, runtime/dependency information, and artifact manifests/digests. Retain observable launch markers and ordered terminal decisions; assess actual continuation and stop behavior, not keyword presence. Preserve existing evidence and run in a fresh distinct destination. Python produces evidence only; compiled Rust retains protected framework authority. Builder does not generate or run this campaign.\n', encoding='utf-8')
sources = [extension, baseline, request, expectations, Path(__file__).resolve(), PROJECT / 'AGENTS.md', PROJECT / 'docs/plan/devforgeai-codex-rust-enforcement-design.md', BUILDER / 'SKILL.md']
sources += [BUILDER / 'references' / name for name in ['authoring.md', 'spec-build.md', 'regeneration.md', 'evidence-format.md', 'validation-handoff.md', 'scaffolding.md', 'openai_yaml.md']]
custody.save(HERE / 'operational-before-manifest.json', custody.manifest(custody.files(PROJECT / '.agents/skills/qa')))
contract = {
    'schema_version': 'authoring-contract-v1', 'run_id': RUN.name,
    'project_root': str(PROJECT), 'target_root': str(target), 'target_name': 'qa', 'operation': 'edit',
    'authorization': 'User invoked $skill-builder with qa-skill-postmvp-spec.md, which selects the existing development qa package and companion MVP specification. Author the extension, preserve historical evidence and operational copies, publish custody records and return manual validator handoff.',
    'history_review': 'Inspected published prior authoring record, baseline manifest and publication readback; use digest-bound authored prior with baseline bytes verified by authoring begin.',
    'prior': custody.reference(prior), 'change_paths': paths, 'requirements': requirements,
    'purpose': 'Independent specification-driven product QA with automatic continuation and evidence-based stopping.',
    'activation': 'Ordinary selected product QA defaults to run; explicit plan, execute and retest remain distinct. Near misses remain excluded.',
    'dependencies': ['Codex terminal and file capabilities; product tools discovered from selected inputs; no mandatory framework/plugin/index/MCP'],
    'operational_constraints': ['Development source only. No installation, product QA execution, skill quality campaign, or framework implementation in authoring.'],
    'recovery': 'Preserve attempts, recheck source identity, checkpoint owned state and report delivery failures; terminal failures require explicit corrected-candidate retest.',
    'capabilities': ['Independent product QA planning, authorized preparation/execution, integrity inspection, metrics assessment, reporting and manual handoff'],
    'expected_outputs': ['Bound test plan, QA report, confirmed-failure qa-fix packet, execution/stop records, external hash manifest and outcome-specific manual user handoff'],
    'side_effects': ['At runtime: authorized isolated QA fixtures/harnesses, local builds/tests/instrumentation, reports and cleanup of QA-owned disposable state. No product repairs or inferred installation/deployment/persistent effects.'],
    'inputs': [custody.reference(p) for p in sources],
    'known_issues': ['Validation: NOT_PERFORMED. Testing: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED.', 'QA-026/QAP-014 evaluated-build completeness remains unproven until a separate validator creates and executes the exact-byte-bound Python evidence bundle and all applicable MVP/extension scenarios. Historical results do not qualify these edited bytes.'],
}
custody.save(HERE / 'authoring-contract.json', contract)
custody.save(HERE / 'requirement-resource-map.json', {'requirements': requirements, 'specifications': [custody.reference(extension), custody.reference(baseline)]})
print(str(HERE / 'authoring-contract.json'))
