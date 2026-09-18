"""Prepare a complete second briefing without altering the first attempt."""
from pathlib import Path
root = Path(__file__).resolve().parent
text = (root/'briefing.md').read_text(encoding='utf-8')
text = text.replace('AGENTS.md:88', 'AGENTS.md:124')
text = text.replace('This is the first reviewer attempt for this question.', '''Attempt 1 completed with process exit 1 after 181.875 seconds. Its CLI JSON reports terminal_reason=api_error, API Error: Connection refused (ConnectionRefused), zero API duration/tokens/cost, empty stderr and no reviewer response. Receipt: docs/plan/advisor-runs/20260916T034812Z-8d3c2a/attempt-001/execution.json; raw stdout at the same attempt. No advice was produced. This is the final permitted attempt, using the identical immutable request, auth mode, restrictions and USD1 cap; normal host escalation is requested for the likely sandbox/network restriction. No third attempt is permitted.''')
text = text.replace('Type: stuck. Determine', 'Type: stuck; execution retry after retained connection refusal, not a new review. Determine')
text = text.replace('## STATE\n', '''## STATE
Since the initial briefing was written, AGENTS.md changed externally to SHA256 3b8e2a112c438b536ab59db2abbcfd6e08ebdd7f41caa13cdf6d5c49866fab86, adding advisor guidance. The first briefing's line88 anchor was stale; this briefing corrects the scope clause anchor. The candidate and all four governing specifications remain unchanged. The original inventory is historical, and a fresh compiled source collection at docs/plan/framework-worker-native-continuation/20260916T034357Z-source-identity/source-observation-002/receipt.json passed (same counts, stdout SHA256 2029d7889cd4054d2791fd0e55684dae48ac0c37aac12710e068aad858a1fbad). State observation at state-observation-001.json in that continuation root records only AGENTS.md changed among prior inventory files and the same single prohibited environment name. No native preflight has run.
''')
with (root/'briefing-retry.md').open('x',encoding='utf-8') as out:
    out.write(text)
