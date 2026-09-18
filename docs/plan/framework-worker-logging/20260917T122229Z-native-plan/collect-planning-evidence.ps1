param([Parameter(Mandatory)][ValidateSet('intake','readback')][string]$Phase)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
# Evidence collection only: no product, native worker, configuration or policy mutations.
$started = [DateTime]::UtcNow.ToString('o')
$timer = [Diagnostics.Stopwatch]::StartNew()
$workspace = 'C:\Projects\DevForgeAI'
$qaRoot = Join-Path $workspace 'docs\plan\framework-worker-logging\20260917T105456Z-qa-retest'
$package = Join-Path $workspace 'devforgeai\experiments\codex-worker-probe-logging-qa-fixes'
$trialRoot = Join-Path $workspace 'docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic'
$qaSeal = '4ac2a9de0392e967fe65c64d782b06563cc11bd9171386b02651d4a6a545fbeb'
$cache = @{}
$problems = [Collections.Generic.List[string]]::new()
$groups = [Collections.Generic.List[object]]::new()
function Binding([string]$Path) {
    if (-not $cache.ContainsKey($Path)) {
        $item = Get-Item -Force -LiteralPath $Path
        if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Expected a regular file: $Path"
        }
        $cache[$Path] = [ordered]@{path=$item.FullName; bytes=$item.Length; sha256=(Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()}
    }
    return $cache[$Path]
}
function CheckBinding($Expected) {
    try {
        $actual = Binding $Expected.path
        if ($actual.bytes -ne $Expected.bytes -or $actual.sha256 -cne $Expected.sha256) {
            $problems.Add("Byte drift: $($Expected.path)")
        }
    } catch { $problems.Add("Unavailable binding: $($Expected.path): $($_.Exception.Message)") }
}
function CheckGroup([string]$Name, [string]$Manifest, $Rows) {
    $before = $problems.Count
    foreach ($row in $Rows) { CheckBinding $row }
    $groups.Add([ordered]@{name=$Name; manifest=(Binding $Manifest); files=@($Rows).Count; mismatches=$problems.Count-$before})
}
function WriteNewJson([string]$Path, $Value) {
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes(($Value | ConvertTo-Json -Depth 20) + "`n")
    $stream = [IO.File]::Open($Path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($bytes, 0, $bytes.Length) } finally { $stream.Dispose() }
}
$handoffPath = Join-Path $qaRoot 'handoff-manifest.json'
$handoffBinding = Binding $handoffPath
if ($handoffBinding.sha256 -cne $qaSeal) { throw 'Selected QA handoff SHA256 does not match.' }
$handoff = Get-Content -Raw -LiteralPath $handoffPath | ConvertFrom-Json
$handoffEntries = @($handoff.entries.PSObject.Properties | ForEach-Object {
    if ($_.Value.required_path -cne $_.Value.path) { throw "QA destination mismatch: $($_.Name)" }
    $_.Value
})
CheckGroup 'qa_handoff_entries' $handoffPath $handoffEntries
if ($problems.Count) { throw ($problems -join "`n") }
foreach ($name in @('candidate-manifest.json','specification-bindings.json','input-manifest.json','preserved-manifest.json','binary-manifest.json','independent-binary-manifest.json')) {
    $manifest = Join-Path $qaRoot $name
    CheckGroup $name $manifest @(Get-Content -Raw -LiteralPath $manifest | ConvertFrom-Json)
}
$evidenceLinks = [Collections.Generic.List[object]]::new()
foreach ($runName in @('20260917T105456Z-qa-retest','20260917T102726Z-dev-qa-fixes','20260917T023835Z-qa')) {
    $manifest = Join-Path $workspace "docs\plan\framework-worker-logging\$runName\evidence-manifest.json"
    $evidence = Get-Content -Raw -LiteralPath $manifest | ConvertFrom-Json
    CheckGroup "$runName retained evidence" $manifest $evidence.files
    if ($evidence.PSObject.Properties.Name -contains 'binaries') {
        CheckGroup "$runName retained binaries" $manifest $evidence.binaries
    }
    foreach ($link in $evidence.reparse_points) {
        $item = Get-Item -Force -LiteralPath $link.path
        $target = @($item.Target)
        $matches = $target.Count -eq 1 -and $target[0] -ceq $link.target -and [bool]($item.Attributes -band [IO.FileAttributes]::ReparsePoint)
        if (-not $matches) { $problems.Add("Evidence reparse metadata drift: $($link.path)") }
        $evidenceLinks.Add([ordered]@{path=$link.path; target=$target; matches=$matches; traversed=$false})
    }
}
$nativeIdentityPath = Join-Path $package 'src\native-executable-identity.json'
$pluginIdentityPath = Join-Path $package 'src\plugin-source-identity.json'
$identity = Get-Content -Raw -LiteralPath $nativeIdentityPath | ConvertFrom-Json
$pluginIdentity = Get-Content -Raw -LiteralPath $pluginIdentityPath | ConvertFrom-Json
$native = Binding $identity.physical_executable
if ($native.sha256 -cne $identity.executable_sha256) { $problems.Add('Pinned native executable digest drift.') }
$junctions = @()
foreach ($expected in @($identity.junctions) + @($pluginIdentity.junctions)) {
    $item = Get-Item -Force -LiteralPath $expected.path
    $target = @($item.Target)
    $matches = $item.LinkType -ceq 'Junction' -and $target.Count -eq 1 -and $target[0] -ceq $expected.target
    if (-not $matches) { $problems.Add("Compiled junction metadata drift: $($expected.path)") }
    $junctions += [ordered]@{path=$expected.path; link_type=$item.LinkType; target=$target; expected_target=$expected.target; matches=$matches; raw_reparse_tag_checked=$false; limitation='PowerShell metadata observation; Rust must perform complete final identity verification.'}
}
$guardNames = @([Environment]::GetEnvironmentVariables().Keys | Where-Object { $_ -match 'API_KEY|ACCESS_TOKEN|^OPENAI_BASE_URL$|^CODEX_HOME$' } | Sort-Object)
$policyPath = Join-Path $package 'src\restrictive-launch-policy.json'
$policy = Get-Content -Raw -LiteralPath $policyPath | ConvertFrom-Json
$helper = Binding (Join-Path $workspace 'Start-CodexAppServerDiagnostic.ps1')
if ($helper.sha256 -cne 'f69da72fb44737127dcfde3607fb0e027e4afeb2463a78ac8f844bc3abfc58a0') { $problems.Add('PowerShell helper drift.') }
$supplemental = @(
    (Binding (Join-Path $workspace 'AGENTS.md')),
    $helper,
    (Binding $nativeIdentityPath),
    (Binding $pluginIdentityPath),
    (Binding $policyPath),
    (Binding (Join-Path $package 'tests\fixtures\task.json')),
    (Binding (Join-Path $qaRoot 'build-target\debug\devforgeai-codex-worker-probe.exe')),
    (Binding (Join-Path $workspace 'docs\plan\framework-worker-native-diagnostics\20260916T202125Z\selection.md')),
    (Binding (Join-Path $workspace 'docs\plan\framework-worker-native-diagnostics\20260916T202125Z\diagnostic-report.md')),
    (Binding (Join-Path $workspace 'docs\plan\framework-worker-native-diagnostics\20260916T202125Z\diagnostic.py')),
    $native
)
$trialExists = Test-Path -LiteralPath $trialRoot
if ($trialExists) { $problems.Add('Proposed future trial root already exists; no reuse permitted.') }
if ($Phase -eq 'readback') {
    $baseline = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'intake-verification.json') | ConvertFrom-Json
    foreach ($group in $baseline.groups) { CheckBinding $group.manifest }
    foreach ($binding in $baseline.supplemental_bindings) { CheckBinding $binding }
    if (($baseline.environment.credential_or_home_names -join '|') -cne ($guardNames -join '|')) { $problems.Add('Relevant environment name set changed during planning.') }
}
$timer.Stop()
$result = [ordered]@{
    phase=$Phase; status=$(if($problems.Count){'DRIFT'}else{'VERIFIED'}); started_utc=$started; ended_utc=[DateTime]::UtcNow.ToString('o'); elapsed_seconds=$timer.Elapsed.TotalSeconds
    command="& '$PSCommandPath' -Phase $Phase"; cwd=(Get-Location).Path; collector=(Binding $PSCommandPath); exit_code=$(if($problems.Count){1}else{0})
    host=[ordered]@{shell=(Get-Process -Id $PID).Path; powershell=$PSVersionTable.PSVersion.ToString(); os=[Environment]::OSVersion.VersionString; architecture=[Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture.ToString(); filesystem=([IO.DriveInfo]::new('C:\')).DriveFormat; git_metadata_present=(Test-Path -LiteralPath (Join-Path $workspace '.git'))}
    qa_handoff=$handoffBinding; expected_qa_handoff_sha256=$qaSeal; groups=@($groups.ToArray()); unique_files_hashed=$cache.Count; supplemental_bindings=$supplemental
    evidence_junctions=@($evidenceLinks.ToArray()); current_compiled_junction_metadata=$junctions; launch_policy=[ordered]@{id=$policy.policy_id; argument_count=$policy.argv.Count; binding=(Binding $policyPath)}
    environment=[ordered]@{credential_or_home_names=$guardNames; credential_values_inspected_or_logged=$false; environment_mutated=$false; proposal='Separately select omission of ANTHROPIC_API_KEY from child copy only; stop on any other guarded variable or alternate CODEX_HOME.'}
    proposed_trial_root=$trialRoot; proposed_trial_root_exists=$trialExists; native_codex='NOT_RUN'; rust_profile_sources='NOT_RUN'; operator_findings='NOT_RECORDED'; framework_acceptance='NOT_EVALUATED'; problems=@($problems.ToArray())
    preservation_scope='Exact file bindings in the listed manifests and supplemental bindings, plus recorded reparse metadata without traversal. No claim over unindexed build intermediates or all unrelated repository bytes.'
}
WriteNewJson (Join-Path $PSScriptRoot "$Phase-verification.json") $result
[ordered]@{phase=$Phase;status=$result.status;exit_code=$result.exit_code;unique_files_hashed=$result.unique_files_hashed;groups=$groups.Count;elapsed_seconds=$timer.Elapsed.TotalSeconds;problems=@($problems.ToArray())} | ConvertTo-Json -Compress
exit $result.exit_code
