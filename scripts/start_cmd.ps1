# ============================================================
# start_cmd.ps1
# Starts the interactive CLI client
# ============================================================
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  Starting Interactive CLI Client       " -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""

Set-Location $ProjectRoot
uv run python -m app.cmd.cmd
