BeforeAll {
    $script:entry = Join-Path (Split-Path (Split-Path $PSScriptRoot)) 'scripts/artifact-relocation/Move-EvidenceCollection.ps1'
    . $script:entry
    function New-Fixture {
        $root = Join-Path $TestDrive ([guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path (Join-Path $root 'worktrees/collection') -Force | Out-Null
        & git -C $root init --initial-branch=main 2>&1 | Out-Null
        & git -C $root -c user.name=Fixture -c user.email=fixture@example.invalid commit --allow-empty -m initial 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'Fixture git setup failed.' }
        [IO.File]::WriteAllBytes((Join-Path $root 'worktrees/collection/日本語 file.bin'), [byte[]](0,255,128,13,10))
        $admission = Join-Path $root 'admission.json'
        @{ Version = 1; Root = $root; Collection = 'collection'; Owner = 'Fixture'; ReviewedUtc = [DateTime]::UtcNow.ToString('o'); Holds = @(); DependencyReview = 'No active location-dependent consumers in fixture.' } | ConvertTo-Json | Set-Content -LiteralPath $admission
        @{ Root = $root; Admission = $admission; Output = Join-Path $root 'receipts' }
    }
}

Describe 'Evidence relocation' {
    It 'moves an admitted collection and verifies every retained byte' -Tag Red {
        $fixture = New-Fixture
        $plan = New-RelocationPlan -ProjectRoot $fixture.Root -Collection collection -OutputDirectory $fixture.Output -AdmissionPath $fixture.Admission
        $result = Invoke-EvidenceRelocation -PlanPath $plan.PlanPath -ExpectedPlanSha256 $plan.SHA256 -Approve
        $result.Status | Should -Be 'VERIFIED'
        Test-Path -LiteralPath (Join-Path $fixture.Root 'worktrees/collection') | Should -BeFalse
        [Convert]::ToHexString([IO.File]::ReadAllBytes((Join-Path $fixture.Root 'artifacts/evidence/collection/日本語 file.bin'))) | Should -Be '00FF800D0A'
    }
}

Describe 'Relocation admission and preservation' {
    It 'preserves empty directories, hidden/read-only attributes and unrelated bytes' {
        $f = New-Fixture
        $payload = Join-Path $f.Root 'worktrees/collection'
        New-Item -ItemType Directory -Path (Join-Path $payload 'empty') | Out-Null
        $file = Join-Path $payload 'sealed.json'
        [IO.File]::WriteAllText($file, '{"historical":"C:\\old\\path"}')
        [IO.File]::SetAttributes($file, ([IO.FileAttributes]::ReadOnly -bor [IO.FileAttributes]::Hidden))
        [IO.File]::WriteAllText((Join-Path $f.Root 'unrelated.txt'),'unpublished sentinel')
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        $r = Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve
        $r.Files | Should -Be 2
        $moved = Join-Path $r.Destination 'sealed.json'
        [IO.File]::ReadAllText($moved) | Should -Be '{"historical":"C:\\old\\path"}'
        ([IO.File]::GetAttributes($moved) -band [IO.FileAttributes]::ReadOnly) | Should -Not -Be 0
        ([IO.File]::GetAttributes($moved) -band [IO.FileAttributes]::Hidden) | Should -Not -Be 0
        Test-Path -LiteralPath (Join-Path $r.Destination 'empty') | Should -BeTrue
        [IO.File]::ReadAllText((Join-Path $f.Root 'unrelated.txt')) | Should -Be 'unpublished sentinel'
        (Get-Content -LiteralPath $r.Receipt -Raw | ConvertFrom-Json).Status | Should -Be VERIFIED
        & git -C $f.Root check-ignore -q -- artifacts/evidence/collection/sealed.json
        $LASTEXITCODE | Should -Be 0
    }
    It 'requires explicit approval and the exact preview digest' {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 } | Should -Throw '*explicit*'
        { Invoke-EvidenceRelocation $p.PlanPath ('0' * 64) -Approve } | Should -Throw '*digest mismatch*'
        { Invoke-EvidenceRelocation $p.PlanPath 'invalid' -Approve } | Should -Throw '*digest mismatch*'
        Test-Path -LiteralPath (Join-Path $f.Root 'worktrees/collection') | Should -BeTrue
    }
    It 'rejects <Change> source drift after preview' -ForEach @(@{Change='bytes'},@{Change='new-file'},@{Change='deleted-file'},@{Change='attributes'}) {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        $file = Join-Path $f.Root 'worktrees/collection/日本語 file.bin'
        switch ($Change) {
            bytes { [IO.File]::WriteAllText($file,'changed') }
            new-file { [IO.File]::WriteAllText((Join-Path $f.Root 'worktrees/collection/new.txt'),'added') }
            deleted-file { [IO.File]::Delete($file) }
            attributes { [IO.File]::SetAttributes($file,[IO.FileAttributes]::Hidden) }
        }
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve } | Should -Throw '*Source changed*'
        Test-Path -LiteralPath (Join-Path $f.Root 'artifacts/evidence/collection') | Should -BeFalse
    }
    It 'refuses destination collisions at preview and execution' {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        $dest = Join-Path $f.Root 'artifacts/evidence/collection'
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
        [IO.File]::WriteAllText((Join-Path $dest 'sentinel'),'existing')
        { New-RelocationPlan $f.Root collection $f.Output $f.Admission } | Should -Throw '*Destination already exists*'
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve } | Should -Throw '*Destination already exists*'
        [IO.File]::ReadAllText((Join-Path $dest 'sentinel')) | Should -Be existing
    }
    It 'refuses invalid or protected collection <Name>' -ForEach @(@{Name='../escape'},@{Name='git'},@{Name='collection/child'},@{Name='-force'},@{Name='.'}) {
        $f = New-Fixture
        { Get-RelocationPaths $f.Root $Name } | Should -Throw '*literal non-Git*'
    }
    It 'rejects nonrepository, subdirectory, linked-root and registered nested worktree selection' {
        $f = New-Fixture
        { Get-RelocationPaths $TestDrive collection } | Should -Throw '*Git inspection failed*'
        { Get-RelocationPaths (Join-Path $f.Root 'worktrees') collection } | Should -Throw '*root*'
        $nested = Join-Path $f.Root 'worktrees/collection/nested-checkout'
        & git -C $f.Root worktree add --detach $nested 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'Fixture worktree creation failed.' }
        { Get-RelocationPaths $f.Root collection } | Should -Throw '*Registered worktree*'
        { Get-RelocationPaths $nested other } | Should -Throw '*primary checkout*'
    }
    It 'keeps receipts outside payloads, protected directories and other projects' {
        $f = New-Fixture
        foreach ($output in @((Join-Path $f.Root 'worktrees/collection/receipts'),(Join-Path $f.Root 'artifacts/evidence/collection/receipts'),(Join-Path $f.Root '.git/receipts'),$TestDrive)) {
            { New-RelocationPlan $f.Root collection $output $f.Admission } | Should -Throw
        }
    }
    It 'refuses admission <Problem>' -ForEach @(@{Problem='hold'},@{Problem='owner'},@{Problem='dependencies'},@{Problem='root'},@{Problem='version'},@{Problem='old'},@{Problem='future'}) {
        $f = New-Fixture
        $record = Get-Content -LiteralPath $f.Admission -Raw | ConvertFrom-Json
        switch ($Problem) {
            hold { $record.Holds = @('active investigation') }
            owner { $record.Owner = '' }
            dependencies { $record.DependencyReview = '' }
            root { $record.Root = $TestDrive }
            version { $record.Version = 2 }
            old { $record.ReviewedUtc = [DateTime]::UtcNow.AddDays(-2).ToString('o') }
            future { $record.ReviewedUtc = [DateTime]::UtcNow.AddDays(2).ToString('o') }
        }
        $record | ConvertTo-Json | Set-Content -LiteralPath $f.Admission
        { New-RelocationPlan $f.Root collection $f.Output $f.Admission } | Should -Throw '*Admission*'
        Test-Path -LiteralPath (Join-Path $f.Root 'worktrees/collection') | Should -BeTrue
    }
    It 'refuses an admission changed after preview' {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        $record = Get-Content -LiteralPath $f.Admission -Raw | ConvertFrom-Json
        $record.Owner = 'Another operator'
        $record | ConvertTo-Json | Set-Content -LiteralPath $f.Admission
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve } | Should -Throw '*Admission changed*'
    }
    It 'does not follow a collection junction or a destination ancestor junction' {
        $f = New-Fixture
        $outside = Join-Path $f.Root 'outside'
        New-Item -ItemType Directory -Path $outside | Out-Null
        [IO.File]::WriteAllText((Join-Path $outside 'sentinel'),'outside')
        $link = Join-Path $f.Root 'worktrees/collection/link'
        New-Item -ItemType Junction -Path $link -Target $outside | Out-Null
        try { { New-RelocationPlan $f.Root collection $f.Output $f.Admission } | Should -Throw '*Reparse*' }
        finally { [IO.Directory]::Delete($link) }
        $link = Join-Path $f.Root 'artifacts'
        New-Item -ItemType Junction -Path $link -Target $outside | Out-Null
        try { { New-RelocationPlan $f.Root collection $f.Output $f.Admission } | Should -Throw '*Reparse*' }
        finally { [IO.Directory]::Delete($link) }
        [IO.File]::ReadAllText((Join-Path $outside 'sentinel')) | Should -Be outside
    }
    It 'rejects missing collections, expired scan deadline and files locked against reads' {
        $f = New-Fixture
        { Get-RelocationTree (Join-Path $f.Root 'missing') } | Should -Throw '*missing*'
        { Get-RelocationTree (Join-Path $f.Root 'worktrees/collection') -TimeoutSeconds 0 } | Should -Throw '*deadline*'
        $stream = [IO.File]::Open((Join-Path $f.Root 'worktrees/collection/日本語 file.bin'),[IO.FileMode]::Open,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
        try { { New-RelocationPlan $f.Root collection $f.Output $f.Admission } | Should -Throw }
        finally { $stream.Dispose() }
    }
    It 'stops when process inspection is unavailable or a consumer is visible' {
        $f = New-Fixture
        Mock Get-CimInstance { throw [UnauthorizedAccessException]::new('Process visibility denied') }
        { New-RelocationPlan $f.Root collection $f.Output $f.Admission } | Should -Throw '*visibility denied*'
        Mock Get-CimInstance { [pscustomobject]@{ ProcessId = 2147483000; Name = 'fixture-worker'; CommandLine = 'worker ' + (Join-Path $f.Root 'docs/plan/collection/run.py') } }
        { New-RelocationPlan $f.Root collection $f.Output $f.Admission } | Should -Throw '*Known process*'
    }
    It 'retains a blocked receipt when a process appears at the final recheck' {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        $script:scanCalls = 0
        Mock Get-CimInstance {
            $script:scanCalls++
            if ($script:scanCalls -eq 2) { [pscustomobject]@{ ProcessId = 2147483000; Name = 'fixture-worker'; CommandLine = 'worker ' + (Join-Path $f.Root 'worktrees/collection/input') } }
        }
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve } | Should -Throw '*incomplete*Known process*'
        $receipt = Get-ChildItem -LiteralPath $f.Output -Filter 'receipt-*.json' | Get-Content -Raw | ConvertFrom-Json
        $receipt.Status | Should -Be BLOCKED
        $receipt.SourceExists | Should -BeTrue
        $receipt.DestinationExists | Should -BeFalse
    }
    It 'refuses a destination whose ignore marker exposes evidence' {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        New-Item -ItemType Directory -Path (Join-Path $f.Root 'artifacts') | Out-Null
        [IO.File]::WriteAllText((Join-Path $f.Root 'artifacts/.gitignore'),'# intentionally not ignored')
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve } | Should -Throw '*not ignored*'
        Test-Path -LiteralPath (Join-Path $f.Root 'worktrees/collection') | Should -BeTrue
    }
    It 'verifies a completed move after interruption without replaying it' {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        { Test-EvidenceRelocation $p.PlanPath $p.SHA256 } | Should -Throw '*Source still exists*'
        $dest = Join-Path $f.Root 'artifacts/evidence/collection'
        New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
        [IO.Directory]::Move((Join-Path $f.Root 'worktrees/collection'),$dest)
        (Test-EvidenceRelocation $p.PlanPath $p.SHA256).Status | Should -Be VERIFIED
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve } | Should -Throw '*use Verify*'
        [IO.File]::WriteAllText((Join-Path $dest '日本語 file.bin'),'corrupted after move')
        { Test-EvidenceRelocation $p.PlanPath $p.SHA256 } | Should -Throw '*Destination manifest mismatch*'
    }
    It 'retains moved bytes and a failure receipt when post-move verification fails' {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        $verify = ${function:Test-EvidenceRelocation}
        Mock Test-EvidenceRelocation {
            param($PlanPath,$ExpectedPlanSha256)
            [IO.File]::WriteAllText((Join-Path $f.Root 'artifacts/evidence/collection/日本語 file.bin'),'concurrent bytes retained')
            & $verify $PlanPath $ExpectedPlanSha256
        }
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve } | Should -Throw '*incomplete*manifest mismatch*'
        $receipt = Get-ChildItem -LiteralPath $f.Output -Filter 'receipt-*.json' | Get-Content -Raw | ConvertFrom-Json
        $receipt.SourceExists | Should -BeFalse
        $receipt.DestinationExists | Should -BeTrue
        [IO.File]::ReadAllText((Join-Path $f.Root 'artifacts/evidence/collection/日本語 file.bin')) | Should -Be 'concurrent bytes retained'
    }
    It 'refuses repeated attempt locks and never overwrites existing records' {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        [IO.File]::WriteAllText(($p.PlanPath + '.attempt.lock'),'prior uncertain attempt')
        { Invoke-EvidenceRelocation $p.PlanPath $p.SHA256 -Approve } | Should -Throw
        { Write-RelocationRecord $p.PlanPath @{ Status = 'fake' } } | Should -Throw
        (Get-FileHash -LiteralPath $p.PlanPath).Hash | Should -Be $p.SHA256
        Test-Path -LiteralPath (Join-Path $f.Root 'worktrees/collection') | Should -BeTrue
    }
    It 'rejects a self-consistent checksum on invalid plan <Problem>' -ForEach @(@{Problem='version'},@{Problem='source'},@{Problem='manifest'}) {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        $plan = Get-Content -LiteralPath $p.PlanPath -Raw | ConvertFrom-Json
        switch ($Problem) {
            version { $plan.Version = 2 }
            source { $plan.Source = Join-Path $f.Root 'unrelated' }
            manifest { $plan.TreeDigest = 'wrong' }
        }
        $plan | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $p.PlanPath
        $hash = (Get-FileHash -LiteralPath $p.PlanPath).Hash
        { Invoke-EvidenceRelocation $p.PlanPath $hash -Approve } | Should -Throw
        Test-Path -LiteralPath (Join-Path $f.Root 'worktrees/collection') | Should -BeTrue
    }
    It 'exposes Inventory Preview Relocate and Verify through the public script' {
        $f = New-Fixture
        $inventory = @(& $script:entry -Mode Inventory -ProjectRoot $f.Root -Collection collection)
        @($inventory | Where-Object Kind -EQ file).Count | Should -Be 1
        $p = & $script:entry -Mode Preview -ProjectRoot $f.Root -Collection collection -OutputDirectory $f.Output -AdmissionPath $f.Admission
        $r = & $script:entry -Mode Relocate -PlanPath $p.PlanPath -ExpectedPlanSha256 $p.SHA256 -Approve
        $r.Status | Should -Be VERIFIED
        (& $script:entry -Mode Verify -PlanPath $p.PlanPath -ExpectedPlanSha256 $p.SHA256).TreeDigest | Should -Be $r.TreeDigest
    }
}

Describe 'Receipt boundary regression' {
    It 'refuses an externally placed plan that would write receipts in <Location>' -Tag SafetyGap -ForEach @(@{Location='git-metadata'},@{Location='outside-project'}) {
        $f = New-Fixture
        $p = New-RelocationPlan $f.Root collection $f.Output $f.Admission
        $copied = if ($Location -eq 'git-metadata') { Join-Path $f.Root '.git/selected-plan.json' } else { Join-Path $TestDrive ([guid]::NewGuid().ToString('N') + '.json') }
        [IO.File]::Copy($p.PlanPath,$copied,$false)
        { Invoke-EvidenceRelocation $copied $p.SHA256 -Approve } | Should -Throw '*Receipt location*'
        Test-Path -LiteralPath (Join-Path $f.Root 'worktrees/collection') | Should -BeTrue
        Test-Path -LiteralPath ($copied + '.attempt.lock') | Should -BeFalse
    }
}
