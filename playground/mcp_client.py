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
            async with ClientSession(read, write) as mcp_session:
                await mcp_session.initialize()

                # Example: Pass these tools to your LLM
                response = await agent.prompt(
                    "What is 15 plus 7?", mcp_session=mcp_session
                )
                print(f"LLM response (potentially with tool call):\n{response}")

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
