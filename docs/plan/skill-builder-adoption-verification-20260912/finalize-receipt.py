"""Final ordinary development readback; not a protected acceptance record."""
import hashlib
import json
from pathlib import Path
import re

evidence = Path(__file__).resolve().parent
project = evidence.parents[2]
package = project / "src/agents/skills/skill-builder"
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
expected = "11457297985c7768faaec1846e54e0bcf4538fd8e064fb0d1099f9da6c7e8620"
assert sha(package / "evals/build-manifest.json") == expected
manifest = json.loads((package / "evals/build-manifest.json").read_text())
actual = {p.relative_to(package).as_posix(): sha(p) for p in package.rglob("*") if p.is_file() and p != package / "evals/build-manifest.json"}
assert actual == manifest["artifacts"]
for name, digest in actual.items():
    assert sha(evidence / "builder-final-release" / name) == digest
specification = project / "docs/plan/skill-builder-adoption-spec.md"
assert sha(specification) == "beebc2b97b6719fafbd1500b63e41280ddd611a3978b7d3af9b2798b7a87f095"
report = evidence / "REPORT.md"
for target in re.findall(r"\]\(([^)]+)\)", report.read_text(encoding="utf-8")):
    assert (report.parent / target).resolve().exists(), target
selected = ["REPORT.md", "source-change-receipt-release.json", "profile-readback-audit-release.json", "regression-release.txt",
            "structural-check-release.txt", "handoff-release-output.txt", "profile-checks-release/summary.json",
            "../skill-builder-adoption-verification-20260912-independent-build-trials-final2/REPORT.md",
            "../skill-builder-adoption-verification-20260912-independent-build-trials-final2/final-readback-audit.json",
            "../skill-builder-adoption-verification-20260912-independent-adoption-trial-final2/report.md",
            "../skill-builder-adoption-verification-20260912-independent-adoption-trial-final2/measured-input-readback-audit.json",
            "../skill-builder-adoption-verification-20260912-independent-adoption-trial-final2/original-input-locator-audit.json",
            "../skill-builder-adoption-verification-20260912-independent-failure-trials/REPORT-FINAL.md",
            "../skill-builder-adoption-verification-20260912-independent-failure-trials/final-snapshot-case-hash-audit.json"]
receipt = {"status": "DEVELOPMENT_ENHANCEMENT_VERIFICATION_COMPLETE", "authority": "NONE",
           "builder_manifest_sha256": expected, "specification_sha256": sha(specification),
           "regression": {"tests": 140, "exit_code": 0},
           "structural_check": "PASS", "profiles": "POSITIVE_AND_NEGATIVE_EXPECTATIONS_MATCHED",
           "independent_import_specification_regeneration": "COMPLETE",
           "independent_adoption_revision_revalidation_lineage": "COMPLETE",
           "independent_partial_delivery_and_publication_faults": "COMPLETE_WITH_RETAINED_EXPECTED_FAILURES",
           "source_manifest_and_archive_readback": "PASS", "report_links_readback": "PASS",
           "operational_skill_writes": "NOT_PERFORMED", "installation": "NOT_PERFORMED", "rust_qualification": "NOT_PERFORMED",
           "selected_evidence": [{"path": p, "sha256": sha(evidence / p)} for p in selected]}
(evidence / "FINAL-RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": receipt["status"], "manifest": expected, "report_sha256": sha(report), "receipt_sha256": sha(evidence / "FINAL-RECEIPT.json")}))
