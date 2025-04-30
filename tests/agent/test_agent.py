import pytest

def test_agent_module_import():
    """Test that the agent module can be imported."""
    try:
        import playground.agent
    except ImportError as e:
        pytest.fail(f"Failed to import playground.agent: {e}")

def test_process_request_placeholder():
    """Test the placeholder response of process_request."""
    # Import locally to avoid issues if module fails to import globally
    from playground.agent import process_request
    test_input = "hello world"
    expected_output = f"Placeholder response for: {test_input}"
    assert process_request(test_input) == expected_output 