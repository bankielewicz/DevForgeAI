$ErrorActionPreference = 'Stop'
$TaskCasePath = Join-Path $PSScriptRoot 'trials/G02'
$TaskSaved = Get-Content -LiteralPath (Join-Path $TaskCasePath 'acl-original.json') -Raw | ConvertFrom-Json
$TaskActual = Get-Acl -LiteralPath $TaskSaved.target
$TaskOriginalDescriptor = [System.Security.AccessControl.RawSecurityDescriptor]::new($TaskSaved.sddl)
$TaskActualDescriptor = [System.Security.AccessControl.RawSecurityDescriptor]::new($TaskActual.Sddl)
function Get-TaskAceStrings($Descriptor) {
    foreach ($TaskAce in $Descriptor.DiscretionaryAcl) {
        $TaskBytes = [byte[]]::new($TaskAce.BinaryLength)
        $TaskAce.GetBinaryForm($TaskBytes, 0)
        [Convert]::ToBase64String($TaskBytes)
    }
}
$TaskBeforeEntries = @(Get-TaskAceStrings $TaskOriginalDescriptor)
$TaskAfterEntries = @(Get-TaskAceStrings $TaskActualDescriptor)
$TaskMissing = @($TaskBeforeEntries | Where-Object { $_ -notin $TaskAfterEntries })
$TaskAdded = @($TaskAfterEntries | Where-Object { $_ -notin $TaskBeforeEntries })
$TaskExplicitDenies = @($TaskActual.Access | Where-Object { -not $_.IsInherited -and $_.AccessControlType -eq 'Deny' })
if ($TaskMissing.Count -ne 0 -or $TaskExplicitDenies.Count -ne 0 -or $TaskOriginalDescriptor.Owner.Value -ne $TaskActualDescriptor.Owner.Value -or $TaskOriginalDescriptor.Group.Value -ne $TaskActualDescriptor.Group.Value) { throw 'Unexpected ACL cleanup state.' }
$TaskRecord = [ordered]@{
    timestamp = [DateTimeOffset]::UtcNow.ToString('o')
    target = $TaskSaved.target
    original_sddl = $TaskSaved.sddl
    actual_sddl = $TaskActual.Sddl
    exact_sddl_match = ($TaskSaved.sddl -eq $TaskActual.Sddl)
    original_entries_retained = ($TaskMissing.Count -eq 0)
    explicit_deny_count = $TaskExplicitDenies.Count
    added_entries_binary_base64 = $TaskAdded
    actual_access = @($TaskActual.Access | Select-Object IdentityReference, FileSystemRights, AccessControlType, IsInherited, InheritanceFlags, PropagationFlags)
    conclusion = 'Injected deny removed; original entries and owner/group retained. Additional inherited access is recorded without attribution; exact final SDDL equality is not claimed.'
}
$TaskOut = Join-Path $TaskCasePath 'acl-readback.json'
$TaskBytes = [System.Text.UTF8Encoding]::new($false).GetBytes(($TaskRecord | ConvertTo-Json -Depth 8) + "`n")
$TaskStream = [System.IO.File]::Open($TaskOut, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
try { $TaskStream.Write($TaskBytes, 0, $TaskBytes.Length) } finally { $TaskStream.Dispose() }
[pscustomobject]@{ result='OBSERVED'; exact_sddl_match=$TaskRecord.exact_sddl_match; added_entries=$TaskAdded.Count; injected_deny_removed=$true } | ConvertTo-Json -Compress
