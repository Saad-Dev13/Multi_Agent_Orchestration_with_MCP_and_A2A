# Project Status

Use this file to track what has been done so far and whether the work has been pushed to GitHub.

## Current Status
- Last updated: 2026-07-16
- Current branch: master
- Working tree status: Uncommitted documentation updates present
- Pushed to GitHub: Yes

## What Has Been Done
- Fixed the MCP server tool decorator in `mcp/servers/terminal_server/terminal_server.py`.
- Created a valid default workspace path for the terminal server and switched it to `Desktop\Test_folder`.
- Confirmed the Claude Desktop MCP config is pointing at `uv.exe` and the server folder.
- Created project-level tracking files for fixes and status.
- Added a streamable HTTP arithmetic MCP server in `mcp/servers/streamable_http_server.py`.
- Added a Claude Desktop remote connector entry for `arithmetic_server`.
- Verified the arithmetic server starts on `http://localhost:3000`.
- Updated the README to reflect the early-stage project showcase and two-server setup.
- Reframed the documentation around the full A2A/MCP architecture.
- Added a self-contained Mermaid overview to the README.
- Documented the intended frontend, host agent/orchestrator, agent registry, and remote A2A layers as future work.
- Added a standalone utilities-side MCP config at `utilities/mcp/mcp_config.json`.
- Updated `utilities/mcp/mcp_connect.py` so the discovered server tools actually load.
- Confirmed the utilities config matches the expectations of `MCPDiscovery` and `MCPConnector`.
- Added `google-adk` to the project environment for the utilities-side connector work.
- Added `uvicorn` to the project dependencies so the website builder agent entrypoint can run.
- Updated the website builder agent executor and entrypoint to match the current A2A SDK API.
- Verified that `uv run python -m agents.website_builder_simple --help` works successfully.

## Next Steps
- Implement the app frontend shown in the diagram.
- Add the host agent / orchestrator layer.
- Add the agent registry and task delegation flow.
- Connect remote A2A agents into the orchestration path.
- Continue testing both MCP servers from Claude Desktop.
- Continue the website builder tutorial flow with the current SDK if new compatibility issues appear.
- Continue following the tutorial while extending the utilities-side Google ADK connector.


## GitHub Push Log
- Date: 2026-07-16
- Commit: Initial commit
- Branch: master
- Pushed: Yes
- Notes: Initial repository push completed successfully before the documentation refresh.
