# ============================================================
# start_all.ps1
#
# Orchestrated startup script for the Multi-Agent System.
# Starts each service in a NEW terminal window and waits for
# it to be fully ready (port accepting connections) before
# moving on to the next.
#
# Start Order:
#   1. MCP Server              (port 3000)
#   2. Website Builder Agent   (port 10000)
#   3. Host Agent              (port 10001)
#   4. Interactive CLI         (this terminal - interactive)
# ============================================================

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

# ── Helpers ──────────────────────────────────────────────────────────────────

function Write-Banner {
    param([string]$Title, [string]$Port, [ConsoleColor]$Color)
    Write-Host ""
    Write-Host ("=" * 50) -ForegroundColor $Color
    Write-Host "  $Title" -ForegroundColor $Color
    if ($Port) { Write-Host "  Port: $Port" -ForegroundColor $Color }
    Write-Host ("=" * 50) -ForegroundColor $Color
    Write-Host ""
}

function Wait-ForPort {
    param(
        [string]$ServiceName,
        [int]$Port,
        [int]$TimeoutSeconds = 60,
        [int]$RetryIntervalMs = 500
    )

    Write-Host "[Wait] Waiting for $ServiceName to be ready on port $Port ..." -ForegroundColor DarkCyan
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

    while ($stopwatch.Elapsed.TotalSeconds -lt $TimeoutSeconds) {
        try {
            $conn = New-Object System.Net.Sockets.TcpClient
            $conn.Connect("127.0.0.1", $Port)
            $conn.Close()
            Write-Host "[OK]   $ServiceName is UP on port $Port  ($([Math]::Round($stopwatch.Elapsed.TotalSeconds, 1))s)" -ForegroundColor Green
            return $true
        }
        catch {
            Start-Sleep -Milliseconds $RetryIntervalMs
        }
    }

    Write-Host "[FAIL] $ServiceName did NOT start within ${TimeoutSeconds}s on port $Port" -ForegroundColor Red
    Write-Host "       Check the terminal window for that service for errors." -ForegroundColor Red
    return $false
}

function Start-ServiceWindow {
    param(
        [string]$Title,
        [string]$Command,
        [ConsoleColor]$Color = [ConsoleColor]::White
    )

    $titleArg = $Title -replace '"', '\"'
    # Run in a new PowerShell window so each service has its own visible console
    $psArgs = @(
        "-NoExit",
        "-Command",
        "& { `$host.UI.RawUI.WindowTitle = '$titleArg'; Set-Location '$ProjectRoot'; $Command }"
    )

    Write-Host "[Start] Launching '$Title' in a new window..." -ForegroundColor $Color
    Start-Process powershell.exe -ArgumentList $psArgs
}

# ── Startup Sequence ─────────────────────────────────────────────────────────

Write-Banner -Title "Multi-Agent Orchestration Startup" -Port "" -Color Cyan

# ── 1. MCP Server ─────────────────────────────────────────────────────────────
Write-Banner -Title "Step 1/3: MCP Streamable HTTP Server" -Port "3000" -Color Cyan

Start-ServiceWindow `
    -Title "MCP Server (port 3000)" `
    -Command "uv run .\mcp\servers\streamable_http_server.py" `
    -Color Cyan

$ready = Wait-ForPort -ServiceName "MCP Server" -Port 3000 -TimeoutSeconds 60
if (-not $ready) {
    Write-Host ""
    Write-Host "[ABORT] Cannot continue without the MCP Server. Exiting." -ForegroundColor Red
    exit 1
}

# ── 2. Website Builder Agent ──────────────────────────────────────────────────
Write-Banner -Title "Step 2/3: Website Builder Agent" -Port "10000" -Color Green

Start-ServiceWindow `
    -Title "Website Builder Agent (port 10000)" `
    -Command "uv run python -m agents.website_builder_simple" `
    -Color Green

$ready = Wait-ForPort -ServiceName "Website Builder Agent" -Port 10000 -TimeoutSeconds 90
if (-not $ready) {
    Write-Host ""
    Write-Host "[ABORT] Cannot continue without the Website Builder Agent. Exiting." -ForegroundColor Red
    exit 1
}

# ── 3. Host Agent ─────────────────────────────────────────────────────────────
Write-Banner -Title "Step 3/3: Host Agent" -Port "10001" -Color Yellow

Start-ServiceWindow `
    -Title "Host Agent (port 10001)" `
    -Command "uv run python -m agents.host_agent" `
    -Color Yellow

$ready = Wait-ForPort -ServiceName "Host Agent" -Port 10001 -TimeoutSeconds 120
if (-not $ready) {
    Write-Host ""
    Write-Host "[ABORT] Cannot continue without the Host Agent. Exiting." -ForegroundColor Red
    exit 1
}

# ── 4. Interactive CLI (in THIS terminal) ─────────────────────────────────────
Write-Banner -Title "All Services Ready! Starting CLI Client" -Port "" -Color Magenta

Write-Host "[Info] The CLI client runs interactively in THIS terminal window." -ForegroundColor DarkGray
Write-Host "[Info] Type ':q' or 'quit' to exit the CLI." -ForegroundColor DarkGray
Write-Host ""

Set-Location $ProjectRoot
uv run python -m app.cmd.cmd
