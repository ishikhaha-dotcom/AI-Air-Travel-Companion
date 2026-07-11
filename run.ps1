# WayFinder one-command launcher (Windows PowerShell)
# Usage: .\run.ps1          -> installs deps if needed, builds UI, starts server on :8000
param([switch]$SkipInstall)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not $SkipInstall) {
    Write-Host "== Installing backend deps ==" -ForegroundColor Cyan
    pip install -q -r backend/requirements.txt
    if (-not (Test-Path "frontend/node_modules")) {
        Write-Host "== Installing frontend deps ==" -ForegroundColor Cyan
        Push-Location frontend; npm install; Pop-Location
    }
}

if (-not (Test-Path "frontend/dist")) {
    Write-Host "== Building UI ==" -ForegroundColor Cyan
    Push-Location frontend; npm run build; Pop-Location
}

Write-Host "== Verifying (tests + benchmark harness) ==" -ForegroundColor Cyan
Push-Location backend
$env:PYTHONIOENCODING = "utf-8"
python -m pytest tests -q
python -m benchmark.run_benchmarks

Write-Host "== Starting WayFinder at http://localhost:8000 ==" -ForegroundColor Green
python -m uvicorn app.main:app --port 8000
Pop-Location
