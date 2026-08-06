[CmdletBinding()]
param(
    [switch]$Offline,
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Show-Usage {
    @'
Usage: tools/scripts/bootstrap.ps1 [-Offline]

Validate the locked Python workspace and synchronize its local .venv with UV.
UV and Python must already be supplied by the active development profile.
'@ | Write-Output
}

function Stop-Bootstrap([string]$Message, [int]$Code = 69) {
    [Console]::Error.WriteLine("bootstrap: error: $Message")
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
foreach ($Marker in @('pyproject.toml', 'uv.lock', '.python-version')) {
    if (-not (Test-Path -LiteralPath (Join-Path $RepositoryRoot $Marker) -PathType Leaf)) {
        Stop-Bootstrap "missing required workspace marker: $Marker"
    }
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Stop-Bootstrap 'python is not available from the active profile'
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Stop-Bootstrap 'uv is not available from the active profile'
}

Push-Location -LiteralPath $RepositoryRoot
try {
    Write-Output "bootstrap: repository root: $RepositoryRoot"
    Write-Output 'bootstrap: verifying uv.lock'
    Invoke-Checked 'uv' @('lock', '--check')

    if ($Offline) {
        Write-Output 'bootstrap: synchronizing .venv from frozen inputs (offline)'
        $PreviousOffline = [Environment]::GetEnvironmentVariable('UV_OFFLINE', 'Process')
        try {
            [Environment]::SetEnvironmentVariable('UV_OFFLINE', '1', 'Process')
            Invoke-Checked 'uv' @('sync', '--frozen', '--all-groups')
        }
        finally {
            [Environment]::SetEnvironmentVariable('UV_OFFLINE', $PreviousOffline, 'Process')
        }
    }
    else {
        Write-Output 'bootstrap: synchronizing .venv from frozen inputs'
        Invoke-Checked 'uv' @('sync', '--frozen', '--all-groups')
    }
    Write-Output 'bootstrap: complete'
}
catch {
    Stop-Bootstrap $_.Exception.Message 1
}
finally {
    Pop-Location
}
