#!/usr/bin/env python3
"""
Villager AI Framework - Comprehensive Test Suite
===============================================

This test file verifies that all components of the Villager framework
are properly connected and working. Run this to ensure your setup is correct.

Usage:
    python3 test_villager_framework.py

Requirements:
    - Villager virtual environment activated
    - Ollama running (if using Ollama provider)
    - Docker running (for containerized tools)
"""

import sys
import os
import time
import subprocess
import requests
from pathlib import Path

# Add Villager to Python path
sys.path.append(str(Path(__file__).parent))

class VillagerFrameworkTester:
    """Comprehensive test suite for Villager AI Framework."""
    
    def __init__(self):
        self.test_results = {}
        self.verbose = True
        
    def log(self, message, status="INFO"):
        """Log test messages with status."""
        if self.verbose:
            status_icons = {
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "WARNING": "⚠️",
                "ERROR": "❌",
                "TEST": "🧪"
            }
            icon = status_icons.get(status, "📝")
            print(f"{icon} {message}")
    
    def test_environment_setup(self):
        """Test 1: Environment and Dependencies"""
        self.log("Testing environment setup...", "TEST")
        
        try:
            # Check Python version
            python_version = sys.version_info
            if python_version >= (3, 8):
                self.log(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}", "SUCCESS")
            else:
                self.log(f"Python version {python_version} is too old. Need 3.8+", "ERROR")
                return False
            
            # Check if we're in virtual environment
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                self.log("Virtual environment detected", "SUCCESS")
            else:
                self.log("Not in virtual environment (recommended but not required)", "WARNING")
            
            # Check required environment variables
            required_vars = ['LLM_PROVIDER']
            optional_vars = ['OLLAMA_BASE_URL', 'OLLAMA_MODEL', 'GITHUB_TOKEN']
            
            for var in required_vars:
                if os.getenv(var):
                    self.log(f"Environment variable {var}: {os.getenv(var)}", "SUCCESS")
                else:
                    self.log(f"Missing required environment variable: {var}", "ERROR")
                    return False
            
            for var in optional_vars:
                if os.getenv(var):
                    self.log(f"Environment variable {var}: {os.getenv(var)}", "SUCCESS")
                else:
                    self.log(f"Optional environment variable {var} not set", "WARNING")
            
            return True
            
        except Exception as e:
            self.log(f"Environment setup test failed: {e}", "ERROR")
            return False
    
    def test_villager_imports(self):
        """Test 2: Villager Core Imports"""
        self.log("Testing Villager core imports...", "TEST")
        
        try:
            # Test core Villager imports
            from scheduler.core.init import global_llm
            from scheduler.core.mcp_client.mcp_client import McpClient
            from scheduler.core.schemas.schemas import TaskModel
            from scheduler.core.tasks.task import TaskNode
            from scheduler.core.tools.common_tool import pyeval, os_execute_cmd
            from scheduler.core.tools.agent_with_tools import tool_villager
            from scheduler.agent_scheduler_manager import agent_scheduler
            from scheduler.toolschain.tools_manager import ToolsManager
            from config import MCP, Master
            from github_tools import GitHubTools
            
            self.log("All Villager core imports successful", "SUCCESS")
            return True
            
        except ImportError as e:
            self.log(f"Villager import failed: {e}", "ERROR")
            return False
        except Exception as e:
            self.log(f"Unexpected error during imports: {e}", "ERROR")
            return False
    
    def test_mcp_server(self):
        """Test 3: MCP Server Functionality"""
        self.log("Testing MCP server functionality...", "TEST")
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location('villager_proper_mcp', 'mcp/villager_proper_mcp.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            VillagerProperMCP = module.VillagerProperMCP
            
            # Initialize MCP server
            villager = VillagerProperMCP()
            self.log("MCP server initialized successfully", "SUCCESS")
            
            # Test system status
            status = villager.get_system_status()
            if status.get('villager_status') == 'running':
                self.log("Villager system status: running", "SUCCESS")
            else:
                self.log(f"Villager system status: {status.get('villager_status')}", "WARNING")
            
            # Test available tools
            tools = villager.list_available_tools()
            if tools:
                self.log(f"Available tools: {len(tools)}", "SUCCESS")
            else:
                self.log("No tools available", "WARNING")
            
            return True
            
        except Exception as e:
            self.log(f"MCP server test failed: {e}", "ERROR")
            return False
    
    def test_llm_provider(self):
        """Test 4: LLM Provider Connection"""
        self.log("Testing LLM provider connection...", "TEST")
        
        try:
            llm_provider = os.getenv('LLM_PROVIDER', 'ollama')
            
            if llm_provider == 'ollama':
                # Test Ollama connection
                ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
                model = os.getenv('OLLAMA_MODEL', 'deepseek-r1-uncensored')
                
                try:
                    response = requests.get(f"{ollama_url}/api/tags", timeout=5)
                    if response.status_code == 200:
                        models = response.json().get('models', [])
                        model_names = [m.get('name', '') for m in models]
                        if any(model in name for name in model_names):
                            self.log(f"Ollama connected, model '{model}' available", "SUCCESS")
                        else:
                            self.log(f"Ollama connected but model '{model}' not found. Available: {model_names}", "WARNING")
                    else:
                        self.log(f"Ollama connection failed: HTTP {response.status_code}", "ERROR")
                        return False
                except requests.exceptions.RequestException as e:
                    self.log(f"Ollama connection failed: {e}", "ERROR")
                    return False
                    
            elif llm_provider == 'deepseek':
                # Test DeepSeek API
                api_key = os.getenv('DEEPSEEK_API_KEY')
                if api_key and api_key != 'your-api-key-here':
                    self.log("DeepSeek API key configured", "SUCCESS")
                else:
                    self.log("DeepSeek API key not configured", "ERROR")
                    return False
                    
            elif llm_provider == 'openai':
                # Test OpenAI API
                api_key = os.getenv('OPENAI_API_KEY')
                if api_key and api_key != 'your-api-key-here':
                    self.log("OpenAI API key configured", "SUCCESS")
                else:
                    self.log("OpenAI API key not configured", "ERROR")
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"LLM provider test failed: {e}", "ERROR")
            return False
    
    def test_tool_execution(self):
        """Test 5: Tool Execution"""
        self.log("Testing tool execution...", "TEST")
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location('villager_proper_mcp', 'mcp/villager_proper_mcp.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            VillagerProperMCP = module.VillagerProperMCP
            villager = VillagerProperMCP()
            
            # Test Python execution
            result = villager.execute_tool('pyeval', {'python_codeblock': 'print("Villager Python execution test")'})
            if result is not None or result == "":
                self.log("Python execution tool working", "SUCCESS")
            else:
                self.log("Python execution tool failed", "ERROR")
                return False
            
            # Test OS command execution
            result = villager.execute_tool('os_execute_cmd', {'system_command': 'echo "Villager OS command test"'})
            if result and len(result) > 0 and result[0]:
                self.log("OS command execution tool working", "SUCCESS")
            else:
                self.log("OS command execution tool failed", "ERROR")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"Tool execution test failed: {e}", "ERROR")
            return False
    
    def test_security_tools(self):
        """Test 6: Security Tools Availability"""
        self.log("Testing security tools availability...", "TEST")
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location('villager_proper_mcp', 'mcp/villager_proper_mcp.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            VillagerProperMCP = module.VillagerProperMCP
            villager = VillagerProperMCP()
            
            # Test common security tools
            security_tools = ['msfvenom', 'nmap', 'sqlmap', 'hydra', 'john']
            available_tools = []
            
            for tool in security_tools:
                result = villager.execute_tool('os_execute_cmd', {'system_command': f'which {tool}'})
                if result and len(result) > 0 and result[0] and tool in result[0]:
                    available_tools.append(tool)
                    self.log(f"Security tool '{tool}' available", "SUCCESS")
                else:
                    self.log(f"Security tool '{tool}' not found", "WARNING")
            
            if available_tools:
                self.log(f"Available security tools: {', '.join(available_tools)}", "SUCCESS")
                return True
            else:
                self.log("No security tools found", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Security tools test failed: {e}", "ERROR")
            return False
    
    def test_github_integration(self):
        """Test 7: GitHub Integration"""
        self.log("Testing GitHub integration...", "TEST")
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location('villager_proper_mcp', 'mcp/villager_proper_mcp.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            VillagerProperMCP = module.VillagerProperMCP
            villager = VillagerProperMCP()
            
            if villager.github_tools:
                self.log("GitHub tools initialized successfully", "SUCCESS")
                return True
            else:
                github_token = os.getenv('GITHUB_TOKEN')
                if github_token and github_token != 'your-github-token-here':
                    self.log("GitHub token configured but tools not initialized", "WARNING")
                else:
                    self.log("GitHub integration not configured (optional)", "WARNING")
                return True  # GitHub is optional
                
        except Exception as e:
            self.log(f"GitHub integration test failed: {e}", "ERROR")
            return False
    
    def test_docker_availability(self):
        """Test 8: Docker Availability"""
        self.log("Testing Docker availability...", "TEST")
        
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log(f"Docker available: {result.stdout.strip()}", "SUCCESS")
                return True
            else:
                self.log("Docker not available", "WARNING")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log("Docker not available", "WARNING")
            return False
        except Exception as e:
            self.log(f"Docker test failed: {e}", "ERROR")
            return False
    
    def run_all_tests(self):
        """Run all tests and provide summary."""
        self.log("🚀 Starting Villager AI Framework Test Suite", "INFO")
        self.log("=" * 50, "INFO")
        
        tests = [
            ("Environment Setup", self.test_environment_setup),
            ("Villager Imports", self.test_villager_imports),
            ("MCP Server", self.test_mcp_server),
            ("LLM Provider", self.test_llm_provider),
            ("Tool Execution", self.test_tool_execution),
            ("Security Tools", self.test_security_tools),
            ("GitHub Integration", self.test_github_integration),
            ("Docker Availability", self.test_docker_availability),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            self.log(f"\n🧪 Running: {test_name}", "TEST")
            try:
                if test_func():
                    self.test_results[test_name] = "PASSED"
                    passed += 1
                else:
                    self.test_results[test_name] = "FAILED"
            except Exception as e:
                self.log(f"Test '{test_name}' crashed: {e}", "ERROR")
                self.test_results[test_name] = "CRASHED"
        
        # Summary
        self.log("\n" + "=" * 50, "INFO")
        self.log("📊 TEST RESULTS SUMMARY", "INFO")
        self.log("=" * 50, "INFO")
        
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result == "PASSED" else "❌" if result == "FAILED" else "💥"
            self.log(f"{status_icon} {test_name}: {result}", "INFO")
        
        self.log(f"\n🎯 Overall: {passed}/{total} tests passed", "INFO")
        
        if passed == total:
            self.log("🎉 All tests passed! Villager framework is ready to use.", "SUCCESS")
            return True
        elif passed >= total * 0.8:
            self.log("⚠️ Most tests passed. Framework should work with minor issues.", "WARNING")
            return True
        else:
            self.log("❌ Multiple test failures. Please check your setup.", "ERROR")
            return False

def main():
    """Main test runner."""
    print("🏘️ Villager AI Framework - Test Suite")
    print("=====================================")
    print()
    
    tester = VillagerFrameworkTester()
    success = tester.run_all_tests()
    
    print()
    if success:
        print("🚀 Framework is ready for use!")
        print("   Run: ./start_villager_proper.sh")
        print("   Or: python3 mcp/villager_proper_mcp.py --debug")
    else:
        print("🔧 Please fix the issues above before using the framework.")
        print("   Check the documentation in docs/ for setup instructions.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
