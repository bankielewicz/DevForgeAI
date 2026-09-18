"""Refresh documentation from final measurements; preserve historical evidence."""
from pathlib import Path

run = Path(__file__).resolve().parent
replacements = {
    '079-windows-coverage': '085-windows-final-coverage',
    'windows-coverage-003.json': 'windows-coverage-004.json',
    'wsl-coverage-001.json': 'wsl-coverage-002.json',
    '079/080': '085/086',
    'Attempt 079:': 'Attempt 085:',
    'Attempt 080:': 'Attempt 086:',
    '2,729 / 3,440 = 79.3313953488372': '2,744 / 3,442 = 79.72109238814643',
    '2,072 / 2,784 = 74.42528735632182': '2,071 / 2,786 = 74.33596554199569',
    '2729/3440 = 79.3313953488372': '2744/3442 = 79.72109238814643',
    '2072/2784 = 74.42528735632182': '2071/2786 = 74.33596554199569',
    '001–083': '001–089',
    '081/082': '087/089',
    'Windows Clippy 078, native release builds 087/089, WSL final checks 083': 'Windows Clippy 088, native release builds 087/089, WSL final checks 089',
    'Attempts 078–083 bind the same candidate.': 'Attempts 085–089 bind the same candidate. Attempt 083 retained a new Rust 1.98 Clippy lint failure; the mechanical iterator refactor in 084 resolved it.',
    '[079 candidate]': '[085 candidate]',
    'PASS (079)': 'PASS (085)',
    'PASS (080)': 'PASS (086)',
    'Windows Clippy PASS (078); source formatted (077); WSL final format/Clippy and binary hashes retained in 083.': 'Windows Clippy PASS (088); source formatted (084); WSL final format/Clippy and binary hashes PASS (089).',
    'Windows PASS (081); WSL Linux CLI/daemon PASS (082)': 'Windows PASS (087); WSL Linux CLI/daemon PASS (089)',
}
qa = 'Formal QA is PENDING. QA must independently verify specification conformance, executed-line coverage >=95%, and the required unit-test pass rate >=95% per platform. Any mock decorator or test that games results is a QA failure. Reject vacuous assertions, fabricated outputs, weakened expectations, skipped required cases counted as passes, unjustified coverage exclusions and duplicate retry counts. Failed QA returns this candidate for remediation; the current coverage already fails both measured platforms.'
integrity = 'The focused test-integrity review found a setup-only assertion in devforgeai/tests/harness.rs (size_of::<u32>() == 4). It supplies no product evidence and receives no required-case credit. Raw runner totals of 38 Windows / 36 WSL include it; removing that setup count leaves 37 / 35 executed non-setup cases, not a complete required-case denominator. The absent-distribution WSL probe does not establish installed-stopped behavior. No mock decorator was found in the scoped Rust source/tests/examples scan. This scan is not a completed anti-gaming audit. The HTML Node checker uses minimal DOM/storage substitutes and supplies only helper logic evidence, never native browser or product qualification.'
for name in ['build_playbook.py', 'platform-status.md', 'finalize_notes.py']:
    p = run / name
    text = p.read_text(encoding='utf-8')
    for old, new in replacements.items():
        text = text.replace(old, new)
    if name == 'build_playbook.py':
        text = text.replace("'Windows measured coverage is below 95%. No full product or protected-framework acceptance is claimed.'", repr('Windows and WSL measured coverage are below 95%. ' + qa))
        anchor = '<section class="panel"><div class="eyebrow">04 / Return the evidence</div>'
        text = text.replace(anchor, '<section class="panel"><h2>Formal QA and test integrity</h2><p>' + qa.replace('>=', '&gt;=') + '</p><p>' + integrity.replace('<u32>', '&lt;u32&gt;') + '</p><p>Retain a file-and-line audit ledger linking every credited test to its requirement, independent expected result and observed failure when that behavior is broken. Search source and test attributes/decorators for mocks; inspect skips, catch-all errors, early exits, coverage exclusions and assertions manually. A clean keyword scan alone cannot pass this review.</p></section>' + anchor)
        text = text.replace("authority:'evidence_only_NOT_EVALUATED',required_cases:", "authority:'evidence_only_NOT_EVALUATED',formal_qa_status:'PENDING',qa_failure_criteria:['specification nonconformance','line coverage below 95%','required unit-test pass rate below 95%','mock decorators present','tests gaming results'],required_cases:")
    elif name == 'platform-status.md':
        text += '\n## Formal QA handoff and test integrity\n\n' + qa + '\n\n' + integrity + '\n'
    else:
        text = text.replace("write('checkpoint-manual-handoff.md',checkpoint)", "checkpoint += " + repr('\n' + qa + '\n\n' + integrity + '\n') + "\nwrite('checkpoint-manual-handoff.md',checkpoint)")
        text = text.replace("write('delivery.md',delivery)", "delivery += " + repr('\n' + qa + '\n\n' + integrity + '\n') + "\nwrite('delivery.md',delivery)")
        text = text.replace("'check_playbook.cjs']", "'check_playbook.cjs','finalize_notes.py','test-integrity-review.md','attempts/085-windows-final-coverage/candidate.json','attempts/089-wsl-final-checks/stdout.txt']")
    p.write_text(text, encoding='utf-8')
(run/'test-integrity-review.md').write_text('# Focused test-integrity observations\n\n' + qa + '\n\n' + integrity + '\n\nRead-only scope: devforgeai/src, tests, examples and Cargo.toml. Inspected mock/patch attributes, coverage bypasses, ignores, constant assertions and early-return matches; read harness.rs, wsl_bridge.rs and GUI wait helpers. The GUI wait return follows an observed matching window value and has a failing deadline. Both explicitly ignored bridge tests executed in attempt 085 via --include-ignored. The ignore crate implements Git ignore rules and is not a test bypass. No first-party coverage bypass attribute was found in this focused search. Full independent test-to-requirement and negative-oracle review remains PENDING.\n', encoding='utf-8')
