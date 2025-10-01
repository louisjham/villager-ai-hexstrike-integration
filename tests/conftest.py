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
def mock_docker():
    """Mock Docker for testing"""
    # This would be used to mock Docker calls in tests
    # For now, just return a simple mock
    class MockDocker:
        def images(self, image_name):
            class MockResult:
                stdout = f"kalilinux/kali-rolling"
                returncode = 0
            return MockResult()
        
        def pull(self, image_name):
            class MockResult:
                returncode = 0
            return MockResult()
    
    return MockDocker()

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
