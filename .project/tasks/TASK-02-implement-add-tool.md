# Task: Implement MCP 'add' Tool

- **Unique Task ID:** TASK-02-implement-add-tool
- **Description:** Implement the 'add' tool within the MCP server (`playground/mcp_server.py`) using the `@mcp.tool()` decorator provided by the SDK. This tool should accept two numbers and return their sum, fulfilling requirements 1.2, 1.3, and 1.4 from the specification. Include basic error handling for non-numeric input (Req 1.5).
- **Relevant Specification:** [.project/specs/SPEC-01-simple-math-agent-mcp.md](.project/specs/SPEC-01-simple-math-agent-mcp.md) (Specifically Requirements 1.2, 1.3, 1.4, 1.5)
- **Acceptance Criteria:**
    - An `add` function decorated with `@mcp.tool()` exists in `playground/mcp_server.py`.
    - The function accepts two arguments (e.g., `a: int`, `b: int` or similar, type hints are recommended).
    - The function correctly returns the sum of the two arguments when they are numeric.
    - The function raises an appropriate exception (e.g., `TypeError` or `ValueError`) or returns an error indicator if non-numeric input is provided.
    - The tool is discoverable when running the server (verifiable via `mcp dev` inspector or later via client code).
    - Integration tests successfully connect to the server, call the 'add' tool via MCP, and verify the result.
    - Integration tests verify that calling the 'add' tool with incorrect types via MCP results in a protocol-level error.
- **Tests:**
    - Unit tests for the `add` function:
        - Test with various integer and float inputs (positive, negative, zero).
        - Test with non-numeric inputs to verify error handling.
    - Integration tests (`tests/mcp_server/test_integration.py` - note: test file path remains nested):
        - Start the MCP server process.
        - Connect using an MCP client (e.g., `stdio_client`).
        - Verify 'add' tool is listed via `list_tools`.
        - Call 'add' tool with valid integer arguments and assert correct sum.
        - Call 'add' tool with invalid type arguments and assert appropriate MCP error is raised by the client session.
- **Metadata:**
    - **ID:** TASK-02-implement-add-tool
    - **Start Date:** 2024-07-26
    - **End Date:** 2024-07-29
    - **State:** closed
    - **Estimated Lines of Code:** ~40-60 (including unit and integration tests)
- **Complexity:** Low
- **Learnings:** 
   - Defined an MCP tool using the `@mcp.tool()` decorator on a standard Python function (`add`).
   - Used type hints (`a: int, b: int`) which `FastMCP` leverages for automatic input validation before the tool function is called.
   - Added unit tests (`tests/mcp_server/test_main.py`) using `pytest` to verify the core logic of the `add` function in isolation.
   - Added integration tests (`tests/mcp_server/test_integration.py`) using `pytest-asyncio`.
   - Integration tests start the server as a subprocess (`StdioServerParameters`, `stdio_client`).
   - Used `ClientSession` to interact with the running server via the MCP protocol.
   - `session.list_tools()` returns a `ListToolsResult` object; the actual tools list is in the `.tools` attribute.
   - `session.call_tool()` returns a `CallToolResult` object, not the raw value. Successful results are in `.content` (often `[TextContent(...)]`), and errors are indicated by `.isError = True`.
   - SDK/`FastMCP` handles type/argument validation errors at the protocol level, resulting in `CallToolResult` with `isError=True` rather than client-side Python exceptions for invalid calls.
   - Debugged integration tests by inspecting return types (`ListToolsResult`, `CallToolResult`) and adjusting assertions accordingly. 