"""
Pytest configuration for Villager AI tests
"""
import pytest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture(scope="session")
def test_environment():
    """Set up test environment"""
    # Set test environment variables
    os.environ['PYTHONPATH'] = os.path.join(os.path.dirname(__file__), '..', 'src')
    return os.environ

@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing"""
    import subprocess
    
    class MockSubprocess:
        def run(self, cmd, **kwargs):
            class MockResult:
                returncode = 0
                stdout = "mock output"
                stderr = ""
            return MockResult()
    
    return MockSubprocess()
