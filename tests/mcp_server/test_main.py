import pytest

# Import the function we want to test
from model_context_playground.mcp_server import add


def test_add_positive_integers():
    """Test adding two positive integers."""
    assert add(5, 3) == 8
    assert add(100, 200) == 300

def test_add_negative_integers():
    """Test adding two negative integers."""
    assert add(-5, -3) == -8
    assert add(-100, -200) == -300

def test_add_mixed_sign_integers():
    """Test adding integers with different signs."""
    assert add(5, -3) == 2
    assert add(-5, 3) == -2
    assert add(10, -10) == 0

def test_add_zero():
    """Test adding with zero."""
    assert add(5, 0) == 5
    assert add(0, 5) == 5
    assert add(-5, 0) == -5
    assert add(0, -5) == -5
    assert add(0, 0) == 0

# Note: We are not explicitly testing non-integer types here.
# The FastMCP framework, leveraging Pydantic/type hints, is expected
# to handle type validation *before* calling the `add` function.
# If invalid types were passed by a client, FastMCP should raise an error.
# Our unit test focuses on the logic within the `add` function itself,
# assuming valid integer inputs based on the type hints. 