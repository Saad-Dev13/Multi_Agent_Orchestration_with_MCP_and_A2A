import asyncio

from utilities.mcp.mcp_discovery import MCPDiscovery
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

from mcp import StdioServerParameters

class MCPConnector:
    """
    Discovers the MCP servers from the config
    Config will be loaded by the MCP Dicovery class.

    Then it lists each server's tools
    and then caches them as MCPToolsets that are compatible with Google's Agent Development Kit

    """

    def __init__(self, config_file: str = None):
        self.discovery = MCPDiscovery(config_file)
        self.tools: list[MCPToolset] = []
        
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # If the event loop is already running, we defer loading the tools
            # to the async `get_tools` method to avoid RuntimeError.
            pass
        else:
            self.tools = asyncio.run(self._load_all_tools())
    
    async def _load_all_tools(self):
        """
        Loads all tools from the discovered MCP servers and caches them as MCPToolsets.

        Raises:
            ValueError: If the server definition is invalid or if the tool list cannot be retrieved.
        """
        tools = []

        for name, server in self.discovery.list_servers().items():
            try:
                if not isinstance(server, dict):
                    raise ValueError(f"Server '{name}' must be a dictionary.")

                if server.get("command") == "streamable_http":
                    args = server.get("args", [])
                    if not args:
                        raise ValueError(f"Server '{name}' is missing the streamable HTTP URL in args.")

                    conn = StreamableHTTPServerParams(
                        url=args[0],
                    )

                else:
                    conn = StdioConnectionParams(
                        server_params=StdioServerParameters(
                            command=server["command"],
                            args=server["args"],
                        ),

                        timeout=5
                    )

                toolset = MCPToolset(connection_params=conn)

                tools_list = await toolset.get_tools()
                tool_names = [tool.name for tool in tools_list]
                print(f"[bold green]Loaded tools from server [cyan]'{name}'[/cyan]:[bold green] {', '.join(tool_names)}")

                tools.append(toolset)
            except Exception as e:
                print(f"[bold red]Error loading tools from server (skipping) '{name}': {str(e)} [/bold red]")
        
        return tools


    async def get_tools(self) -> list[MCPToolset]:
        """
        Returns the list of cached MCPToolsets.

        Returns:
            list[MCPToolset]: The list of cached MCPToolsets.
        """
        await self._load_all_tools()
        return self.tools.copy()
