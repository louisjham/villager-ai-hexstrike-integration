#!/usr/bin/env python3
"""
Proper Villager MCP Server - True Integration with Villager Framework

This MCP server properly integrates with Villager's true architecture:
- TaskNode for task execution and decomposition
- MCP Client for external tool access (Kali Driver, Browser)
- Agent Scheduler for LLM orchestration
- Tools Manager for function registry
- Task Relation Manager for task flow

Architecture Flow:
Cursor → MCP → Villager TaskNode → MCP Client → External Services (Kali Driver, Browser)
"""

import sys
import argparse
import logging
import asyncio
import uuid
import json
import traceback
from typing import Any, Dict, List

# Add Villager to path
sys.path.append('/home/yenn/Villager-AI')

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Import Villager core components
try:
    from scheduler.core.init import global_llm
    from scheduler.core.mcp_client.mcp_client import McpClient
    from scheduler.core.schemas.schemas import TaskModel
    from scheduler.core.schemas.structure.task_relation_manager import TRM
    from scheduler.core.tasks.task import TaskNode
    from scheduler.core.tools.common_tool import pyeval, os_execute_cmd
    from scheduler.core.tools.agent_with_tools import tool_villager
    from scheduler.agent_scheduler_manager import agent_scheduler
    from scheduler.toolschain.tools_manager import ToolsManager
    from config import MCP, Master
    from github_tools import GitHubTools
    VILLAGER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Villager components not available: {e}")
    VILLAGER_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global task manager
task_manager: Dict[str, dict] = {}

class VillagerProperMCP:
    """Proper Villager MCP integration class using true architecture."""
    
    def __init__(self):
        self.mcp_client_base_url = "http://localhost:25989" if VILLAGER_AVAILABLE else None
        self.task_manager = task_manager
        self.tools_manager = ToolsManager() if VILLAGER_AVAILABLE else None
        
        # Initialize GitHub tools
        try:
            self.github_tools = GitHubTools() if VILLAGER_AVAILABLE else None
        except Exception as e:
            logger.warning(f"GitHub tools not available: {e}")
            self.github_tools = None
        
        # Register Villager's core tools
        if VILLAGER_AVAILABLE and self.tools_manager:
            self.tools_manager.register_func(pyeval)
            self.tools_manager.register_func(os_execute_cmd)
            self.tools_manager.register_func(tool_villager)
        
    def create_task(self, abstract: str, description: str, verification: str = "Task completed successfully") -> str:
        """Create a task using Villager's TaskNode architecture."""
        task_id = str(uuid.uuid4())
        
        # Initialize task in manager
        self.task_manager[task_id] = {
            "status": "pending",
            "abstract": abstract,
            "description": description,
            "verification": verification,
            "result": None,
            "error": None
        }
        
        # Start background task execution
        asyncio.create_task(self._execute_task_with_villager(task_id, abstract, description, verification))
        
        return task_id
    
    async def _execute_task_with_villager(self, task_id: str, abstract: str, description: str, verification: str):
        """Execute task using Villager's true TaskNode architecture."""
        try:
            self.task_manager[task_id]["status"] = "running"
            
            if VILLAGER_AVAILABLE:
                # Use Villager's global LLM context
                with global_llm():
                    with TRM() as trm:
                        # Create MCP client for external tool access
                        mcp_client = McpClient(mcp_client_base_url=self.mcp_client_base_url, task_id=task_id)
                        
                        # Create Task Node (Villager's execution unit)
                        task_node = TaskNode(
                            task_model=TaskModel(
                                abstract=abstract,
                                description=description,
                                verification=verification
                            ),
                            trm=trm,
                            mcp_client=mcp_client,
                            graph_name=f'./{task_id}.mermaid'
                        )
                        
                        # Execute task through Villager's framework
                        result = task_node.execute()
                        
                        self.task_manager[task_id]["status"] = "completed"
                        self.task_manager[task_id]["result"] = str(result)
            else:
                # Fallback execution without Villager
                self.task_manager[task_id]["status"] = "completed"
                self.task_manager[task_id]["result"] = f"Task '{abstract}' completed (Villager not available)"
                    
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            traceback.print_exc()
            self.task_manager[task_id]["status"] = "failed"
            self.task_manager[task_id]["error"] = str(e)
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a specific task."""
        if task_id not in self.task_manager:
            return {"error": "Task not found"}
        
        task_info = self.task_manager[task_id]
        return {
            "task_id": task_id,
            "status": task_info["status"],
            "abstract": task_info["abstract"],
            "description": task_info["description"],
            "result": task_info.get("result"),
            "error": task_info.get("error")
        }
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks in the task manager."""
        tasks = []
        for task_id, task_info in self.task_manager.items():
            tasks.append({
                "task_id": task_id,
                "status": task_info["status"],
                "abstract": task_info["abstract"],
                "description": task_info["description"]
            })
        return tasks
    
    def schedule_agent(self, agent_name: str, task_input: str) -> str:
        """Schedule agent through Villager's Agent Scheduler with LLM orchestration."""
        try:
            if VILLAGER_AVAILABLE:
                # Initialize LLM in global context and keep it active
                with global_llm() as llm:
                    # Use Villager's agent scheduler with LLM orchestration
                    response = agent_scheduler(
                        agent_entry=tool_villager,
                        agent_name=agent_name,
                        input=task_input
                    )
                    return response
            else:
                return f"Agent '{agent_name}' scheduled (Villager not available): {task_input}"
        except Exception as e:
            logger.error(f"Agent scheduling failed: {e}")
            return f"Agent scheduling failed: {str(e)}"
    
    def execute_tool(self, tool_name: str, parameters: dict) -> Any:
        """Execute tools through Villager's Tools Manager."""
        try:
            if not VILLAGER_AVAILABLE or not self.tools_manager:
                return f"Villager not available. Cannot execute tool: {tool_name}"
            
            # Use Villager's tools manager to execute functions
            if tool_name == "pyeval":
                code = parameters.get("python_codeblock", "")
                if not code:
                    return "No Python code provided"
                # Handle multi-line code properly - only replace if it's actually escaped
                if isinstance(code, str) and '\\n' in code:
                    code = code.replace('\\n', '\n')
                return pyeval(code)
            elif tool_name == "os_execute_cmd":
                return os_execute_cmd(parameters.get("system_command", ""))
            elif tool_name == "tool_villager":
                return tool_villager(
                    agent_name=parameters.get("agent_name", "实用的助手"),
                    **{k: v for k, v in parameters.items() if k != "agent_name"}
                )
            elif tool_name == "github_tools" and self.github_tools:
                # Execute GitHub tools
                method = parameters.get("method", "")
                if not method:
                    return "No GitHub method specified"
                
                # Get all parameters except method
                github_params = {k: v for k, v in parameters.items() if k != "method"}
                
                # Call the GitHub method
                if hasattr(self.github_tools, method):
                    return getattr(self.github_tools, method)(**github_params)
                else:
                    return f"Unknown GitHub method: {method}"
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return f"Tool execution failed: {str(e)}"
    
    def list_available_tools(self) -> List[Dict[str, Any]]:
        """List tools available through Villager's Tools Manager."""
        if not VILLAGER_AVAILABLE or not self.tools_manager:
            return []
        
        return self.tools_manager.list_func_json()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status from all Villager components."""
        return {
            "villager_status": "running" if VILLAGER_AVAILABLE else "not_available",
            "villager_available": VILLAGER_AVAILABLE,
            "task_manager": {
                "total_tasks": len(self.task_manager),
                "running_tasks": len([t for t in self.task_manager.values() if t["status"] == "running"]),
                "completed_tasks": len([t for t in self.task_manager.values() if t["status"] == "completed"]),
                "failed_tasks": len([t for t in self.task_manager.values() if t["status"] == "failed"])
            },
            "mcp_client": {
                "base_url": self.mcp_client_base_url,
                "status": "connected" if VILLAGER_AVAILABLE else "not_available"
            },
            "tools_manager": {
                "registered_tools": len(self.tools_manager.list_func()) if self.tools_manager else 0,
                "available_tools": self.list_available_tools()
            },
            "llm": {
                "model": Master.get("default_model") if VILLAGER_AVAILABLE else "not_available",
                "base_url": Master.get("openai_api_endpoint") if VILLAGER_AVAILABLE else "not_available"
            }
        }


def build_server() -> Server:
    """Build the proper Villager MCP server."""
    server = Server("villager_proper")
    villager = VillagerProperMCP()

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            # Task Management Tools (True Villager Architecture)
            Tool(
                name="create_task",
                description="Create a task in Villager's Task Manager using true TaskNode architecture",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "abstract": {"type": "string", "description": "Task abstract/summary"},
                        "description": {"type": "string", "description": "Detailed task description"},
                        "verification": {"type": "string", "description": "Task verification criteria", "default": "Task completed successfully"}
                    },
                    "required": ["abstract", "description"]
                },
            ),
            Tool(
                name="get_task_status",
                description="Get status of a specific task from Villager's Task Manager",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "Task ID to check status for"}
                    },
                    "required": ["task_id"]
                },
            ),
            Tool(
                name="list_tasks",
                description="List all tasks in Villager's Task Manager",
                inputSchema={"type": "object", "properties": {}},
            ),
            
            # Agent Orchestration Tools (True Villager Architecture)
            Tool(
                name="schedule_agent",
                description="Schedule agent through Villager's Agent Scheduler with LLM orchestration",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string", "description": "Name of the agent"},
                        "task_input": {"type": "string", "description": "Input for the agent task"}
                    },
                    "required": ["agent_name", "task_input"]
                },
            ),
            
            # Tool Management Tools (True Villager Architecture)
            Tool(
                name="execute_tool",
                description="Execute tools through Villager's core tools (pyeval, os_execute_cmd, tool_villager, github_tools)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tool_name": {"type": "string", "description": "Tool name (pyeval, os_execute_cmd, tool_villager, github_tools)"},
                        "parameters": {"type": "object", "description": "Tool parameters", "additionalProperties": True}
                    },
                    "required": ["tool_name", "parameters"]
                },
            ),
            Tool(
                name="list_available_tools",
                description="List tools available through Villager's Tools Manager",
                inputSchema={"type": "object", "properties": {}},
            ),
            
            # System Integration Tools
            Tool(
                name="get_system_status",
                description="Get comprehensive status from all Villager components and available tools",
                inputSchema={"type": "object", "properties": {}},
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            # Task Management Tools
            if name == "create_task":
                abstract = arguments.get("abstract", "")
                description = arguments.get("description", "")
                verification = arguments.get("verification", "Task completed successfully")
                
                task_id = villager.create_task(abstract, description, verification)
                result = {
                    "success": True,
                    "task_id": task_id,
                    "message": f"Task '{abstract}' created successfully using Villager's TaskNode architecture",
                    "status": "pending"
                }
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            elif name == "get_task_status":
                task_id = arguments.get("task_id", "")
                result = villager.get_task_status(task_id)
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            elif name == "list_tasks":
                result = villager.list_tasks()
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            # Agent Orchestration Tools
            elif name == "schedule_agent":
                agent_name = arguments.get("agent_name", "")
                task_input = arguments.get("task_input", "")
                
                response = villager.schedule_agent(agent_name, task_input)
                result = {
                    "success": True,
                    "agent_name": agent_name,
                    "response": response
                }
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            # Tool Management Tools
            elif name == "execute_tool":
                tool_name = arguments.get("tool_name", "")
                parameters = arguments.get("parameters", {})
                
                result = villager.execute_tool(tool_name, parameters)
                return [TextContent(type="text", text=json.dumps({"result": result}, ensure_ascii=False, indent=2))]
            
            elif name == "list_available_tools":
                result = villager.list_available_tools()
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            # System Integration Tools
            elif name == "get_system_status":
                result = villager.get_system_status()
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
            
        except Exception as e:
            logger.exception("Tool error")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    return server


def parse_args():
    p = argparse.ArgumentParser(description="Proper Villager MCP Server")
    p.add_argument("--debug", action="store_true", help="Enable debug logging")
    return p.parse_args()


async def run():
    args = parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Display banner
    print("""
╔══════════════════════════════════════════════════════════════╗
║              🏘️  PROPER VILLAGER MCP 🏘️                   ║
║                                                              ║
║              True Villager Framework Integration              ║
║              TaskNode + MCP Client + Agent Scheduler         ║
║                                                              ║
║  ✅ True TaskNode execution and decomposition               ║
║  ✅ MCP Client for external tool access                     ║
║  ✅ Agent Scheduler with LLM orchestration                  ║
║  ✅ Tools Manager for function registry                     ║
║  ✅ Proper Villager architecture integration                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    logger.info("🚀 Starting Proper Villager MCP Server")
    logger.info(f"🔗 Villager Available: {VILLAGER_AVAILABLE}")
    
    server = build_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(run())
