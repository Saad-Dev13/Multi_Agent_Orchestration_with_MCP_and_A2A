# ============================================================
# start_mcp_server.ps1
# Starts the MCP Streamable HTTP Server on port 3000
# ============================================================
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting MCP Streamable HTTP Server   " -ForegroundColor Cyan
Write-Host "  Port: 3000                            " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $ProjectRoot
uv run .\mcp\servers\streamable_http_server.py
