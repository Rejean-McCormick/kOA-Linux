[CmdletBinding()]
param(
    [switch]$Offline,
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Show-Usage {
    @'
Usage: tools/scripts/setup-development.ps1 [-Offline]

Bootstrap the locked workspace, install repository-local pre-commit hooks, and
verify that the kOA tooling CLI can display its stable help output.
'@ | Write-Output
}

function Stop-Setup([string]$Message, [int]$Code = 69) {
    [Console]::Error.WriteLine("setup-development: error: $Message")
    exit $Code
}

function Invoke-Checked([string]$Executable, [string[]]$Arguments) {
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "command failed with exit code $LASTEXITCODE: $Executable $($Arguments -join ' ')"
    }
}

if ($Help) {
    Show-Usage
    exit 0
}

$RepositoryRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$Bootstrap = Join-Path $PSScriptRoot 'bootstrap.ps1'

try {
    if ($Offline) {
        & $Bootstrap -Offline
    }
    else {
        & $Bootstrap
    }
    if ($LASTEXITCODE -ne 0) {
        throw "bootstrap failed with exit code $LASTEXITCODE"
    }

    Push-Location -LiteralPath $RepositoryRoot
    try {
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            Stop-Setup 'git is required to configure development hooks'
        }
        Invoke-Checked 'git' @('rev-parse', '--is-inside-work-tree')
        if (-not (Test-Path -LiteralPath '.pre-commit-config.yaml' -PathType Leaf)) {
            Stop-Setup 'missing .pre-commit-config.yaml'
        }

        Write-Output 'setup-development: installing repository-local pre-commit hook'
        Invoke-Checked 'uv' @('run', '--frozen', 'pre-commit', 'install')

        Write-Output 'setup-development: verifying CLI help'
        Invoke-Checked 'uv' @('run', '--frozen', 'python', '-m', 'koa_tools.cli', '--help')
        Write-Output 'setup-development: complete'
    }
    finally {
        Pop-Location
    }
}
catch {
    Stop-Setup $_.Exception.Message 1
}
