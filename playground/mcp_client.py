import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
import mcp.types as types

from playground.agent import Agent


def convert_mcp_tool_to_openrouter_format(mcp_tool: types.Tool) -> dict:
    """Converts an MCP Tool definition into the OpenRouter function calling format."""
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.inputSchema,
        },
    }


async def main():
    agent = Agent()

    print("Starting MCP client...")
    try:
        async with sse_client("http://127.0.0.1:8050/sse") as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                raw_mcp_tools: types.ListToolsResult = await session.list_tools()
                tool_names = [tool.name for tool in raw_mcp_tools.tools]
                print(f"tool_names: {tool_names}")

                # Convert MCP tools to OpenRouter format
                mcp_tools = [
                    convert_mcp_tool_to_openrouter_format(tool)
                    for tool in raw_mcp_tools.tools
                ]

                # Example: Pass these tools to your LLM
                response = await agent.prompt_llm(
                    "What is 15 plus 7?", tools=mcp_tools
                )  # TODO: check why seems we have no response? debug?
                print(f"LLM response (potentially with tool call):\n{response}")

                # Keep the direct tool call example for now
                print("\nCalling 'add' tool directly via MCP:")
                tool_result: types.CallToolResult = await session.call_tool(
                    "add", {"a": 15, "b": 7}
                )
                print(f"Direct tool_result: {tool_result.content[0].text}")

    # Handle specific connection refusal error
    except ConnectionRefusedError:
        print(
            "\nError: Connection refused. Could not connect to the MCP server at http://127.0.0.1:8050/sse"
        )
        print("Please ensure the MCP server (playground/mcp_server.py) is running.")

    # Handle any other exception during connection/initialization
    except Exception as e:
        print(f"\nAn error occurred while connecting to the MCP server: {e}")
        print(
            "Please ensure the MCP server (playground/mcp_server.py) is running and accessible."
        )


if __name__ == "__main__":
    asyncio.run(main())
