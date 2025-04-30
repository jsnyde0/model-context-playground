# tests/mcp_server/test_integration.py
import pytest
import sys
import asyncio  # <-- Import asyncio
import playground  # Import our package
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
import mcp.types as types

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio


# Request the mcp_server_process fixture explicitly
async def test_server_lists_add_tool(mcp_server_process):
    """Verify the server lists the 'add' tool via MCP."""
    await asyncio.sleep(0.5)  # <-- Add small delay for server startup
    async with sse_client("http://127.0.0.1:8050/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result: types.ListToolsResult = await session.list_tools()
            # print(f"list_tools result: {tools_result!r}") # No longer needed
            # Access the .tools attribute which contains the list
            assert isinstance(tools_result.tools, list)
            tool_names = [tool.name for tool in tools_result.tools]
            assert "add" in tool_names
            # Remove the try/except block as we now know the structure


# Request the mcp_server_process fixture explicitly
async def test_server_call_add_tool_success(mcp_server_process):
    """Test calling the 'add' tool with valid arguments via MCP."""
    await asyncio.sleep(0.1)  # <-- Add small delay (can be shorter after first test)
    async with sse_client("http://127.0.0.1:8050/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result: types.CallToolResult = await session.call_tool(
                "add", {"a": 15, "b": 7}
            )
            assert not result.isError
            # Assuming the result is in the first TextContent block
            assert len(result.content) == 1
            assert isinstance(result.content[0], types.TextContent)
            assert result.content[0].text == "22"


# Request the mcp_server_process fixture explicitly
async def test_server_call_add_tool_invalid_type(mcp_server_process):
    """Test calling the 'add' tool with invalid argument types via MCP."""
    await asyncio.sleep(0.1)  # <-- Add small delay
    async with sse_client("http://127.0.0.1:8050/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Expect a CallToolResult indicating an error, not a Python exception
            result: types.CallToolResult = await session.call_tool(
                "add", {"a": "not_a_number", "b": 7}
            )
            assert result.isError
            # Optionally, check the error message content if needed
            # assert "validation error" in result.content[0].text.lower()


# Request the mcp_server_process fixture explicitly
async def test_server_call_add_tool_missing_arg(mcp_server_process):
    """Test calling the 'add' tool with missing arguments via MCP."""
    await asyncio.sleep(0.1)  # <-- Add small delay
    async with sse_client("http://127.0.0.1:8050/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Expect a CallToolResult indicating an error
            result: types.CallToolResult = await session.call_tool(
                "add", {"a": 5}
            )  # Missing 'b'
            assert result.isError
            # Optionally, check the error message content if needed
            # assert "validation error" in result.content[0].text.lower()
