$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
# Documentation and byte consistency only; not product QA or an acceptance authority.
$checks = [Collections.Generic.List[object]]::new()
function Record([string]$Name, [bool]$Result, $Detail) {
    $checks.Add([ordered]@{name=$Name; result=$(if($Result){'PASS'}else{'FAIL'}); detail=$Detail})
}
function Digest([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function KeysEqual($Object, [string[]]$Expected) {
    return (@($Object.PSObject.Properties.Name | Sort-Object) -join '|') -ceq (@($Expected | Sort-Object) -join '|')
}
$root = $PSScriptRoot
$package = 'C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes'
$qa = 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T105456Z-qa-retest'
$request = Get-Content -Raw -LiteralPath (Join-Path $root 'request.template.json') | ConvertFrom-Json
$review = Get-Content -Raw -LiteralPath (Join-Path $root 'review.template.json') | ConvertFrom-Json
$commands = Get-Content -Raw -LiteralPath (Join-Path $root 'command-plan.json') | ConvertFrom-Json
$diagnostics = Get-Content -Raw -LiteralPath (Join-Path $root 'inputs\diagnostics.json') | ConvertFrom-Json
$policy = Get-Content -Raw -LiteralPath (Join-Path $package 'src\restrictive-launch-policy.json') | ConvertFrom-Json
$identity = Get-Content -Raw -LiteralPath (Join-Path $package 'src\native-executable-identity.json') | ConvertFrom-Json
$intake = Get-Content -Raw -LiteralPath (Join-Path $root 'intake-v2-verification.json') | ConvertFrom-Json
Record 'intake_and_preservation' ($intake.status -ceq 'VERIFIED' -and $intake.problems.Count -eq 0) 'Corrected intake after retained display-prefix comparison error.'
Record 'task_exact_bytes' ((Digest (Join-Path $root 'inputs\task.json')) -ceq (Digest (Join-Path $package 'tests\fixtures\task.json')) -and $request.candidate_sha256 -ceq 'b35366b508eea199c12142a8a4a8d13a083426c35c4b9ebaf9f0ccf168eeab3a') 'Task digest is separate from candidate source-manifest identity.'
Record 'request_document_fields' (KeysEqual $request @('schema_version','diagnostics_ref','diagnostics_sha256','project_id','checkout_id','work_id','run_id','candidate_sha256','checkout_root','run_dir','worker_executable','worker_sha256','adapter','scenario','profile')) 'Static field comparison with Request in current request.rs; not runtime admission.'
Record 'review_document_fields' (KeysEqual $review @('schema_version','reviewer','trial_selection_ref','codex_sha256','checkout_root','model','effort','profile_sources','findings','launch_policy_id','launch_policy_sha256','source_inventory_ref','source_inventory_sha256')) 'Static field comparison with ReviewV2 in current request.rs; not runtime admission.'
Record 'templates_deliberately_incomplete' ($null -eq $request.profile.review_sha256 -and $null -eq $review.reviewer -and $null -eq $review.trial_selection_ref -and $null -eq $review.source_inventory_sha256 -and $null -eq $review.profile_sources -and @($review.findings.PSObject.Properties | Where-Object {$null -ne $_.Value}).Count -eq 0) 'Null placeholders remain unresolved, not fabricated findings or launch-ready inputs.'
Record 'schema_and_profile_bindings' ($request.schema_version -eq 3 -and $review.schema_version -eq 2 -and $review.model -ceq 'gpt-6-astra' -and $review.effort -ceq 'high' -and $request.profile.model -ceq $review.model -and $request.profile.effort -ceq $review.effort -and $request.checkout_root -ceq $review.checkout_root -and $request.worker_sha256 -ceq $review.codex_sha256 -and $request.worker_executable -ceq $identity.physical_executable -and $request.worker_sha256 -ceq $identity.executable_sha256 -and $request.adapter -ceq $identity.adapter) 'Logging request 3, review 2 and exact native profile; inventory 2 remains future evidence.'
Record 'fixed_policy' ($policy.argv.Count -eq 116 -and $request.profile.launch_policy_id -ceq $policy.policy_id -and $review.launch_policy_id -ceq $policy.policy_id -and $request.profile.launch_policy_sha256 -ceq (Digest (Join-Path $package 'src\restrictive-launch-policy.json')) -and $review.launch_policy_sha256 -ceq $request.profile.launch_policy_sha256) 'Exact compiled v3 record and all argument positions retained.'
Record 'closed_diagnostics_selection' ((KeysEqual $diagnostics @('schema_version','level','redaction_policy')) -and $diagnostics.schema_version -eq 1 -and $diagnostics.level -ceq 'debug' -and $diagnostics.redaction_policy -ceq 'closed-v1' -and $request.diagnostics_sha256 -ceq (Digest (Join-Path $root 'inputs\diagnostics.json')) -and (Get-Item -LiteralPath (Join-Path $root 'inputs\diagnostics.json')).Length -le 4096) 'Selected byte-bound config only; no operational configuration write.'
$native = @($commands.commands | Where-Object native_launch)
Record 'one_preflight_no_work_command' ($native.Count -eq 1 -and $native[0].argv[1] -ceq 'preflight' -and $commands.native_invocation_limit -eq 1 -and $commands.automatic_retries -eq 0 -and $commands.thread_starts -eq 0 -and $commands.turn_starts -eq 0 -and @($commands.commands | Where-Object {$_.operation -notin @('profile-sources','preflight','inspect')}).Count -eq 0) 'Five planned observations/invocations; only one native preflight, none executed.'
Record 'supervisor_and_rust_bounds' ($native[0].timeout_seconds -eq 145 -and $native[0].cancel_if_still_running_at_seconds -eq 135 -and $native[0].containment_and_finalization_reserve_seconds -eq 10 -and $commands.rust_deadlines_seconds.total -eq 120 -and $commands.rust_deadlines_seconds.rpc -eq 10 -and $commands.rust_deadlines_seconds.grace -eq 5 -and $commands.rust_deadlines_seconds.teardown -eq 5 -and @($commands.commands | Where-Object {-not $_.native_launch -and $_.timeout_seconds -ne 30}).Count -eq 0) 'Proposed outer budget and unchanged compiled bounds; supervisor implementation/checks remain pending.'
Record 'selected_probe_identity' ($commands.binary_sha256 -ceq 'cdd7de15eece11ad4c6f8b910ddca947bcc0ca0e98cd1ed939e61ddd73975bcd' -and @($commands.commands | Where-Object {$_.argv[0] -cne (Join-Path $qa 'build-target\debug\devforgeai-codex-worker-probe.exe') -or $_.cwd -cne 'C:\Projects\DevForgeAI'}).Count -eq 0) 'All planned product invocations use the QA-built probe on the selected host/cwd.'
$trial = 'C:\Projects\DevForgeAI\docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic'
Record 'future_layout_absent' (-not (Test-Path -LiteralPath $trial) -and $request.checkout_root -ceq (Join-Path $trial 'fixture') -and $request.run_dir -ceq (Join-Path $trial 'run')) 'No native runtime fixture or run created during planning.'
$linkRows = [Collections.Generic.List[object]]::new()
foreach ($name in @('native-diagnostic-plan.md','operator-review-handoff.md')) {
    $path = Join-Path $root $name
    $text = Get-Content -Raw -LiteralPath $path
    foreach ($match in [regex]::Matches($text, '\[[^\]]+\]\(([^\)]+)\)')) {
        $target = $match.Groups[1].Value
        if ($target -match '^[a-z]+://|^#') { continue }
        $absolute = [IO.Path]::GetFullPath((Join-Path $root ($target.Split('#')[0])))
        $exists = Test-Path -LiteralPath $absolute
        $linkRows.Add([ordered]@{document=$name;target=$target;resolved=$absolute;exists=$exists})
    }
}
Record 'local_markdown_links' (@($linkRows.ToArray() | Where-Object {-not $_.exists}).Count -eq 0) ([ordered]@{checked=$linkRows.Count;links=@($linkRows.ToArray())})
$bindings = Get-Content -Raw -LiteralPath (Join-Path $root 'planning-input-manifest.json') | ConvertFrom-Json
$badBindings = @($bindings | Where-Object {(Get-Item -LiteralPath $_.path).Length -ne $_.bytes -or (Digest $_.path) -cne $_.sha256})
Record 'prepared_input_manifest' ($badBindings.Count -eq 0) 'All five prepared input/template/command files reread by literal path.'
$badSyntax = @()
foreach ($path in Get-ChildItem -LiteralPath $root -Filter '*.ps1' -File) {
    $tokens=$null
    $parseErrors=$null
    [void][Management.Automation.Language.Parser]::ParseFile($path.FullName,[ref]$tokens,[ref]$parseErrors)
    if ($parseErrors.Count) { $badSyntax += $path.Name }
}
Record 'planning_helper_powershell_syntax' ($badSyntax.Count -eq 0) $badSyntax
$failures = @($checks.ToArray() | Where-Object {$_.result -ceq 'FAIL'})
$result = [ordered]@{utc=[DateTime]::UtcNow.ToString('o');command="& '$PSCommandPath'";cwd=(Get-Location).Path;exit_code=$(if($failures.Count){1}else{0});scope='Documentation, static template consistency, exact bytes and local links only';checks=@($checks.ToArray());failures=$failures.Count;native_codex='NOT_RUN';rust_profile_sources='NOT_RUN';new_product_tests='NOT_RUN';new_coverage='NOT_RUN';operator_review='PENDING';framework_acceptance='NOT_EVALUATED'}
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($result | ConvertTo-Json -Depth 18) + "`n")
$stream = [IO.File]::Open((Join-Path $root 'planning-checks.json'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length)} finally {$stream.Dispose()}
[ordered]@{checks=$checks.Count;failures=$failures.Count;exit_code=$result.exit_code;native_codex='NOT_RUN'} | ConvertTo-Json -Compress
exit $result.exit_code
