$target = Join-Path $PSScriptRoot 'ProbeTarget.ps1'
Describe 'coverage probe' {
    It 'runs a branch' {
        $shell = [PowerShell]::Create()
        try {
            [void]$shell.AddScript("& '$target' -Value 1")
            [void]$shell.Invoke()
            $shell.HadErrors | Should -Be $false
        } finally {
            $shell.Dispose()
        }
    }
}
