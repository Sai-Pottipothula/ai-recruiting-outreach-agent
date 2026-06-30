from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class CandidateMCPClient:
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "src.mcp.server"],
        )

        # Start the stdio transport
        read, write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        # Create MCP session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )

        # Perform MCP handshake
        await self.session.initialize()

        print("✅ Connected to MCP Server")

    async def list_tools(self):
        return await self.session.list_tools()

    async def call_tool(self, tool_name: str, arguments: dict):
        return await self.session.call_tool(tool_name, arguments)

    async def close(self):
        await self.exit_stack.aclose()
