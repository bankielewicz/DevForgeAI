param(
    [Parameter(Mandatory)][ValidateSet('Deny','Restore')][string]$Action,
    [Parameter(Mandatory)][string]$Target,
    [Parameter(Mandatory)][string]$StatePath
)
$ErrorActionPreference = 'Stop'
$TaskRunRoot = [System.IO.Path]::GetFullPath($PSScriptRoot)
$TaskTargetPath = [System.IO.Path]::GetFullPath($Target)
$TaskStatePath = [System.IO.Path]::GetFullPath($StatePath)
$TaskControlRoot = Join-Path $TaskRunRoot 'harness-controls'
$TaskDenialTarget = Join-Path $TaskRunRoot 'trials\G02\project\backlog'
if (-not ($TaskTargetPath -eq $TaskDenialTarget -or $TaskTargetPath.StartsWith($TaskControlRoot + '\', [System.StringComparison]::OrdinalIgnoreCase))) { throw 'Target is outside declared synthetic fault roots.' }
if (-not $TaskStatePath.StartsWith($TaskRunRoot + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'ACL state must stay in the validation run.' }
$TaskItem = Get-Item -LiteralPath $TaskTargetPath -Force
if (-not $TaskItem.PSIsContainer -or ($TaskItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) { throw 'Target must be a plain synthetic directory.' }
if ($Action -eq 'Deny') {
    $TaskAcl = Get-Acl -LiteralPath $TaskTargetPath
    $TaskState = @{ target = $TaskTargetPath; sddl = $TaskAcl.Sddl } | ConvertTo-Json -Compress
    $TaskStream = [System.IO.File]::Open($TaskStatePath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
    try {
        $TaskBytes = [System.Text.UTF8Encoding]::new($false).GetBytes($TaskState)
        $TaskStream.Write($TaskBytes, 0, $TaskBytes.Length)
    } finally { $TaskStream.Dispose() }
    $TaskEveryone = [System.Security.Principal.SecurityIdentifier]::new('S-1-1-0')
    $TaskRights = [System.Security.AccessControl.FileSystemRights]::CreateFiles -bor [System.Security.AccessControl.FileSystemRights]::CreateDirectories
    $TaskRule = [System.Security.AccessControl.FileSystemAccessRule]::new($TaskEveryone, $TaskRights, [System.Security.AccessControl.InheritanceFlags]::None, [System.Security.AccessControl.PropagationFlags]::None, [System.Security.AccessControl.AccessControlType]::Deny)
    $TaskAcl.AddAccessRule($TaskRule)
    Set-Acl -LiteralPath $TaskTargetPath -AclObject $TaskAcl
    @{ action = $Action; result = 'DENY_APPLIED' } | ConvertTo-Json -Compress
} else {
    $TaskState = Get-Content -Raw -LiteralPath $TaskStatePath | ConvertFrom-Json
    if ($TaskState.target -ne $TaskTargetPath) { throw 'Recorded ACL target does not match.' }
    $TaskAcl = Get-Acl -LiteralPath $TaskTargetPath
    $TaskAcl.SetSecurityDescriptorSddlForm($TaskState.sddl)
    Set-Acl -LiteralPath $TaskTargetPath -AclObject $TaskAcl
    @{ action = $Action; result = 'RESTORED' } | ConvertTo-Json -Compress
}
