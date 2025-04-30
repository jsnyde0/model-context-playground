"""Basic structure for the Math Wizard Agent."""

def process_request(user_input: str) -> str:
    """Placeholder for processing user input."""
    # In future tasks, this will involve:
    # 1. Understanding the intent (e.g., is it addition?)
    # 2. Extracting arguments (e.g., the numbers)
    # 3. Calling the MCP server's tool
    # 4. Formatting the response
    return f"Placeholder response for: {user_input}"

def run_agent_loop():
    """Runs the main interaction loop for the agent."""
    print("Math Wizard Agent initialized. Ask me to add numbers!")
    print("(Type 'quit' to exit)")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Wizard: Goodbye!")
                break

            response = process_request(user_input)
            print(f"Wizard: {response}")

        except EOFError: # Handle Ctrl+D
            print("\nWizard: Goodbye!")
            break
        except KeyboardInterrupt: # Handle Ctrl+C
            print("\nWizard: Goodbye!")
            break

if __name__ == "__main__":
    run_agent_loop() 