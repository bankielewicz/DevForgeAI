$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
# Seals this documentation packet only. Does not decide product acceptance.
function Binding([string]$Path) {
    $item=Get-Item -LiteralPath $Path
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function WriteNewJson([string]$Name, $Value) {
    $bytes=[Text.UTF8Encoding]::new($false).GetBytes(($Value | ConvertTo-Json -Depth 20)+"`n")
    $stream=[IO.File]::Open((Join-Path $PSScriptRoot $Name),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
}
$readback=Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'readback-v2-verification.json') | ConvertFrom-Json
$checks=Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'planning-checks.json') | ConvertFrom-Json
if($readback.status -cne 'VERIFIED' -or $checks.failures -ne 0){throw 'Cannot seal failed planning verification.'}
$linkCount=0
foreach($file in Get-ChildItem -LiteralPath $PSScriptRoot -File -Filter '*.md'){
    foreach($match in [regex]::Matches((Get-Content -Raw -LiteralPath $file.FullName),'\[[^\]]+\]\(([^\)]+)\)')){
        $target=$match.Groups[1].Value
        if($target -match '^[a-z]+://|^#'){continue}
        $absolute=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot ($target.Split('#')[0])))
        if(-not(Test-Path -LiteralPath $absolute)){throw "Broken link: $target"}
        $linkCount++
    }
}
$syntaxCount=0
foreach($file in Get-ChildItem -LiteralPath $PSScriptRoot -File -Filter '*.ps1'){
    $tokens=$null
    $errors=$null
    [void][Management.Automation.Language.Parser]::ParseFile($file.FullName,[ref]$tokens,[ref]$errors)
    if($errors.Count){throw "PowerShell syntax error: $($file.FullName)"}
    $syntaxCount++
}
$created=@(Get-ChildItem -LiteralPath $PSScriptRoot -Recurse -File | Sort-Object FullName | ForEach-Object{Binding $_.FullName})
WriteNewJson 'changed-files.json' ([ordered]@{scope=$PSScriptRoot;operation='Create fresh planning packet';created_bindings_before_sealing=$created;additional_created_seal_files=@('changed-files.json','handoff-manifest.json','final-readback.json');modified_existing_files=@();deleted_files=@();note='Seal files are bound by handoff/final readback; no recursive self-hash. All candidate, operational and prior evidence paths remain outside the write scope.'})
$entries=[ordered]@{}
foreach($file in Get-ChildItem -LiteralPath $PSScriptRoot -Recurse -File | Sort-Object FullName){
    $relative=[IO.Path]::GetRelativePath($PSScriptRoot,$file.FullName).Replace('\','/')
    $binding=Binding $file.FullName
    $entries[$relative]=[ordered]@{required_path=$binding.path;path=$binding.path;bytes=$binding.bytes;sha256=$binding.sha256}
}
$qaRoot='C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T105456Z-qa-retest'
WriteNewJson 'handoff-manifest.json' ([ordered]@{
    schema_version=1;purpose='Native diagnostic planning and operator-review handoff only';created_utc=[DateTime]::UtcNow.ToString('o');required_destination=$PSScriptRoot;actual_destination=$PSScriptRoot
    workspace='C:\Projects\DevForgeAI';platform='Native Windows x64 / PowerShell 7.6.6 / C: NTFS';candidate_root='C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes'
    planning_status='COMPLETE';launch_readiness='PENDING_OPERATOR_REVIEW_AND_SEPARATE_SELECTION';native_codex='NOT_RUN';framework_acceptance='NOT_EVALUATED'
    selected_qa_handoff=(Binding (Join-Path $qaRoot 'handoff-manifest.json'));expected_qa_handoff_sha256='4ac2a9de0392e967fe65c64d782b06563cc11bd9171386b02651d4a6a545fbeb'
    candidate_manifest=(Binding (Join-Path $qaRoot 'candidate-manifest.json'));selected_probe=(Binding (Join-Path $qaRoot 'build-target\debug\devforgeai-codex-worker-probe.exe'));specification_bindings=(Binding (Join-Path $qaRoot 'specification-bindings.json'))
    inherited_qa=[ordered]@{verdict='PASS';required_cases='178/178';unit_cases='49/49';executed_lines='3872/4057';qa_findings='VERIFIED_FIXED by independent QA; no lifecycle changes in planning';report=(Binding (Join-Path $qaRoot 'qa-report.md'))}
    proposed_native_attempts=1;authorized_native_attempts_this_task=0;proposed_trial_root=$readback.proposed_trial_root;proposed_trial_root_created=$false
    unresolved=@('Separate trial/model/effort selection','Named operator review and rationale','Fresh compiled source inventory','Final review/request binding','Child-only environment selection','Reviewed and offline-tested supervisor','Runtime startup/profile/account/model/capture/cleanup observations')
    entries=$entries;excluded_self_and_final_readback=@('handoff-manifest.json','final-readback.json')
})
$sealPath=Join-Path $PSScriptRoot 'handoff-manifest.json'
$seal=Get-Content -Raw -LiteralPath $sealPath | ConvertFrom-Json
foreach($property in $seal.entries.PSObject.Properties){
    $expected=$property.Value
    $actual=Binding $expected.path
    if($expected.required_path -cne $expected.path -or $actual.bytes -ne $expected.bytes -or $actual.sha256 -cne $expected.sha256){throw "Seal readback mismatch: $($property.Name)"}
}
WriteNewJson 'final-readback.json' ([ordered]@{utc=[DateTime]::UtcNow.ToString('o');status='READBACK_VERIFIED';command="& '$PSCommandPath'";cwd=(Get-Location).Path;exit_code=0;handoff=(Binding $sealPath);entries_checked=@($seal.entries.PSObject.Properties).Count;local_markdown_links_checked=$linkCount;powershell_files_parsed=$syntaxCount;preservation_receipt=(Binding (Join-Path $PSScriptRoot 'readback-v2-verification.json'));native_codex='NOT_RUN';operator_review='PENDING';framework_acceptance='NOT_EVALUATED';problems=@()})
[ordered]@{status='READBACK_VERIFIED';handoff=(Binding $sealPath);entries=@($seal.entries.PSObject.Properties).Count;local_links=$linkCount;native_codex='NOT_RUN'} | ConvertTo-Json -Compress
