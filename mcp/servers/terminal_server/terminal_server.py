from mcp.server.fastmcp import FastMCP
import os
import subprocess


mcp = FastMCP("terminal_server")
# Fixed: Set the default workspace to a folder on the desktop, rathern than the root of the C drive, to avoid permission issues.
# Fixed: Use os.path.join to construct the path if it does not exist, and create the folder if it does not exist.
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
if not os.path.isdir(DESKTOP_PATH):
    DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

DEFAULT_WORKSPACE = os.path.join(DESKTOP_PATH, "Test_folder")
os.makedirs(DEFAULT_WORKSPACE, exist_ok=True)


#Fixed: use @mcp.tool() decorator to register the function as a tool in the MCP server instead of mcp,tool(terminal_server)
@mcp.tool()
async def run_command(command:str) -> str:
    """
    Run a command in the terminal and return the output.

    Args:
        command (str): The command to run.
        
    Returns:
        str: The output of the command or an error message if the command fails.
    """
    try:
        result = subprocess.run(command, shell=True, cwd=DEFAULT_WORKSPACE, text=True, capture_output=True)
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error running command '{command}' : {str(e)}"
    

if __name__ == "__main__":
    mcp.run(transport="stdio")

    