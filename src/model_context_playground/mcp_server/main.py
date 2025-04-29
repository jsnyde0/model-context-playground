from mcp.server.fastmcp import FastMCP

# Create an MCP server instance named 'MathWizardMCP'
mcp = FastMCP("MathWizardMCP")

# We will add tools (@mcp.tool) here in the next task
@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two integers together.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        The sum of a and b.
    """
    # FastMCP handles type validation based on hints
    # If non-integers are sent, it should raise an error before calling this
    return a + b


# Add the entry point for running the server directly (optional but good practice)
if __name__ == "__main__":
    mcp.run() 