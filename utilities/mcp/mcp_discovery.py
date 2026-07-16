
import json
import os
from typing import Any, Dict

class MCPDiscovery:
    """
    Reads a JSON file defining MCP servers and provide access to 
    the server definitions under the mcpServers key.


    Attributes:
        config_file (str): The path to the JSON configuration file.
        config (Dict[str, Any]): Parsed JSON content, expected to contain the mcpServers key.
    """

    def __init__(self, config_file: str = None):
        """
        Initializes the MCPDiscovery instance by loading the JSON configuration file.

        Args:
            config_file (str, optional): The path to the JSON configuration file. 
            If None, defaults to 'mcp_config.json' in the same directory as this script/Module.
        
        """
        if config_file is None:
            self.config_file = os.path.join(
                os.path.dirname(__file__), 'mcp_config.json')
        else:
            self.config_file = config_file
        
        self.config = self._load_config()


    def _load_config(self) -> Dict[str, Any]:
        """
        Loads and parses the JSON configuration file.

        Returns:
            Dict[str, Any]: Parsed JSON content.

        """
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)

            if not isinstance(data, dict) or 'mcpServers' not in data:
                raise ValueError(
                    f"Invalid configuration format in {self.config_file}. Expected a dictionary with an 'mcpServers' key.")
            
            return data
    
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file {self.config_file} not found.")
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Error parsing JSON from {self.config_file}: {str(e)}")
        except ValueError as e:
            raise ValueError(str(e))
        

    def list_servers(self) -> Dict[str, Any]:
        """
        Returns the list of MCP servers defined in the configuration.

        Returns:
            Dict[str, Any]: The mcpServers dictionary from the configuration.

        Raises:
            ValueError: If the configuration is invalid or does not contain the mcpServers key.
        """
        if 'mcpServers' not in self.config:
            raise ValueError(
                f"Configuration does not contain 'mcpServers' key.")
        
        return self.config.get('mcpServers', {})