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
- Continue extending the utilities-side Google ADK connector flow if the tutorial introduces more validation or caching logic.
- Continue following the website builder agent tutorial with the current A2A SDK if more import or route updates appear.

## Files to be checked from original status
- Date: 2026-07-16 file_loader.py in utilities/common

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
- Date: 2026-07-16
	File: [utilities/mcp/mcp_config.json](utilities/mcp/mcp_config.json)
	Lines: 1-18
	Problem: The standalone utilities config still contained Claude Desktop-only fields and a connector command that did not match the utilities-side loader.
	Why it was needed: The utilities folder needs a clean config format that the local discovery and connector code can read directly.
	How it was fixed: Removed the Claude Desktop-specific metadata and normalized the arithmetic server entry to the custom `streamable_http` marker used by `MCPConnector`.
	Result: The standalone config now matches the expectations of the utilities-side discovery and connector path.
- Date: 2026-07-16
	File: [utilities/mcp/mcp_connect.py](utilities/mcp/mcp_connect.py)
	Lines: 1-65
	Problem: The connector created an async loader but did not await it, and server iteration did not handle each entry independently.
	Why it was needed: Without awaiting the loader, no toolsets would be cached, and one bad server entry could interfere with the rest.
	How it was fixed: Added a minimal startup load with `asyncio.run(...)`, iterated over `list_servers().items()`, and kept per-server exception handling.
	Result: The utilities connector now loads the discovered server toolsets while staying close to the tutorial flow.
- Date: 2026-07-16
	File: [pyproject.toml](pyproject.toml)
	Lines: 1-8
	Problem: The website builder agent entrypoint imported `uvicorn`, but the project manifest did not declare it.
	Why it was needed: `uv run` needs the dependency in the project environment, otherwise the module fails before the agent starts.
	How it was fixed: Added `uvicorn` to the project dependencies and synced the environment.
	Result: The website builder agent entrypoint now imports cleanly under the project environment.
- Date: 2026-07-16
	File: [agents/website_builder_simple/agent_executor.py](agents/website_builder_simple/agent_executor.py)
	Lines: 1-70
	Problem: The executor used older A2A helper imports and the older task/message creation pattern.
	Why it was needed: The installed A2A SDK had moved those helpers, so the original imports no longer worked.
	How it was fixed: Switched to `a2a.helpers.proto_helpers`, used the current `TaskState.TASK_STATE_*` names, and kept the same task update flow.
	Result: The executor now runs with the current A2A helper API while preserving the tutorial behavior.
- Date: 2026-07-16
	File: [agents/website_builder_simple/__main__.py](agents/website_builder_simple/__main__.py)
	Lines: 1-60
	Problem: The entrypoint used the removed `A2AStarletteApplication` bootstrap.
	Why it was needed: The current A2A SDK exposes route helpers mounted on FastAPI instead of the old app wrapper.
	How it was fixed: Replaced the old wrapper with `FastAPI()` plus `add_a2a_routes_to_fastapi(...)`.
	Result: The agent module now starts correctly with the current SDK and exposes CLI help under `uv run python -m agents.website_builder_simple`.
- Date: 2026-07-16
	File: [agents/website_builder_simple/__main__.py](agents/website_builder_simple/__main__.py), [agents/website_builder_simple/agent.py](agents/website_builder_simple/agent.py)
	Lines: multiple
	Problem: Running the agent module failed due to multiple API changes in the newer version of the `a2a-sdk` and `google-adk` libraries. First, `ValueError: Protocol message AgentCard has no "url" field.` (and camelCase fields for modes failed). Second, `pydantic_core._pydantic_core.ValidationError: 1 validation error for LlmAgent instructions Extra inputs are not permitted`. Third, `TypeError: DefaultRequestHandlerV2.__init__() missing 1 required positional argument: 'agent_card'`.
	Why it was needed: The agent codebase was outdated compared to the active versions of both SDKs, preventing the FastAPI server from instantiating or starting.
	How it was fixed:
		1. Imported `AgentInterface` and updated the `AgentCard` instantiation to declare the URL under `supported_interfaces` (using `JSONRPC` protocol binding). Also updated `defaultInputModes` and `defaultOutputModes` constructor arguments to their snake_case equivalents (`default_input_modes` and `default_output_modes`).
		2. Updated `LlmAgent` construction in `agent.py` to use `instruction=self.system_instruction` instead of `instructions=`.
		3. Added `agent_card=agent_card` parameter to `DefaultRequestHandler` call in `__main__.py`.
	Result: The agent server starts successfully on `http://localhost:10000` with the updated A2A and ADK library APIs.
- Date: 2026-07-16
	File: [agents/website_builder_simple/agent.py](agents/website_builder_simple/agent.py)
	Lines: 75
	Problem: The google-genai SDK's `types.Part.from_text` method requires the `text` argument to be passed by keyword name (keyword-only parameter), but it was passed positionally, causing `Expected argument text to be passed by name`.
	Why it was needed: Running the agent to process queries failed immediately with a TypeError/ValueError due to the positional argument call pattern.
	How it was fixed: Modified the invocation at line 75 to pass `text=query` instead of `query`.
	Result: The agent correctly runs queries and uses the Google GenAI SDK to generate content.
