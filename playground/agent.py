import json
import requests
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
from typing import Any

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


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

    def _process_llm_response(self, response: Any) -> dict:
        """Processes the raw response from the LLM API into a simple dictionary."""
        message = response.choices[0].message

        if message.tool_calls:
            # The LLM decided to call one or more tools
            return {"type": "tool_call", "tool_calls": message.tool_calls}
        elif message.content is not None:
            # The LLM provided a text response
            return {"type": "text", "content": message.content}
        else:
            # No tool call and no text content (unusual)
            return {"type": "empty"}

    async def prompt_llm(
        self, user_input: str, tools: list[dict] | None = None
    ) -> dict:
        """Sends a prompt to the LLM and processes the response into a simple dictionary."""

        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

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
        message = response.choices[0].message.dict()
        self.messages.append(message)

        return message


async def run_agent_loop():
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

            response = await agent.prompt_llm(user_input)
            print(f"Wizard: {response}")

        except EOFError:  # Handle Ctrl+D
            print("\nWizard: Goodbye!")
            break
        except KeyboardInterrupt:  # Handle Ctrl+C
            print("\nWizard: Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(run_agent_loop())
