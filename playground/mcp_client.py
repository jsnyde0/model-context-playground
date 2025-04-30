import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
import mcp.types as types


async def main():
    print("Starting MCP client...")
    async with sse_client("http://127.0.0.1:8050/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result: types.ListToolsResult = await session.list_tools()
            tool_names = [tool.name for tool in tools_result.tools]
            print(f"tool_names: {tool_names}")

            result: types.CallToolResult = await session.call_tool(
                "add", {"a": 15, "b": 7}
            )
            print(f"result: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
