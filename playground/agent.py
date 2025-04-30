import json
import requests
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# You can use any model that supports tool calling
MODEL = "google/gemini-2.0-flash-exp:free"

llm_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


async def prompt_llm(llm_client: AsyncOpenAI, user_input: str) -> str:
    """Placeholder for processing user input."""

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": user_input,
        },
    ]

    response = await llm_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        # tools=tools,
        tool_choice="auto",
    )

    return response.choices[0].message.content


async def run_agent_loop():
    """Runs the main interaction loop for the agent."""
    print("Math Wizard Agent initialized. Ask me to add numbers!")
    print("(Type 'quit' to exit)")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                print("Wizard: Goodbye!")
                break

            response = await prompt_llm(llm_client, user_input)
            print(f"Wizard: {response}")

        except EOFError:  # Handle Ctrl+D
            print("\nWizard: Goodbye!")
            break
        except KeyboardInterrupt:  # Handle Ctrl+C
            print("\nWizard: Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(run_agent_loop())
