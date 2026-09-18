"""Create a fresh authoring contract from approved inputs; never mutate the skill."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[3]
sys.path.insert(0,str(PROJECT/"src/agents/skills/skill-builder/scripts"))
import authoring as a
old=PROJECT/"docs/plan/skill-authorings/dev/20260913T2114525120037Z"
prior=a.reference(old/"authoring-baseline.json")
proposal=PROJECT/"docs/plan/skill-validations/dev/20260913T2310456388212Z/revision-spec.md"
if a.digest(proposal.read_bytes())!="d4fdb404ebf3e869d4d2b6f99756cf70d54a460a369a74bd3f645f5cb9cfe1b9":
    raise ValueError("proposal drift")
contract=json.loads((old/"contract.json").read_bytes())
contract.update(run_id=ROOT.name,operation="edit",history_review="Verified authored baseline from prior successful publication; rejected old request remains historical",
 prior=prior,authorization="User approved the complete remediation plan and instructed: Implement the plan. Author dev REV-001 through REV-004 in development source, then separately validate; no installation.",
 change_paths=["SKILL.md","references/context.md","references/evidence-resume.md","references/failure-delivery.md","assets/context.md","assets/delivery.md","assets/checkpoint.md","assets/traceability.md"],
 known_issues=["Quality of revised dev bytes remains unperformed during authoring; separately selected validation stage owns DV-01..DV-18 and RV-01..RV-06 with a newly bound external evaluation bundle."],
 inputs=[a.reference(p) for p in (PROJECT/"docs/plan/dev-qa-remediation-plan.md",proposal,PROJECT/"docs/specs/dev-skill-spec.md",PROJECT/"AGENTS.md",PROJECT/"src/agents/skills/skill-builder/SKILL.md",PROJECT/"src/agents/skills/skill-builder/scripts/authoring.py",PROJECT/"src/agents/skills/skill-builder/references/evidence-format.md",ROOT/"approval.md")])
for rid,desc,paths in [
 ("REV-001","Preserve complete literal evidence destination and original source before writes.",["SKILL.md","references/context.md","assets/context.md"]),
 ("REV-002","Bind original value, resolved root and logical output map before writes and on resume.",["references/context.md","references/evidence-resume.md","assets/context.md","assets/checkpoint.md"]),
 ("REV-003","Read back every promised output against original selection before VERIFIED/COMPLETE.",["references/failure-delivery.md","references/evidence-resume.md","assets/delivery.md","assets/traceability.md"]),
 ("REV-004","Preserve all DEV requirements, runtime TDD, portable identity and custody/assessment boundaries.",["SKILL.md"])]:
    contract["requirements"].append({"id":rid,"origin":"approved revision specification","outcome":desc,"artifacts":paths})
origin,baseline=a.origin(contract)
current=a.manifest(a.files(PROJECT/"src/agents/skills/dev"))
if {r["path"]:r["sha256"] for r in current["files"]}!=baseline:
    raise ValueError("current source drift")
a.save(ROOT/"dev-baseline-supplement.json",{"basis":origin,"current_package_digest":current["package_digest"],"current_matches_baseline":True,"old_packet_status":"REJECTED, unchanged","interpretation":"Authored custody independently verified; no adoption or retroactive validator readiness."})
a.save(ROOT/"dev-authoring-contract.json",contract)
print(json.dumps({"contract":str(ROOT/"dev-authoring-contract.json"),"prior":prior,"current_package_digest":current["package_digest"]}))

