param(
    [Parameter(Mandatory = $true)][string] $Launcher,
    [Parameter(Mandatory = $true)][string] $Request,
    [Parameter(Mandatory = $true)][string] $Briefing,
    [Parameter(Mandatory = $true)][string] $RunDir,
    [Parameter(Mandatory = $true)][string] $PolicyOutput
)

Get-ExecutionPolicy -List | Select-Object Scope, ExecutionPolicy | ConvertTo-Json | Set-Content -LiteralPath $PolicyOutput -Encoding UTF8
& $Launcher -Request $Request -Briefing $Briefing -RunDir $RunDir -Reason initial -Python 'C:\Program Files\Python310\python.exe' -ShowProgress
exit $LASTEXITCODE
