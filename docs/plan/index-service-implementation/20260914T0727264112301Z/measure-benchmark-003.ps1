$ErrorActionPreference = 'Stop'
$runRoot = $PSScriptRoot
$startInfo = [Diagnostics.ProcessStartInfo]::new()
$startInfo.FileName = 'C:\Projects\DevForgeAI\devforgeai\target\release\examples\benchmark.exe'
$startInfo.WorkingDirectory = 'C:\Projects\DevForgeAI\devforgeai'
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$startInfo.ArgumentList.Add((Join-Path $runRoot 'benchmark-fixture-manifest-003.json'))
$hardware = Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors
$memory = Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
$process = [Diagnostics.Process]::Start($startInfo)
$outFile = [IO.File]::Create((Join-Path $runRoot "benchmark-003.stdout.jsonl"))
$errFile = [IO.File]::Create((Join-Path $runRoot "benchmark-003.stderr.txt"))
$outCopy = $process.StandardOutput.BaseStream.CopyToAsync($outFile)
$errCopy = $process.StandardError.BaseStream.CopyToAsync($errFile)
$timer = [Diagnostics.Stopwatch]::StartNew()
$samples = [Collections.Generic.List[object]]::new()
while (-not $process.WaitForExit(500)) {
    $process.Refresh()
    $samples.Add([pscustomobject]@{elapsed_ms=$timer.ElapsedMilliseconds;cpu_ms=$process.TotalProcessorTime.TotalMilliseconds;working_set_bytes=$process.WorkingSet64;peak_working_set_bytes=$process.PeakWorkingSet64})
    if ($timer.Elapsed.TotalSeconds -gt 1700) { $process.Kill(); $process.WaitForExit(); break }
}
$outCopy.GetAwaiter().GetResult()
$errCopy.GetAwaiter().GetResult()
$outFile.Dispose()
$errFile.Dispose()
$result = [pscustomobject]@{command=$startInfo.FileName;arguments=@($startInfo.ArgumentList);platform='Windows native';hardware=$hardware;memory=$memory;elapsed_ms=$timer.ElapsedMilliseconds;exit_code=$process.ExitCode;cpu_ms=$process.TotalProcessorTime.TotalMilliseconds;peak_working_set_bytes=$process.PeakWorkingSet64;samples=$samples}
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $runRoot 'benchmark-resources-003.json') -Encoding utf8
exit $process.ExitCode
