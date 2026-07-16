# Fixes Log

Use this file to record every fix made in the project.

## Entry Template
- Date:
- File:
- Lines:
- Problem:
- Why it was needed:
- How it was fixed:
- Result:

## Remaining Fixes
- Restart Claude Desktop and verify the MCP server reconnects successfully.
- Test the `run_command` tool from Claude with a simple command such as `echo hello`.
- Confirm whether the server should keep using `Desktop\Test_folder` or switch to a different workspace folder later.
- Confirm that the arithmetic connector appears in Claude Desktop after restarting with the updated `npx -y mcp-remote` config.
- Verify the arithmetic server remains reachable at `http://localhost:3000/mcp/` before connector startup.
- Implement the frontend, host agent, agent registry, and remote A2A layers that are still planned in the architecture.

## Completed Fixes
- Date: 2026-07-16
	File: [mcp/servers/terminal_server/terminal_server.py](mcp/servers/terminal_server/terminal_server.py)
	Lines: 6-19
	Problem: The MCP tool file included a stray `mcp.tool("terminal_server")` line and the default working directory pointed to a non-existent folder, which caused WinError 267 in Claude Desktop.
	Why it was needed: The server could not reliably start command execution without a valid working directory, and the extra line was not a valid tool registration pattern.
	How it was fixed: Removed the stray line, kept `@mcp.tool()` as the tool decorator, created the default workspace automatically, and changed the default workspace to a `Test_folder` on the Desktop.
	Result: The MCP server file now validates cleanly and should have a stable working directory when started.
- Date: 2026-07-16
	File: [mcp/servers/streamable_http_server.py](mcp/servers/streamable_http_server.py)
	Lines: 1-35
	Problem: The arithmetic MCP service needed to be confirmed as a valid streamable HTTP server for Claude Desktop remote connector testing.
	Why it was needed: Claude Desktop can only show the connector if the server starts successfully and exposes a reachable HTTP endpoint.
	How it was fixed: Defined the arithmetic server with `FastMCP(..., host="localhost", port=3000, stateless_http=True)` and launched it with `mcp.run(transport="streamable-http")`.
	Result: The arithmetic server starts successfully on `http://localhost:3000` and is ready for MCP remote connection.
- Date: 2026-07-16
	File: [README.md](README.md)
	Lines: 1-220
	Problem: The README still referenced the diagram indirectly and depended on the image to explain the intended architecture.
	Why it was needed: The documentation needed to stand on its own so readers could understand the project without seeing the diagram.
	How it was fixed: Rewrote the README around the layered A2A/MCP architecture and added a self-contained Mermaid flowchart.
	Result: The README now explains the system independently of the image and matches the current project direction.
- Date: 2026-07-16
	File: [PROJECT_STATUS.md](PROJECT_STATUS.md)
	Lines: 1-220
	Problem: The status file still described the work in a diagram-dependent way.
	Why it was needed: The project status should match the same self-contained architecture description used in the README.
	How it was fixed: Updated the status file to separate implemented slices from future architecture layers.
	Result: The project status now reflects the current implementation boundaries and planned next layers.
