$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'venv creation failed' }
}
& .venv/Scripts/python.exe scripts/reproduce_all.py
if ($LASTEXITCODE -ne 0) { throw 'reproduction failed' }
