from langchain_mcp_adapters.client import MultiServerMCPClient


class MCPService:
    """
    Singleton wrapper around the MCP client.
    """

    def __init__(self):
        self.client = MultiServerMCPClient(
            {
                "security": {
                    "transport": "stdio",
                    "command": "python",
                    "args": ["-m", "security_mcp.server"],
                }
            }
        )

        self._tools = None

    async def get_tools(self):
        """
        Connect to the MCP server and return all available tools.
        """
        if self._tools is None:
            self._tools = await self.client.get_tools()

        return self._tools


mcp_service = MCPService()