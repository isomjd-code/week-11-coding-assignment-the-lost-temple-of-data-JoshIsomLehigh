import subprocess 
import re

# Test 1: Check for unhandled pylint errors
def test_pylint_errors():
    result = subprocess.run(['pylint', 'adventure.py'], capture_output=True, text=True)
    assert "E0" not in result.stdout, "Pylint errors found"
