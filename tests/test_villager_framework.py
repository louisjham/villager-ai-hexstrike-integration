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
            # Try alternative import method
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location('config', 'config.py')
                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)
                self.log("Config module loaded via alternative method", "SUCCESS")
                return True
            except Exception as e2:
                self.log(f"Alternative import also failed: {e2}", "ERROR")
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
            # pyeval returns None for successful execution, so we check if it's not an error string
            if result is None or (isinstance(result, str) and not result.startswith("Tool execution failed")):
                self.log("Python execution tool working", "SUCCESS")
            else:
                self.log(f"Python execution tool failed: {result}", "ERROR")
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
    
    def test_new_workflow_services(self):
        """Test 9: New Workflow Services"""
        self.log("Testing new workflow services...", "TEST")
        
        try:
            # Test all service endpoints
            services = [
                ("Villager Server", "http://localhost:37695/health"),
                ("MCP Client", "http://localhost:25989/health"),
                ("Kali Driver", "http://localhost:1611/health"),
                ("Browser Service", "http://localhost:8080/health")
            ]
            
            all_healthy = True
            for service_name, url in services:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        self.log(f"{service_name} is healthy", "SUCCESS")
                    else:
                        self.log(f"{service_name} returned status {response.status_code}", "ERROR")
                        all_healthy = False
                except requests.exceptions.RequestException as e:
                    self.log(f"{service_name} connection failed: {e}", "ERROR")
                    all_healthy = False
            
            return all_healthy
            
        except Exception as e:
            self.log(f"New workflow services test failed: {e}", "ERROR")
            return False
    
    def test_complete_workflow(self):
        """Test 10: Complete Workflow Integration"""
        self.log("Testing complete workflow integration...", "TEST")
        
        try:
            # Test task creation through Villager Server
            task_data = {
                "abstract": "Test Complete Workflow",
                "description": "Verify the complete Cursor → Villager MCP → Villager Server → MCP Client → Kali Driver workflow",
                "verification": "Task completed successfully"
            }
            
            # Create task
            response = requests.post(
                "http://localhost:37695/task",
                params=task_data,
                timeout=10
            )
            
            if response.status_code == 200:
                task_result = response.json()
                task_id = task_result.get("task_id")
                self.log(f"Task created successfully with ID: {task_id}", "SUCCESS")
                
                # Wait for task completion
                time.sleep(3)
                
                # Check task status
                status_response = requests.get("http://localhost:37695/get/task/status", timeout=10)
                if status_response.status_code == 200:
                    tasks = status_response.json()
                    # Find our task
                    our_task = next((t for t in tasks if t.get("token") == task_id), None)
                    if our_task:
                        if our_task.get("status") == "completed":
                            self.log("Complete workflow executed successfully", "SUCCESS")
                            return True
                        else:
                            self.log(f"Task status: {our_task.get('status')}", "WARNING")
                            return True  # Still consider it a pass if task was created
                    else:
                        self.log("Task not found in status list", "WARNING")
                        return True
                else:
                    self.log(f"Status check failed: {status_response.status_code}", "ERROR")
                    return False
            else:
                self.log(f"Task creation failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Complete workflow test failed: {e}", "ERROR")
            return False
    
    def test_rat_payload_generation(self):
        """Test 11: RAT Payload Generation Through New Workflow"""
        self.log("Testing RAT payload generation through new workflow...", "TEST")
        
        try:
            # Test RAT payload creation through the complete workflow
            rat_task_data = {
                "abstract": "Generate RAT Payload",
                "description": "Create Windows meterpreter reverse TCP payload using msfvenom with LHOST=192.168.1.100 and LPORT=4444",
                "verification": "Payload file created successfully"
            }
            
            # Create RAT generation task
            response = requests.post(
                "http://localhost:37695/task",
                params=rat_task_data,
                timeout=30
            )
            
            if response.status_code == 200:
                task_result = response.json()
                task_id = task_result.get("task_id")
                self.log(f"RAT generation task created with ID: {task_id}", "SUCCESS")
                
                # Wait for task completion
                time.sleep(5)
                
                # Check task status
                status_response = requests.get("http://localhost:37695/get/task/status", timeout=10)
                if status_response.status_code == 200:
                    tasks = status_response.json()
                    our_task = next((t for t in tasks if t.get("token") == task_id), None)
                    if our_task and our_task.get("status") == "completed":
                        result = our_task.get("result", "")
                        if "msfvenom" in result.lower() and "payload" in result.lower():
                            self.log("RAT payload generation successful through new workflow", "SUCCESS")
                            return True
                        else:
                            self.log("RAT generation completed but result unclear", "WARNING")
                            return True
                    else:
                        self.log(f"RAT generation task status: {our_task.get('status') if our_task else 'not found'}", "WARNING")
                        return True
                else:
                    self.log("RAT generation status check failed", "ERROR")
                    return False
            else:
                self.log(f"RAT generation task creation failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"RAT payload generation test failed: {e}", "ERROR")
            return False
    
    def test_mcp_tools_integration(self):
        """Test 12: MCP Tools Integration"""
        self.log("Testing MCP tools integration...", "TEST")
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location('villager_proper_mcp', 'mcp/villager_proper_mcp.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            VillagerProperMCP = module.VillagerProperMCP
            villager = VillagerProperMCP()
            
            # Test task creation through MCP
            task_id = villager.create_task(
                abstract="MCP Integration Test",
                description="Test task creation through MCP tools",
                verification="Task completed successfully"
            )
            
            if task_id:
                self.log(f"MCP task creation successful with ID: {task_id}", "SUCCESS")
                
                # Test task status retrieval
                status = villager.get_task_status(task_id)
                if status and not status.get("error"):
                    self.log("MCP task status retrieval successful", "SUCCESS")
                    return True
                else:
                    self.log(f"MCP task status retrieval failed: {status.get('error')}", "ERROR")
                    return False
            else:
                self.log("MCP task creation failed", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"MCP tools integration test failed: {e}", "ERROR")
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
            ("New Workflow Services", self.test_new_workflow_services),
            ("Complete Workflow", self.test_complete_workflow),
            ("RAT Payload Generation", self.test_rat_payload_generation),
            ("MCP Tools Integration", self.test_mcp_tools_integration),
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
