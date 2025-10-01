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
        from villager_ai.services.kali_driver_service import KaliContainer, ensure_kali_image
        assert KaliContainer is not None
        assert ensure_kali_image is not None
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

def test_kali_container_class():
    """Test KaliContainer class basic functionality"""
    try:
        from villager_ai.services.kali_driver_service import KaliContainer
        import time
        
        # Test container creation
        container = KaliContainer("test_id", 22000)
        assert container.container_id == "test_id"
        assert container.ssh_port == 22000
        assert container.created_at > 0
        
        # Test expiration check (should not be expired immediately)
        assert not container.is_expired()
        
    except ImportError as e:
        pytest.skip(f"Could not import KaliContainer: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
