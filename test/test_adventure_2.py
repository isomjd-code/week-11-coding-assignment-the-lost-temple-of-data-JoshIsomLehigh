import subprocess
import re

# Test 2: Check for unhandled pylint warnings
def test_pylint_warnings():
    result = subprocess.run(['pylint', 'adventure.py'], capture_output=True, text=True)
    assert "W0" not in result.stdout, "Pylint warnings found"
