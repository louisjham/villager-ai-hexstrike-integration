#!/usr/bin/env python3
"""
Villager HTTP MCP Server

Mirror HexStrike's CLI pattern: accepts --server (Villager FastAPI base URL)
and exposes MCP tools that proxy to Villager HTTP endpoints.

Tools exposed:
- get_status: GET /api/status - Server status and health
- villager_tool: Access to Villager internal Python tools
- create_agent: POST /api/agents/create - Create autonomous AI agents
- list_agents: GET /api/agents - List all active agents
- run_scan: POST /api/scans/run - Initiate security scans
- list_scans: GET /api/scans - List all active scans
- execute_shell: POST /api/exec/shell - Execute shell commands
- execute_python: POST /api/exec/python - Execute Python code
"""

import sys
import argparse
import logging
from typing import Any, Dict, List

import json
import importlib
import traceback
import urllib.request

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VillagerHttpClient:
    def __init__(self, base_url: str, timeout: int = 120):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _post_json(self, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        req = urllib.request.Request(
            url=url,
            data=json.dumps(body).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def _get_json(self, path: str) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        req = urllib.request.Request(url=url, method='GET')
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def exec_shell(self, cmd: str, timeout: int | None = None, cwd: str | None = None, env: Dict[str, str] | None = None) -> Dict[str, Any]:
        return self._post_json('/api/exec/shell', {
            'cmd': cmd,
            'timeout': timeout,
            'cwd': cwd,
            'env': env,
        })

    def exec_python(self, code: str, timeout: int | None = None) -> Dict[str, Any]:
        return self._post_json('/api/exec/python', {
            'code': code,
            'timeout': timeout,
        })

    # First-class HTTP wrappers for Villager features
    def get_status(self) -> Dict[str, Any]:
        return self._get_json('/api/status')

    def create_agent(self, name: str, task: str) -> Dict[str, Any]:
        return self._post_json('/api/agents/create', {
            'name': name,
            'task': task,
        })

    def list_agents(self) -> Dict[str, Any]:
        return self._get_json('/api/agents')

    def run_scan(self, target: str, scan_type: str | None = None) -> Dict[str, Any]:
        return self._post_json('/api/scans/run', {
            'target': target,
            'scan_type': scan_type or 'comprehensive',
        })

    def list_scans(self) -> Dict[str, Any]:
        return self._get_json('/api/scans')


def build_server(client: VillagerHttpClient) -> Server:
    server = Server("villager")

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            # Core Villager Tools
            Tool(
                name="get_status",
                description="Get Villager server status summary (agents, scans, server time)",
                inputSchema={"type": "object", "properties": {}},
            ),
            Tool(
                name="villager_tool",
                description=(
                    "Dispatch to Villager internal Python tools. Use { tool, params }. "
                    "tool can be 'module:function' (e.g., 'scheduler.core.tools.common_tool:pyeval') "
                    "or a bare name searched in common modules (pyeval, os_execute_cmd, tool_villager)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tool": {"type": "string"},
                        "params": {"type": "object", "additionalProperties": True}
                    },
                    "required": ["tool"]
                },
            ),
            
            # Agent Management Tools
            Tool(
                name="create_agent",
                description="Create an autonomous AI agent for penetration testing. The agent will work independently to complete the specified task.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Unique name for the agent (e.g., 'AsyncRAT_Agent', 'PenTest_Agent')"},
                        "task": {"type": "string", "description": "Detailed task description including: 1) Analysis steps, 2) Execution methods, 3) Expected outcomes, 4) Reporting requirements"}
                    },
                    "required": ["name", "task"]
                },
            ),
            Tool(
                name="list_agents",
                description="List all active agents and their current status (pending, processing, completed, error)",
                inputSchema={"type": "object", "properties": {}},
            ),
            
            # Security Scan Tools
            Tool(
                name="run_scan",
                description="Initiate a security scan against a target. The scan will run autonomously and provide results.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "target": {"type": "string", "description": "Target to scan (IP, domain, URL, etc.)"},
                        "scan_type": {"type": "string", "description": "Type of scan to perform", "default": "comprehensive"}
                    },
                    "required": ["target"]
                },
            ),
            Tool(
                name="list_scans",
                description="List all active security scans and their progress",
                inputSchema={"type": "object", "properties": {}},
            ),
            
            # Direct Execution Tools (for agent support)
            Tool(
                name="execute_shell",
                description="Execute shell commands with full system access. Use sparingly - prefer creating agents for complex tasks.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cmd": {"type": "string", "description": "Shell command to execute"},
                        "timeout": {"type": "integer", "description": "Command timeout in seconds", "default": 120},
                        "cwd": {"type": "string", "description": "Working directory for command execution"},
                        "env": {"type": "object", "description": "Environment variables for command execution"}
                    },
                    "required": ["cmd"]
                },
            ),
            Tool(
                name="execute_python",
                description="Execute Python code with full system access. Use sparingly - prefer creating agents for complex tasks.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Python code to execute"},
                        "timeout": {"type": "integer", "description": "Execution timeout in seconds", "default": 120}
                    },
                    "required": ["code"]
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            # Core Villager Tools
            if name == "get_status":
                result = client.get_status()
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            if name == "villager_tool":
                tool_str = arguments.get("tool", "")
                params = arguments.get("params") or {}

                def _resolve(tool_name: str):
                    if ":" in tool_name:
                        mod_name, func_name = tool_name.split(":", 1)
                        mod = importlib.import_module(mod_name)
                        func = getattr(mod, func_name)
                        return func
                    # Search common Villager modules for bare function name
                    candidates = [
                        "scheduler.core.tools.common_tool",
                        "scheduler.core.tools.agent_with_tools",
                    ]
                    for mod_name in candidates:
                        try:
                            mod = importlib.import_module(mod_name)
                            if hasattr(mod, tool_name):
                                return getattr(mod, tool_name)
                        except Exception:
                            continue
                    raise ImportError(f"Tool not found: {tool_name}")

                try:
                    func = _resolve(tool_str)
                    result = func(**params) if callable(func) else func
                    try:
                        text = json.dumps(result, ensure_ascii=False, indent=2)
                    except Exception:
                        text = str(result)
                    return [TextContent(type="text", text=text)]
                except Exception as e:
                    err = f"villager_tool error: {e}\n{traceback.format_exc()}"
                    return [TextContent(type="text", text=err)]
            
            # Agent Management Tools
            if name == "create_agent":
                name_param = arguments.get("name", "")
                task = arguments.get("task", "")
                result = client.create_agent(name_param, task)
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            if name == "list_agents":
                result = client.list_agents()
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            # Security Scan Tools
            if name == "run_scan":
                target = arguments.get("target", "")
                scan_type = arguments.get("scan_type", "comprehensive")
                result = client.run_scan(target, scan_type)
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            if name == "list_scans":
                result = client.list_scans()
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            # Direct Execution Tools
            if name == "execute_shell":
                cmd = arguments.get("cmd", "")
                timeout = arguments.get("timeout", 120)
                cwd = arguments.get("cwd")
                env = arguments.get("env")
                result = client.exec_shell(cmd, timeout, cwd, env)
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            if name == "execute_python":
                code = arguments.get("code", "")
                timeout = arguments.get("timeout", 120)
                result = client.exec_python(code, timeout)
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        except Exception as e:
            logger.exception("Tool error")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    return server


def parse_args():
    p = argparse.ArgumentParser(description="Villager HTTP MCP Server")
    p.add_argument("--server", type=str, default="http://127.0.0.1:37695", help="Villager FastAPI base URL")
    p.add_argument("--timeout", type=int, default=120)
    return p.parse_args()


async def run():
    args = parse_args()
    
    # Display banner
    try:
        from villager_visuals import create_ascii_font, create_banner, create_startup_message, create_success_message
        print(create_ascii_font())
        print(create_banner())
        print(create_startup_message())
        print(create_success_message("Villager HTTP MCP starting successfully"))
    except ImportError:
        # Fallback banner if villager_visuals is not available
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    🏘️  VILLAGER AI 🏘️                      ║
║                                                              ║
║              Autonomous Agent Framework                      ║
║              for Security Testing & Research                 ║
║                                                              ║
║  🤖 Create custom agents for any security task              ║
║  🔧 GitHub Tool Discovery & Integration                     ║
║  🚀 Flexible framework for autonomous operations            ║
╚══════════════════════════════════════════════════════════════╝
        """)
    except Exception as e:
        from villager_visuals import create_error_message
        print(create_error_message(f"Could not display banner: {e}"))
    
    logger.info("🚀 Starting Villager HTTP MCP")
    logger.info(f"🔗 Base URL: {args.server}")
    client = VillagerHttpClient(args.server, args.timeout)
    server = build_server(client)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())



