"""Bounded maintenance commands and publication of observation evidence."""
import json
from pathlib import Path
import sys
from harness import RUN, ROOT, TARGET, read, write, save, ref, sha, inventory, execute

if sys.argv[1] == 'red' or sys.argv[1] == 'green':
    stage=sys.argv[1]
    execute(stage.upper(),[sys.executable,'-B','-X','utf8','-m','unittest','discover','-s','src/agents/skills/skill-validator/tests','-p','test_confirmed_findings.py','-v'])
elif sys.argv[1] == 'pin':
    proposal=ROOT/'docs/plan/skill-validations/skill-validator/20260913T201813155594Z/revision-spec.md'
    assert sha(read(proposal))=='832de4a0d2512f9f50481aeb822645c3830bfd005da954a0a10070dc69b92c25'
    write(RUN/'inputs/revision-spec.md',read(proposal))
    save(RUN/'authorization.json',dict(user_request='Implement the plan.',scope='Four confirmed fixes plus fresh QA in the approved workflow; no operational installation.',target=str(TARGET),proposal=ref(proposal),basis='Verified observed scoped edit; preserved historical implementation receipt and snapshot, no generated/adopted status invented.',permitted_paths=['scripts/adaptive_observe.py','scripts/text_resources.py','tests/test_confirmed_findings.py','evals/build-manifest.json'],workflow=ref(ROOT/'docs/plan/skill-validator-confirmed-findings-remediation-workflow.md')))
    implementation=ROOT/'docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z'
    for name in ('final-receipt.json','final-delta.json','implementation-report.md'):
        write(RUN/'inputs'/('historical-'+name),read(implementation/name))
    save(RUN/'tests-before-production-edits.json',inventory(TARGET/'tests'))
    print('Authorization, proposal, prior delivery and pre-production tests pinned.')
