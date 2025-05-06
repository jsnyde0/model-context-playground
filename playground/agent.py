import json
from openai import AsyncOpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from dotenv import load_dotenv
import os
import asyncio
from typing import Any
import mcp.types as types
from mcp.client.session import ClientSession

from playground.mcp_server import add

load_dotenv()

add_tool_schema = {
    "type": "function",
    "function": {
        "name": "add",
        "description": "Add two numbers together",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "First number"},
                "b": {"type": "integer", "description": "Second number"},
            },
            "required": ["a", "b"],
        },
    },
}

TOOL_MAPPING = {
    "add": add,
}


class Agent:
    def __init__(self):
        self.llm_client = self._create_llm_client()
        self.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Use tools when appropriate.",
            },
        ]

    def run(self):
        print("Agent initialized. Ask me to add numbers!")
        print("(Type 'quit' to exit)")

    def _create_llm_client(self) -> AsyncOpenAI:
        """Creates and returns an asynchronous OpenAI client."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable not set."
                "Please set it before running the script."
            )

        return AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def _convert_mcp_tool_to_openrouter_format(self, mcp_tool: types.Tool) -> dict:
        """Converts an MCP Tool definition into the OpenRouter function calling format."""
        return {
            "type": "function",
            "function": {
                "name": mcp_tool.name,
                "description": mcp_tool.description,
                "parameters": mcp_tool.inputSchema,
            },
        }

    async def _prompt_llm(
        self, tools: list[dict] | None = None
    ) -> ChatCompletionMessage:
        """Sends a prompt to the LLM and processes the response into a simple dictionary."""

        # Prepare arguments for the API call
        api_args = {
            "model": "openai/gpt-4o-mini",
            "messages": self.messages,
        }
        if tools:  # Only add tools argument if provided
            api_args["tools"] = tools
            api_args["tool_choice"] = "auto"

        # Make the API call
        response = await self.llm_client.chat.completions.create(**api_args)
        message = response.choices[0].message

        return message

    async def _execute_tool(self, tool_call: ChatCompletionMessageToolCall) -> Any:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        tool_output = TOOL_MAPPING[tool_name](**tool_args)
        return tool_output

    async def _execute_mcp_tool(
        self, mcp_session: ClientSession, tool_call: ChatCompletionMessageToolCall
    ) -> types.CallToolResult:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        tool_result: types.CallToolResult = await mcp_session.call_tool(
            tool_name, tool_args
        )
        return tool_result

    async def prompt(
        self,
        user_input: str,
        mcp_session: ClientSession | None = None,
    ) -> Any:
        """Prompt the agent, which in turn might prompt an LLM or call a tool or both."""
        self.messages.append({"role": "user", "content": user_input})

        if mcp_session:
            raw_mcp_tools: types.ListToolsResult = await mcp_session.list_tools()
            mcp_tools = [
                self._convert_mcp_tool_to_openrouter_format(tool)
                for tool in raw_mcp_tools.tools
            ]

        while True:
            # call the LLM
            try:
                llm_completion_message: ChatCompletionMessage = await self._prompt_llm(
                    tools=mcp_tools
                )
            except Exception as e:
                print(f"Error: {e}")
                return "Sorry, I encountered an error trying to process that."

            # extend the message history with the LLM's response
            self.messages.append(llm_completion_message.model_dump())

            # if the LLM called a tool, execute it and extend the message history
            if llm_completion_message.tool_calls:
                tool_call = llm_completion_message.tool_calls[0]
                tool_result: types.CallToolResult = await self._execute_mcp_tool(
                    mcp_session, tool_call
                )
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": tool_result.content[0].text,
                    }
                )

            elif llm_completion_message.content:
                return llm_completion_message.content
            else:
                print(
                    "No tool call or text content in the response, or LLM call failed."
                )
                return None


async def chat_with_agent():
    """Runs the main interaction loop for the agent."""
    print("Math Wizard Agent initialized. Ask me to add numbers!")
    print("(Type 'quit' to exit)")

    agent = Agent()

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                print("Wizard: Goodbye!")
                break

            response = await agent.prompt(user_input, tools=[add_tool_schema])
            print(f"Wizard: {response}")

        except EOFError:  # Handle Ctrl+D
            print("\nWizard: Goodbye!")
            break
        except KeyboardInterrupt:  # Handle Ctrl+C
            print("\nWizard: Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(chat_with_agent())
