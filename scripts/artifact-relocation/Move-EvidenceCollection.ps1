#Requires -Version 7.2
[CmdletBinding()]
param(
    [ValidateSet('Inventory','Preview','Relocate','Verify')][string]$Mode = 'Inventory',
    [string]$ProjectRoot,
    [string]$Collection,
    [string]$OutputDirectory,
    [string]$AdmissionPath,
    [string]$PlanPath,
    [string]$ExpectedPlanSha256,
    [switch]$Approve
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-RelocationGit {
    param([string]$Root, [string[]]$Arguments, [switch]$AllowFailure)
    $output = @(& git -C $Root @Arguments 2>&1)
    $code = $LASTEXITCODE
    if ($code -ne 0 -and -not $AllowFailure) { throw "Git inspection failed ($code): $output" }
    [pscustomobject]@{ ExitCode = $code; Text = $output -join "`n" }
}

function Assert-PlainRelocationPath {
    param([string]$Path)
    $current = [IO.Path]::GetFullPath($Path)
    while ($current) {
        $item = Get-Item -LiteralPath $current -Force -ErrorAction SilentlyContinue
        if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Reparse point refused: $current" }
        $current = [IO.Path]::GetDirectoryName($current)
    }
}

function Get-RelocationPaths {
    param([string]$Root, [string]$Name)
    if ($Name -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$' -or $Name -eq 'git') { throw 'Select one literal non-Git collection name.' }
    $rootPath = (Resolve-Path -LiteralPath $Root).Path
    Assert-PlainRelocationPath $rootPath
    $gitRoot = (Invoke-RelocationGit $rootPath @('rev-parse','--show-toplevel')).Text
    if ([IO.Path]::GetFullPath($gitRoot) -ne $rootPath) { throw 'Select the project root, not a subdirectory.' }
    $listing = (Invoke-RelocationGit $rootPath @('worktree','list','--porcelain','-z')).Text
    $registered = @($listing.Split([char]0) | Where-Object { $_.StartsWith('worktree ') } | ForEach-Object { [IO.Path]::GetFullPath($_.Substring(9)) })
    if ($registered[0] -ne $rootPath) { throw 'Select the primary checkout explicitly.' }
    $source = Join-Path $rootPath "worktrees/$Name"
    $destination = Join-Path $rootPath "artifacts/evidence/$Name"
    foreach ($path in @($source,$destination)) {
        Assert-PlainRelocationPath $path
        foreach ($worktree in $registered) {
            if ($worktree -eq $path -or $worktree.StartsWith($path + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Registered worktree inside selected collection.' }
        }
    }
    if ([IO.Path]::GetPathRoot($source) -ne [IO.Path]::GetPathRoot($destination)) { throw 'Relocation must remain on the same volume.' }
    [pscustomobject]@{ Root = $rootPath; Collection = $Name; Source = $source; Destination = $destination }
}

function Get-RelocationTree {
    param([string]$Path, [int]$TimeoutSeconds = 900)
    Assert-PlainRelocationPath $Path
    if (-not [IO.Directory]::Exists($Path)) { throw "Collection directory missing: $Path" }
    $watch = [Diagnostics.Stopwatch]::StartNew()
    $stack = [Collections.Generic.Stack[IO.DirectoryInfo]]::new()
    $stack.Push([IO.DirectoryInfo]::new($Path))
    $records = [Collections.Generic.List[object]]::new()
    while ($stack.Count) {
        if ($watch.Elapsed.TotalSeconds -ge $TimeoutSeconds) { throw 'Inventory deadline exceeded.' }
        $directory = $stack.Pop()
        $records.Add([pscustomobject][ordered]@{ Path = [IO.Path]::GetRelativePath($Path,$directory.FullName).Replace('\','/'); Kind = 'directory'; Bytes = 0; Attributes = [int]$directory.Attributes; SHA256 = '' })
        foreach ($item in $directory.EnumerateFileSystemInfos()) {
            if ($watch.Elapsed.TotalSeconds -ge $TimeoutSeconds) { throw 'Inventory deadline exceeded.' }
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point in collection: $($item.FullName)" }
            if ($item -is [IO.DirectoryInfo]) { $stack.Push($item); continue }
            $length = $item.Length
            $modified = $item.LastWriteTimeUtc
            $stream = [IO.File]::Open($item.FullName,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read)
            try { $hash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($stream)).ToLowerInvariant() }
            finally { $stream.Dispose() }
            $item.Refresh()
            if ($length -ne $item.Length -or $modified -ne $item.LastWriteTimeUtc) { throw 'File changed during capture.' }
            $records.Add([pscustomobject][ordered]@{ Path = [IO.Path]::GetRelativePath($Path,$item.FullName).Replace('\','/'); Kind = 'file'; Bytes = $length; Attributes = [int]$item.Attributes; SHA256 = $hash })
        }
    }
    @($records | Sort-Object Path)
}

function Get-TreeDigest {
    param([object[]]$Records)
    $json = ConvertTo-Json -InputObject @($Records) -Depth 4 -Compress
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($json))).ToLowerInvariant()
}

function Write-RelocationRecord {
    param([string]$Path, $Record)
    Assert-PlainRelocationPath $Path
    $null = [IO.Directory]::CreateDirectory((Split-Path $Path))
    $stream = [IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes(($Record | ConvertTo-Json -Depth 8))
        $stream.Write($bytes,0,$bytes.Length)
        $stream.Flush($true)
    }
    finally { $stream.Dispose() }
}

function Read-RelocationAdmission {
    param([string]$Path, $Paths)
    Assert-PlainRelocationPath $Path
    $hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    $record = [IO.File]::ReadAllText($Path) | ConvertFrom-Json
    if ($record.Version -ne 1 -or $record.Root -ne $Paths.Root -or $record.Collection -ne $Paths.Collection) { throw 'Admission identity mismatch.' }
    if ([string]::IsNullOrWhiteSpace($record.Owner) -or [string]::IsNullOrWhiteSpace($record.DependencyReview) -or @($record.Holds).Count) { throw 'Admission has holds or unresolved ownership/dependencies.' }
    $age = [DateTime]::UtcNow - ([DateTime]$record.ReviewedUtc).ToUniversalTime()
    if ($age.TotalHours -gt 24 -or $age.TotalMinutes -lt -5) { throw 'Admission review is stale or future-dated.' }
    if ((Get-FileHash -LiteralPath $Path).Hash -ne $hash) { throw 'Admission changed while reading.' }
    [pscustomobject]@{ Path = [IO.Path]::GetFullPath($Path); SHA256 = $hash; Record = $record }
}

function Assert-NoKnownCollectionProcess {
    param($Paths)
    $needles = @($Paths.Source,$Paths.Destination,(Join-Path $Paths.Root "docs/plan/$($Paths.Collection)")) | ForEach-Object { $_.Replace('\','/').ToLowerInvariant() }
    $processes = @(Get-CimInstance Win32_Process -ErrorAction Stop)
    foreach ($process in $processes) {
        if ($process.ProcessId -eq $PID -or -not $process.CommandLine) { continue }
        $command = $process.CommandLine.Replace('\','/').ToLowerInvariant()
        foreach ($needle in $needles) {
            if ($command.Contains($needle)) { throw "Known process references collection: PID $($process.ProcessId), $($process.Name)." }
        }
    }
}

function Assert-RelocationReceiptLocation {
    param($Paths, [string]$OutputDirectory)
    $output = [IO.Path]::GetFullPath($OutputDirectory)
    Assert-PlainRelocationPath $output
    if (-not $output.StartsWith($Paths.Root + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or $output -match '[\\/]\.(git|agents|codex|claude)([\\/]|$)') { throw 'Receipt location must be inside the project and outside protected directories.' }
    foreach ($payload in @($Paths.Source,$Paths.Destination)) { if ($output -eq $payload -or $output.StartsWith($payload + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Receipts must be outside the moved collection.' } }
}

function New-RelocationPlan {
    param([string]$ProjectRoot, [string]$Collection, [string]$OutputDirectory, [string]$AdmissionPath)
    $paths = Get-RelocationPaths $ProjectRoot $Collection
    $output = [IO.Path]::GetFullPath($OutputDirectory)
    Assert-RelocationReceiptLocation $paths $output
    if (Test-Path -LiteralPath $paths.Destination) { throw 'Destination already exists; inspect or Verify the prior outcome.' }
    $admission = Read-RelocationAdmission $AdmissionPath $paths
    Assert-NoKnownCollectionProcess $paths
    $tree = @(Get-RelocationTree $paths.Source)
    $plan = [ordered]@{ Version = 1; CreatedUtc = [DateTime]::UtcNow.ToString('o'); Root = $paths.Root; Collection = $Collection; Source = $paths.Source; Destination = $paths.Destination; Admission = $admission.Path; AdmissionSHA256 = $admission.SHA256; TreeDigest = Get-TreeDigest $tree; Tree = $tree }
    $file = Join-Path $output ('plan-' + [guid]::NewGuid().ToString('N') + '.json')
    Write-RelocationRecord $file $plan
    [pscustomobject]@{ PlanPath = $file; SHA256 = (Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant(); Collection = $Collection; Files = @($tree | Where-Object Kind -EQ file).Count; Bytes = ($tree | Measure-Object Bytes -Sum).Sum }
}

function Read-BoundRelocationPlan {
    param([string]$Path, [string]$ExpectedHash)
    Assert-PlainRelocationPath $Path
    if ($ExpectedHash -notmatch '^[a-fA-F0-9]{64}$' -or (Get-FileHash -LiteralPath $Path).Hash -ne $ExpectedHash) { throw 'Selected plan digest mismatch.' }
    $plan = [IO.File]::ReadAllText($Path) | ConvertFrom-Json
    if ((Get-FileHash -LiteralPath $Path).Hash -ne $ExpectedHash) { throw 'Plan changed while reading.' }
    if ($plan.Version -ne 1) { throw 'Unsupported relocation plan version.' }
    $paths = Get-RelocationPaths $plan.Root $plan.Collection
    if ($plan.Source -ne $paths.Source -or $plan.Destination -ne $paths.Destination -or $plan.TreeDigest -ne (Get-TreeDigest $plan.Tree)) { throw 'Plan paths or manifest digest mismatch.' }
    $fullPlan = [IO.Path]::GetFullPath($Path)
    Assert-RelocationReceiptLocation $paths (Split-Path $fullPlan)
    foreach ($payload in @($paths.Source,$paths.Destination)) { if ($fullPlan.StartsWith($payload + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Plan cannot be inside the payload.' } }
    [pscustomobject]@{ Plan = $plan; Paths = $paths }
}

function Initialize-EvidenceStorage {
    param($Paths)
    $storage = Join-Path $Paths.Root 'artifacts'
    Assert-PlainRelocationPath $storage
    $null = [IO.Directory]::CreateDirectory($storage)
    $marker = Join-Path $storage '.gitignore'
    if (-not (Test-Path -LiteralPath $marker)) {
        $stream = [IO.File]::Open($marker,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
        try { $stream.Write([Text.Encoding]::UTF8.GetBytes("*`n")); $stream.Flush($true) }
        finally { $stream.Dispose() }
    }
    $ignored = Invoke-RelocationGit $Paths.Root @('check-ignore','-q','--no-index','--',(Join-Path $Paths.Destination 'relocation-ignore-probe')) -AllowFailure
    if ($ignored.ExitCode -ne 0) { throw 'Evidence destination is not ignored; no collection moved.' }
    $null = [IO.Directory]::CreateDirectory((Split-Path $Paths.Destination))
}

function Test-EvidenceRelocation {
    param([string]$PlanPath, [string]$ExpectedPlanSha256)
    $bound = Read-BoundRelocationPlan $PlanPath $ExpectedPlanSha256
    if (Test-Path -LiteralPath $bound.Paths.Source) { throw 'Source still exists; relocation is not verified.' }
    $actual = @(Get-RelocationTree $bound.Paths.Destination)
    if ((Get-TreeDigest $actual) -ne $bound.Plan.TreeDigest) { throw 'Destination manifest mismatch.' }
    [pscustomobject]@{ Status = 'VERIFIED'; Collection = $bound.Plan.Collection; PlanSHA256 = $ExpectedPlanSha256; TreeDigest = $bound.Plan.TreeDigest; Files = @($actual | Where-Object Kind -EQ file).Count; Bytes = ($actual | Measure-Object Bytes -Sum).Sum; Destination = $bound.Paths.Destination }
}

function Invoke-EvidenceRelocation {
    param([string]$PlanPath, [string]$ExpectedPlanSha256, [switch]$Approve)
    if (-not $Approve) { throw 'Relocation requires explicit -Approve and the selected plan digest.' }
    $bound = Read-BoundRelocationPlan $PlanPath $ExpectedPlanSha256
    $plan = $bound.Plan; $paths = $bound.Paths
    if (Test-Path -LiteralPath $paths.Destination) { throw 'Destination already exists; use Verify instead of replaying the move.' }
    $admission = Read-RelocationAdmission $plan.Admission $paths
    if ($admission.SHA256 -ne $plan.AdmissionSHA256) { throw 'Admission changed after preview.' }
    Assert-NoKnownCollectionProcess $paths
    $before = @(Get-RelocationTree $paths.Source)
    if ((Get-TreeDigest $before) -ne $plan.TreeDigest) { throw 'Source changed after preview.' }
    Initialize-EvidenceStorage $paths
    $attempt = [IO.File]::Open(($PlanPath + '.attempt.lock'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    $receiptPath = Join-Path (Split-Path $PlanPath) ('receipt-' + [guid]::NewGuid().ToString('N') + '.json')
    try {
        Assert-NoKnownCollectionProcess $paths
        $null = Get-RelocationPaths $paths.Root $paths.Collection
        $latestAdmission = Read-RelocationAdmission $plan.Admission $paths
        if ($latestAdmission.SHA256 -ne $plan.AdmissionSHA256) { throw 'Admission changed before move.' }
        [IO.Directory]::Move($paths.Source,$paths.Destination)
        $result = Test-EvidenceRelocation $PlanPath $ExpectedPlanSha256
        $result | Add-Member -NotePropertyName Receipt -NotePropertyValue $receiptPath
        Write-RelocationRecord $receiptPath $result
        $result
    }
    catch {
        $failure = [ordered]@{ Status = 'BLOCKED'; Collection = $paths.Collection; PlanSHA256 = $ExpectedPlanSha256; SourceExists = [IO.Directory]::Exists($paths.Source); DestinationExists = [IO.Directory]::Exists($paths.Destination); Error = $_.Exception.Message }
        Write-RelocationRecord $receiptPath $failure
        throw "Relocation incomplete; inspect both paths and retained receipt $receiptPath. $($_.Exception.Message)"
    }
    finally { $attempt.Dispose() }
}

if ($MyInvocation.InvocationName -ne '.') {
    switch ($Mode) {
        Inventory { $paths = Get-RelocationPaths $ProjectRoot $Collection; Get-RelocationTree $paths.Source }
        Preview { New-RelocationPlan $ProjectRoot $Collection $OutputDirectory $AdmissionPath }
        Relocate { Invoke-EvidenceRelocation $PlanPath $ExpectedPlanSha256 -Approve:$Approve }
        Verify { Test-EvidenceRelocation $PlanPath $ExpectedPlanSha256 }
    }
}
