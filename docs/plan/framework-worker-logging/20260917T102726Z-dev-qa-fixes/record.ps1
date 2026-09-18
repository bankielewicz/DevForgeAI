param(
    [Parameter(Mandatory)][string]$Id,
    [Parameter(Mandatory)][ValidateSet('focused','list','coverage','fmt','format','clippy','build','supplemental')][string]$Check,
    [Parameter(Mandatory)][ValidateSet('setup','red','green','refactor','qa')][string]$Stage,
    [int]$TimeoutSeconds = 420
)
$ErrorActionPreference = 'Stop'
$evidenceRoot = $PSScriptRoot
$candidateRoot = 'C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes'
if ($Id -notmatch '^[0-9]{2}-[a-z0-9-]+$') { throw 'Invalid attempt id' }
$attemptRoot = Join-Path $evidenceRoot ('attempts\' + $Id)
if (Test-Path -LiteralPath $attemptRoot) { throw 'Attempt already exists; retain it and use a new id' }
[void][IO.Directory]::CreateDirectory($attemptRoot)
$source = @(Get-ChildItem -LiteralPath $candidateRoot -Recurse -File | Sort-Object FullName | ForEach-Object {
    [ordered]@{path=$_.FullName;relative_path=[IO.Path]::GetRelativePath($candidateRoot,$_.FullName);bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
})
$sourcePath = Join-Path $attemptRoot 'source-manifest.json'
$source | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $sourcePath -Encoding utf8
$manifest = Join-Path $candidateRoot 'Cargo.toml'
$common = @('--locked','--offline','--manifest-path',$manifest)
$commandArgs = switch ($Check) {
    'focused' { @('test') + $common + @('--test','inspection_consistency','--','--test-threads=1','--nocapture') }
    'list' { @('test') + $common + @('--all-targets','--','--list','--format','terse') }
    'coverage' { @('llvm-cov') + $common + @('--all-targets','--json','--output-path',(Join-Path $evidenceRoot 'coverage.json'),'--ignore-filename-regex','[/\\]tests[/\\]','--fail-under-lines','95','--','--test-threads=1') }
    'fmt' { @('fmt','--manifest-path',$manifest,'--all','--','--check') }
    'format' { @('fmt','--manifest-path',$manifest,'--all') }
    'clippy' { @('clippy') + $common + @('--all-targets','--','-D','warnings') }
    'build' { @('build') + $common + @('--bins') }
    'supplemental' { @('test','--locked','--offline','--manifest-path',(Join-Path $evidenceRoot 'supplemental-harness\Cargo.toml'),'--all-targets','--','--test-threads=1') }
}
$tool = (Get-Command cargo).Source
$overrides = [ordered]@{
    CARGO_TARGET_DIR=(Join-Path $evidenceRoot 'build-target')
    CARGO_LLVM_COV_TARGET_DIR=(Join-Path $evidenceRoot 'coverage-target')
    WF_TEST_EVIDENCE=(Join-Path $attemptRoot 'fixtures')
}
$receipt = [ordered]@{
    attempt_id=$Id;stage=$Stage;check=$Check;executable=$tool;argv=@($commandArgs);cwd=$candidateRoot
    platform='Windows x64, native C: filesystem';shell=(Get-Process -Id $PID).Path;shell_version=$PSVersionTable.PSVersion.ToString()
    executable_sha256=(Get-FileHash -LiteralPath $tool -Algorithm SHA256).Hash.ToLowerInvariant()
    recorder_sha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    source_manifest=$sourcePath;source_manifest_sha256=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
    environment_overrides=$overrides;timeout_seconds=$TimeoutSeconds;started_utc=[DateTime]::UtcNow.ToString('o')
}
$receiptPath = Join-Path $attemptRoot 'receipt.json'
$receipt | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $receiptPath -Encoding utf8
$start = [Diagnostics.ProcessStartInfo]::new($tool)
$start.WorkingDirectory = $candidateRoot
$start.UseShellExecute = $false
$start.CreateNoWindow = $true
$start.RedirectStandardOutput = $true
$start.RedirectStandardError = $true
foreach ($arg in $commandArgs) { [void]$start.ArgumentList.Add($arg) }
foreach ($key in $overrides.Keys) { $start.Environment[$key] = $overrides[$key] }
$process = [Diagnostics.Process]::new()
$process.StartInfo = $start
$watch = [Diagnostics.Stopwatch]::StartNew()
[void]$process.Start()
$receipt.owned_pid = $process.Id
$stdoutTask = $process.StandardOutput.ReadToEndAsync()
$stderrTask = $process.StandardError.ReadToEndAsync()
$timedOut = !$process.WaitForExit($TimeoutSeconds * 1000)
if ($timedOut) { $process.Kill($true); $process.WaitForExit() }
$stdoutPath = Join-Path $attemptRoot 'stdout.txt'
$stderrPath = Join-Path $attemptRoot 'stderr.txt'
[IO.File]::WriteAllText($stdoutPath,$stdoutTask.GetAwaiter().GetResult())
[IO.File]::WriteAllText($stderrPath,$stderrTask.GetAwaiter().GetResult())
$receipt.exit_code = $process.ExitCode
$receipt.timed_out = $timedOut
$receipt.ended_utc = [DateTime]::UtcNow.ToString('o')
$receipt.elapsed_seconds = $watch.Elapsed.TotalSeconds
$receipt.outputs = @($stdoutPath,$stderrPath) | ForEach-Object {
    [ordered]@{path=$_;bytes=(Get-Item -LiteralPath $_).Length;sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$receipt | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $receiptPath -Encoding utf8
$receipt | ConvertTo-Json -Depth 7 -Compress | Add-Content -LiteralPath (Join-Path $evidenceRoot 'execution-record.jsonl') -Encoding utf8
[pscustomobject]@{attempt=$Id;exit_code=$receipt.exit_code;timed_out=$timedOut;seconds=$receipt.elapsed_seconds;receipt=$receiptPath} | ConvertTo-Json
Get-Content -LiteralPath $stdoutPath -Tail 12
Get-Content -LiteralPath $stderrPath -Tail 12
exit $receipt.exit_code
