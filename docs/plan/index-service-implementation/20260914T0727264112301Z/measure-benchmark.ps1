$ErrorActionPreference = 'Stop'
$runRoot = $PSScriptRoot
$startInfo = [Diagnostics.ProcessStartInfo]::new()
$startInfo.FileName = 'C:\Projects\DevForgeAI\devforgeai\target\release\examples\benchmark.exe'
$startInfo.WorkingDirectory = 'C:\Projects\DevForgeAI\devforgeai'
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true
$startInfo.ArgumentList.Add((Join-Path $runRoot 'benchmark-fixture-manifest-002.json'))
$hardware = Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors
$memory = Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
$process = [Diagnostics.Process]::Start($startInfo)
$timer = [Diagnostics.Stopwatch]::StartNew()
$samples = [Collections.Generic.List[object]]::new()
while (-not $process.WaitForExit(500)) {
    $process.Refresh()
    $samples.Add([pscustomobject]@{elapsed_ms=$timer.ElapsedMilliseconds;cpu_ms=$process.TotalProcessorTime.TotalMilliseconds;working_set_bytes=$process.WorkingSet64;peak_working_set_bytes=$process.PeakWorkingSet64})
    if ($timer.Elapsed.TotalSeconds -gt 1700) { $process.Kill(); $process.WaitForExit(); break }
}
$result = [pscustomobject]@{command=$startInfo.FileName;arguments=@($startInfo.ArgumentList);platform='Windows native';hardware=$hardware;memory=$memory;elapsed_ms=$timer.ElapsedMilliseconds;exit_code=$process.ExitCode;cpu_ms=$process.TotalProcessorTime.TotalMilliseconds;peak_working_set_bytes=$process.PeakWorkingSet64;samples=$samples}
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $runRoot 'benchmark-resources-002.json') -Encoding utf8
exit $process.ExitCode
