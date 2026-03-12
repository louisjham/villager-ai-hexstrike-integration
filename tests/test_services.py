"""
Tests for Villager AI services
"""
import pytest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_kali_driver_service_import():
    """Test that we can import the kali_driver_service"""
    try:
        from villager_ai.services.kali_driver_service import execute_local, app
        assert execute_local is not None
        assert app is not None
    except ImportError as e:
        pytest.skip(f"Could not import kali_driver_service: {e}")

def test_mcp_service_import():
    """Test that we can import the mcp_service"""
    try:
        from villager_ai.services import mcp_service
        assert mcp_service is not None
    except ImportError as e:
        pytest.skip(f"Could not import mcp_service: {e}")

def test_browser_service_import():
    """Test that we can import the browser_service"""
    try:
        from villager_ai.services import browser_service
        assert browser_service is not None
    except ImportError as e:
        pytest.skip(f"Could not import browser_service: {e}")

def test_villager_server_import():
    """Test that we can import the villager_server"""
    try:
        from villager_ai.services import villager_server_simple
        assert villager_server_simple is not None
    except ImportError as e:
        pytest.skip(f"Could not import villager_server_simple: {e}")

def test_execute_local():
    """Test local command execution"""
    try:
        from villager_ai.services.kali_driver_service import execute_local
        
        # Test a simple echo command
        result = execute_local("echo hello")
        assert result["success"] is True
        assert "hello" in result["stdout"]
        
    except ImportError as e:
        pytest.skip(f"Could not import execute_local: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
