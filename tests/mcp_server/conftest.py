import sys
import pytest
from xprocess import ProcessStarter


@pytest.fixture(scope="session")
def mcp_server_process(xprocess):
    """Fixture to start the MCP server process for integration tests."""

    # Define how to start the server
    class Starter(ProcessStarter):
        # Command to start the server
        # Assumes playground/mcp_server.py is runnable as a module
        # Use sys.executable to ensure the correct python interpreter is used
        # (especially important when using virtual environments)
        # Corrected pattern to match Uvicorn's startup message
        pattern = "Uvicorn running on"
        args = [sys.executable, "-m", "playground.mcp_server"]

    # Start the process and ensure it's terminated after the session
    xprocess.ensure("mcp_server", Starter)

    # Yield control to the tests - server is running in the background
    yield

    # Teardown: Stop the server process
    print("\n[Fixture] Calling terminate() on MCP server process...")
    xprocess.getinfo("mcp_server").terminate()
    print("[Fixture] terminate() call returned.")
