# ============================================================
# start_host_agent.ps1
# Starts the Host Agent on port 10001
# ============================================================
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Starting Host Agent                   " -ForegroundColor Yellow
Write-Host "  Port: 10001                           " -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Set-Location $ProjectRoot
uv run python -m agents.host_agent
