# ============================================================
# start_website_builder.ps1
# Starts the Website Builder Simple Agent on port 10000
# ============================================================
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Starting Website Builder Agent        " -ForegroundColor Green
Write-Host "  Port: 10000                           " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Set-Location $ProjectRoot
uv run python -m agents.website_builder_simple
