# Fixes Log

This log documents all issues identified and resolved during the development of the Multi-Agent Orchestration system.

---

## Remaining Maintenance & Verification
- **Testing**: Run regular checks on external MCP connections.
- **Rate-Limiting**: Monitor Gemini API quota usage and implement client-side retries if free tier limits are hit.

---

## Completed Fixes

### 1. Model Name and Quota Resolution
- **Date**: 2026-07-16
- **File**: [agents/host_agent/agent.py](agents/host_agent/agent.py)
- **Problem**: Running the agent resulted in `404 NOT_FOUND` for the `gemini-2.5-flash` and `gemini-3.5-flash` models.
- **Why it was needed**: Those model identifiers are deprecated or invalid. The current stable model is `gemini-2.0-flash`.
- **How it was fixed**: Changed the model definition to `gemini-2.0-flash`.
- **Result**: Host Agent queries execute correctly.

- **Date**: 2026-07-16
- **File**: [agents/host_agent/agent.py](agents/host_agent/agent.py)
- **Problem**: When hitting a `429 RESOURCE_EXHAUSTED` rate limit, the final agent response returned as an empty string.
- **Why it was needed**: The client yielded empty strings on failed ADK execution instead of surfacing the error details.
- **How it was fixed**: Updated `invoke()` to extract `error_code` and `error_message` from the final response event and surface it.
- **Result**: Rate limit and API quota errors are gracefully printed in the terminal.

---

### 2. A2A Communication and SDK Updates
- **Date**: 2026-07-16
- **File**: [utilities/a2a/agent_connect.py](utilities/a2a/agent_connect.py)
- **Problem**: Calling `send_message` returned `object async_generator can't be used in 'await' expression`.
- **Why it was needed**: `send_message` is an async generator (utilizing `yield`). Calling it returns an `async_generator` object synchronously, so it should not be awaited directly.
- **How it was fixed**: Removed the `await` keyword from `a2a_client.send_message(...)` and consumed the stream using `async for`.
- **Result**: Streaming responses parse correctly.

- **Date**: 2026-07-16
- **File**: [utilities/a2a/agent_connect.py](utilities/a2a/agent_connect.py)
- **Problem**: Missing await on client instantiation returned a coroutine.
- **Why it was needed**: `create_client` is defined with `async def` and must be awaited to resolve to the client instance.
- **How it was fixed**: Added `await` to `create_client(...)`.
- **Result**: Connection establishes successfully.

- **Date**: 2026-07-16
- **File**: [utilities/a2a/agent_connect.py](utilities/a2a/agent_connect.py)
- **Problem**: Client returned "No response from agent" on all requests.
- **Why it was needed**: The updated SDK sends completion content wrapped inside a `status_update` event payload rather than direct `message` fields.
- **How it was fixed**: Added parsing for `status_update` event states and extracted completed text content.
- **Result**: Stream content resolves and displays successfully.

---

### 3. Service Lifecycle and Startup Automation
- **Date**: 2026-07-17
- **File**: [scripts/start_all.ps1](scripts/start_all.ps1)
- **Problem**: Running multiple agents, MCP servers, and terminal clients required manual startup of 4 separate windows.
- **Why it was needed**: A unified startup was required to prevent race conditions (e.g. CLI client starting before servers are fully bound to ports).
- **How it was fixed**: Created a master PowerShell script `start_all.ps1` that starts each service in a new window and uses TCP socket polling to wait until the port is open before launching the next.
- **Result**: Clean, automated system startup.

- **Date**: 2026-07-16
- **File**: [agents/host_agent/__main__.py](agents/host_agent/__main__.py)
- **Problem**: Host agent exited immediately right after launching the FastAPI/Uvicorn server.
- **Why it was needed**: `asyncclick` was wrapping the main function with `anyio.run` but Uvicorn was starting its own event loop, causing immediate socket cancellations.
- **How it was fixed**: Switched to synchronous `click` and wrapped the server startup in `asyncio.run(serve())` within the callback.
- **Result**: Host agent server runs stably on port 10001.

- **Date**: 2026-07-16
- **File**: [app/cmd/cmd.py](app/cmd/cmd.py)
- **Problem**: CLI client failed with `ModuleNotFoundError: No module named 'asyncclick'` and loop conflict warnings.
- **Why it was needed**: Legacy command line wrapper loop conflicts.
- **How it was fixed**: Replaced `asyncclick` with standard `click` and executed the main loop inside a synchronous callback using `asyncio.run()`.
- **Result**: CLI starts cleanly and prompts for user commands.

---

### 4. Codebase Typos and Pathing
- **Date**: 2026-07-16
- **File**: [utilities/common/file_loader.py](utilities/common/file_loader.py)
- **Problem**: Host agent couldn't locate `instructions.txt` or `description.txt`.
- **Why it was needed**: File loader resolved paths relative to its own subdirectory instead of the project root.
- **How it was fixed**: Configured the loader base path to search relative to the repository root.
- **Result**: Text assets resolve and load cleanly.

- **Date**: 2026-07-16
- **File**: [agents/host_agent/agent_executor.py](agents/host_agent/agent_executor.py)
- **Problem**: `ImportError` on `HostAgentExecutor`.
- **Why it was needed**: Copy-paste class name typo in `agent_executor.py`.
- **How it was fixed**: Renamed class definition to `HostAgentExecutor`.
- **Result**: Module runs correctly.

- **Date**: 2026-07-16
- **File**: [utilities/a2a/agent_registry.json](utilities/a2a/agent_registry.json)
- **Problem**: Host agent registry not found error.
- **Why it was needed**: The file was saved as `agent_registry.josn`.
- **How it was fixed**: Renamed file extension to `.json`.
- **Result**: Registry loads on startup.

---

### 5. Git Security
- **Date**: 2026-07-17
- **File**: [.gitignore](.gitignore)
- **Problem**: Sensitive API keys and keys in `.env` could be pushed to GitHub accidentally.
- **Why it was needed**: The `.gitignore` file did not contain rule declarations for `.env` files.
- **How it was fixed**: Appended `.env`, `*.local`, and standard secret file patterns to `.gitignore`.
- **Result**: Credentials and local variables are excluded from git.
