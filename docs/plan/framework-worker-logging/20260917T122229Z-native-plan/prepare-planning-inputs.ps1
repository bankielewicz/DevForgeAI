$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
# Creates documentation templates and byte copies only. Does not invoke any product binary.
$workspace = 'C:\Projects\DevForgeAI'
$package = Join-Path $workspace 'devforgeai\experiments\codex-worker-probe-logging-qa-fixes'
$trial = Join-Path $workspace 'docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic'
$fixture = Join-Path $trial 'fixture'
$inputs = Join-Path $trial 'inputs-001'
$probe = Join-Path $workspace 'docs\plan\framework-worker-logging\20260917T105456Z-qa-retest\build-target\debug\devforgeai-codex-worker-probe.exe'
$identity = Get-Content -Raw -LiteralPath (Join-Path $package 'src\native-executable-identity.json') | ConvertFrom-Json
$policyPath = Join-Path $package 'src\restrictive-launch-policy.json'
$policy = Get-Content -Raw -LiteralPath $policyPath | ConvertFrom-Json
function Digest([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function WriteNewJson([string]$Name, $Value) {
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes(($Value | ConvertTo-Json -Depth 15) + "`n")
    $stream = [IO.File]::Open((Join-Path $PSScriptRoot $Name), [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($bytes, 0, $bytes.Length) } finally { $stream.Dispose() }
}
if (Test-Path -LiteralPath $trial) { throw 'Future trial root must remain absent during planning.' }
$taskCopy = Join-Path $PSScriptRoot 'inputs\task.json'
[IO.File]::Copy((Join-Path $package 'tests\fixtures\task.json'), $taskCopy, $false)
$diagnostics = Join-Path $PSScriptRoot 'inputs\diagnostics.json'
$policyDigest = Digest $policyPath
$review = [ordered]@{
    schema_version=2; reviewer=$null; trial_selection_ref=$null; codex_sha256=$identity.executable_sha256
    checkout_root=$fixture; model='gpt-6-astra'; effort='high'; profile_sources=$null
    findings=[ordered]@{native_read_only_available=$null; no_external_tool_or_hook_effects=$null; codex_managed_chatgpt=$null; no_custom_provider=$null}
    launch_policy_id=$policy.policy_id; launch_policy_sha256=$policyDigest
    source_inventory_ref=(Join-Path $trial 'sources-002-prelaunch\stdout.bin'); source_inventory_sha256=$null
}
WriteNewJson 'review.template.json' $review
$request = [ordered]@{
    schema_version=3; diagnostics_ref=(Join-Path $inputs 'diagnostics.json'); diagnostics_sha256=(Digest $diagnostics)
    project_id='DevForgeAI'; checkout_id='logging-native-diagnostic'; work_id='no-work-profile-diagnostic'; run_id='20260917T122229Z-logging-diagnostic'
    candidate_sha256=(Digest $taskCopy); checkout_root=$fixture; run_dir=(Join-Path $trial 'run')
    worker_executable=$identity.physical_executable; worker_sha256=$identity.executable_sha256; adapter=$identity.adapter; scenario='complete'
    profile=[ordered]@{model='gpt-6-astra'; effort='high'; review_ref=(Join-Path $inputs 'review.json'); review_sha256=$null; launch_policy_id=$policy.policy_id; launch_policy_sha256=$policyDigest}
}
WriteNewJson 'request.template.json' $request
$commands = @(
    [ordered]@{id='sources-001'; operation='profile-sources'; argv=@($probe,'profile-sources','--checkout-root',$fixture); cwd=$workspace; timeout_seconds=30; native_launch=$false; stdin='DEVNULL'; evidence_directory=(Join-Path $trial 'sources-001')},
    [ordered]@{id='sources-002-prelaunch'; operation='profile-sources'; argv=@($probe,'profile-sources','--checkout-root',$fixture); cwd=$workspace; timeout_seconds=30; native_launch=$false; stdin='DEVNULL'; evidence_directory=(Join-Path $trial 'sources-002-prelaunch')},
    [ordered]@{id='native-001'; operation='preflight'; argv=@($probe,'preflight','--request',(Join-Path $inputs 'request.json')); cwd=$workspace; timeout_seconds=145; cancel_if_still_running_at_seconds=135; containment_and_finalization_reserve_seconds=10; native_launch=$true; stdin='PIPE held open with no input except explicit bounded cancellation'; evidence_directory=(Join-Path $trial 'native-001')},
    [ordered]@{id='sources-003-after'; operation='profile-sources'; argv=@($probe,'profile-sources','--checkout-root',$fixture); cwd=$workspace; timeout_seconds=30; native_launch=$false; stdin='DEVNULL'; evidence_directory=(Join-Path $trial 'sources-003-after')},
    [ordered]@{id='inspect-001'; operation='inspect'; argv=@($probe,'inspect','--run-dir',(Join-Path $trial 'run'),'--after','0','--limit','100'); cwd=$workspace; timeout_seconds=30; native_launch=$false; stdin='DEVNULL'; evidence_directory=(Join-Path $trial 'inspect-001')}
)
WriteNewJson 'command-plan.json' ([ordered]@{
    status='PLANNED_NOT_EXECUTED'; commands=$commands; native_invocation_limit=1; automatic_retries=0; thread_starts=0; turn_starts=0
    binary_sha256=(Digest $probe); rust_deadlines_seconds=[ordered]@{total=120; rpc=10; grace=5; teardown=5}
    input_version_rule='If prelaunch refresh requires different review/request bytes, preserve inputs-001 and operator review; bind a distinct inputs-002 before dispatch and record the final exact argv. Stop on unreviewed drift.'
    inspection_pagination='Use next_after with a fresh receipt per read-only page until an empty events page; preserve truncated_tail/state and all nonzero exits. Never replay native invocation.'
    output_rule='Create-new stdout.bin/stderr.bin and receipts; inventory hash refers to exact stdout bytes. Capture probe streams only, no additional raw worker logging.'
    supervisor_status='NOT_PREPARED_OR_TESTED'; launch_authorization='NOT_SELECTED'; operator_review='PENDING'; native_codex='NOT_RUN'; framework_acceptance='NOT_EVALUATED'
})
$inputsManifest = @('inputs\task.json','inputs\diagnostics.json','review.template.json','request.template.json','command-plan.json') | ForEach-Object {
    $path = Join-Path $PSScriptRoot $_
    [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $path).Length; sha256=(Digest $path)}
}
WriteNewJson 'planning-input-manifest.json' @($inputsManifest)
[ordered]@{status='TEMPLATES_CREATED';files=5;future_trial_root_exists=(Test-Path -LiteralPath $trial);native_codex='NOT_RUN';diagnostics_sha256=(Digest $diagnostics)} | ConvertTo-Json -Compress
