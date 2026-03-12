#!/usr/bin/env python3
"""
Villager MCP Server — Hexclaw Integration Build

Architecture:
    Hexclaw / Cursor
        └─► MCP stdio  (this file)
                ├─► VillagerProperMCP.create_mission()   ← Hexclaw fire-and-forget
                ├─► VillagerProperMCP.create_task()      ← granular tasks
                └─► Background thread → asyncio loop
                        └─► _execute_task_with_villager()
                                ├─► Villager TaskNode + LLM  (when available)
                                │       └─► McpClient → HexStrike, Kali Driver, Browser
                                └─► HTTP fallback              (when Villager not installed)

Key improvements over original:
  ✅ TaskNode path wired — LLM actually reasons and calls tools
  ✅ SQLite persistence via task_store.py
  ✅ Webhook callbacks for Hexclaw fire-and-forget
  ✅ create_mission() — high-level Hexclaw entry point
  ✅ HexStrike tool context injected into every task description
  ✅ Config import no longer raises ValueError at module load
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import threading
import traceback
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Path setup ────────────────────────────────────────────────────────────────
VILLAGER_ROOT = os.getenv("VILLAGER_ROOT", str(Path(__file__).parent.parent.parent.parent))

_src = str(Path(VILLAGER_ROOT) / "src")
_vaai = str(Path(_src) / "villager_ai")

for _p in [VILLAGER_ROOT, _src, _vaai]:
    if _p not in sys.path:
        sys.path.insert(0, _p)



# ── Visual helpers (optional) ─────────────────────────────────────────────────
try:
    from villager_visuals import (
        create_agent_message,
        create_error_message,
        create_github_message,
        create_info_message,
        create_success_message,
        create_warning_message,
    )
    VISUALS_AVAILABLE = True
except ImportError:
    VISUALS_AVAILABLE = False

# ── MCP protocol ──────────────────────────────────────────────────────────────
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# ── Persistent task store ─────────────────────────────────────────────────────
try:
    from task_store import delete_task as _store_delete
    from task_store import get_task as _store_get
    from task_store import init_db as _store_init
    from task_store import list_tasks as _store_list
    from task_store import upsert_task as _store_upsert
    TASK_STORE_AVAILABLE = True
except ImportError:
    TASK_STORE_AVAILABLE = False

# ── Villager framework (optional — graceful fallback when not installed) ───────
try:
    from config import MCP, Master
    from github_tools import GitHubTools
    from scheduler.agent_scheduler_manager import agent_scheduler
    from scheduler.core.init import global_llm
    from scheduler.core.mcp_client.mcp_client import McpClient
    from scheduler.core.schemas.schemas import TaskModel
    from scheduler.core.schemas.structure.task_relation_manager import TRM
    from scheduler.core.tasks.task import TaskNode
    from scheduler.core.tools.agent_with_tools import tool_villager
    from scheduler.core.tools.common_tool import os_execute_cmd, pyeval
    from scheduler.toolschain.tools_manager import ToolsManager
    VILLAGER_AVAILABLE = True
except ImportError as e:
    print(f"ℹ️  Villager framework not installed — HTTP fallback mode active: {e}", file=sys.stderr)
    VILLAGER_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HexStrike endpoint exposed to the task LLM
HEXSTRIKE_MCP_URL = os.getenv("HEXSTRIKE_MCP_URL", "http://localhost:8000")


# ─────────────────────────────────────────────────────────────────────────────
# Thin adapter layer — hides SQLite vs memory depending on availability
# ─────────────────────────────────────────────────────────────────────────────
_memory: Dict[str, dict] = {}


def _upsert(task_id: str, **kw) -> None:
    if TASK_STORE_AVAILABLE:
        _store_upsert(task_id, **kw)
    else:
        rec = _memory.setdefault(task_id, {})
        rec.update(kw)


def _get(task_id: str) -> Optional[dict]:
    if TASK_STORE_AVAILABLE:
        return _store_get(task_id)
    return _memory.get(task_id)


def _list(source: str = None, status: str = None) -> List[dict]:
    if TASK_STORE_AVAILABLE:
        return _store_list(source=source, status=status)
    rows = list(_memory.values())
    if source:
        rows = [r for r in rows if r.get("source") == source]
    if status:
        rows = [r for r in rows if r.get("status") == status]
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# Core integration class
# ─────────────────────────────────────────────────────────────────────────────

class VillagerProperMCP:
    """Proper Villager MCP integration using true TaskNode architecture."""

    def __init__(self):
        self.mcp_client_base_url = "http://localhost:25989" if VILLAGER_AVAILABLE else None
        self.tools_manager = ToolsManager() if VILLAGER_AVAILABLE else None

        # Init persistent store
        if TASK_STORE_AVAILABLE:
            try:
                _store_init()
            except Exception as exc:
                logger.warning(f"Task store init failed — using memory: {exc}")

        # GitHub tools
        try:
            self.github_tools = GitHubTools() if VILLAGER_AVAILABLE else None
            if VISUALS_AVAILABLE and self.github_tools:
                print(create_github_message("GitHub integration initialised"), file=sys.stderr)
        except Exception as exc:
            self.github_tools = None
            logger.warning(f"GitHub tools not available: {exc}")

        # Register core tools
        if VILLAGER_AVAILABLE and self.tools_manager:
            self.tools_manager.register_func(pyeval)
            self.tools_manager.register_func(os_execute_cmd)
            self.tools_manager.register_func(tool_villager)

    # ─────────────────────────────────────────────────────────────────────────
    # Public — Task lifecycle
    # ─────────────────────────────────────────────────────────────────────────

    def create_task(
        self,
        abstract: str,
        description: str,
        verification: str = "Task completed successfully",
        callback_url: Optional[str] = None,
        source: str = "unknown",
    ) -> str:
        """
        Persist a task and immediately start executing it on a background thread.

        Uses Villager's true TaskNode / LLM reasoning loop when available,
        otherwise falls back to keyword-routed HTTP execution.

        Returns task_id immediately — fire and forget.
        """
        task_id = str(uuid.uuid4())

        _upsert(
            task_id,
            status="pending",
            abstract=abstract,
            description=description,
            verification=verification,
            callback_url=callback_url,
            source=source,
        )

        if VISUALS_AVAILABLE:
            print(create_agent_message(f"Task queued [{task_id[:8]}]: {abstract}"), file=sys.stderr)

        def _run():
            # Each background thread gets its own event loop — asyncio-safe.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(
                    self._execute_task_with_villager(
                        task_id, abstract, description, verification, callback_url
                    )
                )
            except Exception as exc:
                logger.error(f"Task thread {task_id[:8]} crashed: {exc}")
                _upsert(task_id, status="failed", error=str(exc))
            finally:
                loop.close()

        t = threading.Thread(target=_run, name=f"villager-{task_id[:8]}", daemon=True)
        t.start()
        return task_id

    async def _execute_task_with_villager(
        self,
        task_id: str,
        abstract: str,
        description: str,
        verification: str,
        callback_url: Optional[str] = None,
    ) -> None:
        """
        Core execution engine.

        When Villager is installed: uses global_llm() + TRM + TaskNode so the LLM
        reasons about the task, calls HexStrike / Kali Driver / Browser tools in
        a loop, then returns a synthesised result.

        When Villager is not installed: falls back to keyword-routed HTTP calls.
        """
        _upsert(task_id, status="running")
        result_str = ""

        try:
            if VILLAGER_AVAILABLE:
                # Augment description so the LLM knows about all available tools
                aug_description = self._build_tool_context(description)

                with global_llm():
                    with TRM() as trm:
                        mcp_client = McpClient(
                            mcp_client_base_url=self.mcp_client_base_url,
                            task_id=task_id,
                        )
                        task_node = TaskNode(
                            task_model=TaskModel(
                                abstract=abstract,
                                description=aug_description,
                                verification=verification,
                            ),
                            trm=trm,
                            mcp_client=mcp_client,
                            graph_name=f"./{task_id}.mermaid",
                        )
                        result_str = str(task_node.execute())

                _upsert(task_id, status="completed", result=result_str)
                if VISUALS_AVAILABLE:
                    print(create_success_message(f"Task {task_id[:8]} completed via TaskNode"), file=sys.stderr)

            else:
                # HTTP fallback — no LLM reasoning, direct routing
                result_str = await self._http_fallback(abstract, description)
                _upsert(task_id, status="completed", result=result_str)

        except Exception as exc:
            logger.error(f"Task {task_id} failed: {exc}")
            traceback.print_exc(file=sys.stderr)
            _upsert(task_id, status="failed", error=str(exc))
            if VISUALS_AVAILABLE:
                print(create_error_message(f"Task {task_id[:8]} failed: {exc}"), file=sys.stderr)

        finally:
            if callback_url:
                await self._fire_callback(task_id, callback_url)

    def _build_tool_context(self, description: str) -> str:
        """
        Append a tool inventory to the description so the LLM knows exactly
        how to reach HexStrike, Kali Driver, and Browser services.
        """
        ctx = f"""

=== AVAILABLE TOOLS ===

HexStrike MCP ({HEXSTRIKE_MCP_URL}) — 150+ security tools:
  Network  : nmap_scan, masscan, rustscan, netdiscover
  Web      : gobuster_scan, dirb, nikto_scan, sqlmap_scan, wfuzz
  Passwords: hydra_attack, hashcat_crack, john_crack, medusa
  Payloads : msfvenom_generate, custom exploits
  Post-Exp : metasploit modules, mimikatz, empire
  OSINT    : theHarvester, maltego, recon-ng

Kali Driver (http://localhost:1611) — direct WSL shell execution:
  Use for: any CLI security tool, custom scripts, file operations
  Endpoint: POST / with {{"prompt": "<shell command>"}}

Browser Service (http://localhost:8080) — web automation:
  Use for: OSINT, web recon, form interaction, screenshot capture
  Endpoint: POST / with {{"prompt": "<browser instruction>"}}

=== END TOOLS ===
"""
        return description + ctx

    async def _http_fallback(self, abstract: str, description: str) -> str:
        """Keyword-routed HTTP execution when Villager LLM is unavailable."""
        import requests

        combined = (abstract + " " + description).lower()
        url = (
            "http://localhost:8080/"
            if any(k in combined for k in ("browser", "web", "scrape", "osint", "screenshot"))
            else "http://localhost:1611/"
        )
        prompt = f"Execute: {abstract}. {description}"
        try:
            resp = requests.post(url, json={"prompt": prompt}, timeout=90)
            if resp.status_code == 200:
                return resp.json().get("content", f"Task '{abstract}' executed (no Villager)")
            return f"Service error HTTP {resp.status_code}"
        except Exception as exc:
            return f"HTTP execution error: {exc}"

    async def _fire_callback(self, task_id: str, callback_url: str) -> None:
        """POST the completed task record to Hexclaw's webhook URL."""
        task = _get(task_id) or {}
        try:
            import httpx
            async with httpx.AsyncClient(timeout=15) as client:
                await client.post(
                    callback_url,
                    json={
                        "task_id": task_id,
                        "status":  task.get("status"),
                        "abstract": task.get("abstract"),
                        "result":  task.get("result"),
                        "error":   task.get("error"),
                    },
                )
            logger.info(f"Callback fired: task {task_id[:8]} → {callback_url}")
        except Exception as exc:
            logger.warning(f"Callback failed for {task_id[:8]}: {exc}")

    def get_task_status(self, task_id: str) -> dict:
        task = _get(task_id)
        return task if task else {"error": f"Task {task_id} not found"}

    def list_tasks(
        self,
        source: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[dict]:
        return _list(source=source, status=status)

    # ─────────────────────────────────────────────────────────────────────────
    # Public — Mission (Hexclaw high-level entry point)
    # ─────────────────────────────────────────────────────────────────────────

    def create_mission(
        self,
        mission: str,
        target_scope: str,
        constraints: Optional[List[str]] = None,
        callback_url: Optional[str] = None,
    ) -> str:
        """
        High-level Hexclaw entry point.

        Wraps create_task with a rich, structured description so Villager's LLM
        knows the target, rules of engagement, and full tool inventory — then
        autonomously decomposes and executes the whole mission.
        """
        roe = "\n".join(f"  • {c}" for c in (constraints or []))
        description = (
            f"Target Scope: {target_scope}\n\n"
            f"Rules of Engagement:\n{roe if roe else '  • No specific constraints'}\n\n"
            "Autonomously decompose this mission into phases. For each phase, select\n"
            "and execute the appropriate security tools from the available inventory.\n"
            "Collect all findings, analyse results, and produce a consolidated report."
        )
        verification = (
            "Comprehensive findings report covering all executed phases: "
            "open ports, running services, identified CVEs, exploitation outcomes, "
            "and prioritised recommendations."
        )
        return self.create_task(
            abstract=mission,
            description=description,
            verification=verification,
            callback_url=callback_url,
            source="hexclaw",
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Public — Agent scheduling + direct tool execution (unchanged)
    # ─────────────────────────────────────────────────────────────────────────

    def schedule_agent(self, agent_name: str, task_input: str) -> str:
        """Schedule an agent through Villager's Agent Scheduler."""
        try:
            if VILLAGER_AVAILABLE:
                with global_llm():
                    return agent_scheduler(
                        agent_entry=tool_villager,
                        agent_name=agent_name,
                        input=task_input,
                    )
            return f"Agent '{agent_name}' cannot run (Villager not available): {task_input}"
        except Exception as exc:
            logger.error(f"Agent scheduling failed: {exc}")
            return f"Agent scheduling failed: {exc}"

    def execute_tool(self, tool_name: str, parameters: dict) -> Any:
        """Execute a Villager core tool by name."""
        if not VILLAGER_AVAILABLE or not self.tools_manager:
            return f"Villager not available — cannot execute tool: {tool_name}"
        try:
            if tool_name == "pyeval":
                code = parameters.get("python_codeblock", "")
                if not code:
                    return "No Python code provided"
                if isinstance(code, str) and "\\n" in code:
                    code = code.replace("\\n", "\n")
                return pyeval(code)

            elif tool_name == "os_execute_cmd":
                return os_execute_cmd(parameters.get("system_command", ""))

            elif tool_name == "tool_villager":
                return tool_villager(
                    agent_name=parameters.get("agent_name", "实用的助手"),
                    **{k: v for k, v in parameters.items() if k != "agent_name"},
                )

            elif tool_name == "github_tools" and self.github_tools:
                method = parameters.get("method", "")
                if not method:
                    return "No GitHub method specified"
                params = {k: v for k, v in parameters.items() if k != "method"}
                if hasattr(self.github_tools, method):
                    return getattr(self.github_tools, method)(**params)
                return f"Unknown GitHub method: {method}"

            return f"Unknown tool: {tool_name}"

        except Exception as exc:
            msg = f"Tool execution failed: {exc}"
            if VISUALS_AVAILABLE:
                print(create_error_message(msg), file=sys.stderr)
            logger.error(msg)
            return msg

    def list_available_tools(self) -> List[dict]:
        if not VILLAGER_AVAILABLE or not self.tools_manager:
            return []
        return self.tools_manager.list_func_json()

    def get_system_status(self) -> dict:
        all_tasks = _list()
        return {
            "villager_available": VILLAGER_AVAILABLE,
            "villager_status": "running" if VILLAGER_AVAILABLE else "not_available",
            "task_store": "sqlite" if TASK_STORE_AVAILABLE else "memory",
            "hexstrike_url": HEXSTRIKE_MCP_URL,
            "task_summary": {
                "total":     len(all_tasks),
                "pending":   sum(1 for t in all_tasks if t.get("status") == "pending"),
                "running":   sum(1 for t in all_tasks if t.get("status") == "running"),
                "completed": sum(1 for t in all_tasks if t.get("status") == "completed"),
                "failed":    sum(1 for t in all_tasks if t.get("status") == "failed"),
            },
            "mcp_client": {
                "base_url": self.mcp_client_base_url,
                "status": "connected" if VILLAGER_AVAILABLE else "not_available",
            },
            "tools_manager": {
                "registered": len(self.tools_manager.list_func()) if self.tools_manager else 0,
            },
            "llm": {
                "model":    Master.get("default_model") if VILLAGER_AVAILABLE else "not_available",
                "base_url": Master.get("openai_api_endpoint") if VILLAGER_AVAILABLE else "not_available",
            },
        }


# ─────────────────────────────────────────────────────────────────────────────
# MCP server construction
# ─────────────────────────────────────────────────────────────────────────────

def build_server() -> Server:
    server  = Server("villager_proper")
    villager = VillagerProperMCP()

    if VISUALS_AVAILABLE:
        try:
            from villager_visuals import create_integrated_banner, create_startup_message, create_info_message
            print(create_integrated_banner(), file=sys.stderr)
            print(create_startup_message(), file=sys.stderr)
            print(create_info_message("MCP Server ready — Hexclaw integration build"), file=sys.stderr)
        except Exception:
            pass

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            # ── HIGH LEVEL: Hexclaw fire-and-forget ──────────────────────────
            Tool(
                name="create_mission",
                description=(
                    "HIGH-LEVEL HEXCLAW ENTRY POINT. Submit a complete attack mission for "
                    "fully autonomous execution by Villager's LLM. Villager decomposes the "
                    "mission into phases, selects HexStrike/Kali Driver tools, executes them "
                    "in a reasoning loop, and returns a consolidated findings report. "
                    "Returns task_id immediately — fire and forget. "
                    "Results delivered via callback_url webhook or polled with get_task_status."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "mission": {
                            "type": "string",
                            "description": (
                                "High-level attack objective. Example: "
                                "'Perform full recon on 10.0.0.0/24, identify exploitable services, "
                                "and attempt initial access'"
                            ),
                        },
                        "target_scope": {
                            "type": "string",
                            "description": "Target IP range, CIDR, domain, or URL",
                        },
                        "constraints": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": (
                                "Rules of engagement. Example: "
                                "['no destructive payloads', 'avoid host 10.0.0.1', "
                                "'recon only — no exploitation']"
                            ),
                        },
                        "callback_url": {
                            "type": "string",
                            "description": "Hexclaw webhook URL. Villager POSTs results here on completion.",
                        },
                    },
                    "required": ["mission", "target_scope"],
                },
            ),

            # ── GRANULAR TASK ─────────────────────────────────────────────────
            Tool(
                name="create_task",
                description=(
                    "Create a granular task using Villager's TaskNode / LLM architecture. "
                    "The LLM reasons about the task and calls HexStrike / Kali Driver tools "
                    "autonomously until the verification criteria are met. "
                    "Returns task_id immediately (async). "
                    "For high-level Hexclaw objectives prefer create_mission."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "abstract":      {"type": "string", "description": "One-line task summary"},
                        "description":   {"type": "string", "description": "Detailed task description"},
                        "verification":  {
                            "type": "string",
                            "description": "Success criteria / what done looks like",
                            "default": "Task completed successfully",
                        },
                        "callback_url": {
                            "type": "string",
                            "description": "Optional webhook URL to POST on completion",
                        },
                        "source": {
                            "type": "string",
                            "description": "Caller identifier: 'hexclaw' | 'cursor' | 'unknown'",
                            "default": "unknown",
                        },
                    },
                    "required": ["abstract", "description"],
                },
            ),

            Tool(
                name="get_task_status",
                description="Poll task status and result by task_id",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "task_id returned by create_task or create_mission",
                        },
                    },
                    "required": ["task_id"],
                },
            ),

            Tool(
                name="list_tasks",
                description=(
                    "List tasks with optional filters. "
                    "Use source='hexclaw' to see only Hexclaw-originated tasks."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "Filter by caller: 'hexclaw' | 'cursor' | 'unknown'",
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status: 'pending' | 'running' | 'completed' | 'failed'",
                        },
                    },
                },
            ),

            # ── AGENT ORCHESTRATION ───────────────────────────────────────────
            Tool(
                name="schedule_agent",
                description="Schedule a named agent through Villager's Agent Scheduler with LLM orchestration",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string", "description": "Agent name"},
                        "task_input": {"type": "string", "description": "Agent task input"},
                    },
                    "required": ["agent_name", "task_input"],
                },
            ),

            # ── DIRECT TOOL EXECUTION ─────────────────────────────────────────
            Tool(
                name="execute_tool",
                description=(
                    "Execute a Villager core tool directly: "
                    "pyeval (run Python), os_execute_cmd (shell command), "
                    "tool_villager (LLM agent), github_tools (GitHub API)"
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tool_name": {
                            "type": "string",
                            "description": "pyeval | os_execute_cmd | tool_villager | github_tools",
                        },
                        "parameters": {
                            "type": "object",
                            "description": "Tool-specific parameters",
                            "additionalProperties": True,
                        },
                    },
                    "required": ["tool_name", "parameters"],
                },
            ),

            Tool(
                name="list_available_tools",
                description="List tools registered in Villager's Tools Manager",
                inputSchema={"type": "object", "properties": {}},
            ),

            # ── SYSTEM ────────────────────────────────────────────────────────
            Tool(
                name="get_system_status",
                description="Health snapshot: Villager availability, task counts, LLM config, HexStrike URL",
                inputSchema={"type": "object", "properties": {}},
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Dispatch MCP tool calls to VillagerProperMCP methods."""
        try:
            # ── Mission ───────────────────────────────────────────────────────
            if name == "create_mission":
                mission      = arguments.get("mission", "")
                target_scope = arguments.get("target_scope", "")
                constraints  = arguments.get("constraints", [])
                callback_url = arguments.get("callback_url")

                if VISUALS_AVAILABLE:
                    print(create_agent_message(f"Mission received from Hexclaw: {mission[:80]}"), file=sys.stderr)

                task_id = villager.create_mission(mission, target_scope, constraints, callback_url)
                return [TextContent(type="text", text=json.dumps({
                    "success":            True,
                    "task_id":            task_id,
                    "message":            f"Mission submitted for autonomous execution",
                    "status":             "pending",
                    "callback_configured": callback_url is not None,
                    "poll_with":          f"get_task_status(task_id='{task_id}')",
                }, ensure_ascii=False, indent=2))]

            # ── Task management ───────────────────────────────────────────────
            elif name == "create_task":
                task_id = villager.create_task(
                    abstract     = arguments.get("abstract", ""),
                    description  = arguments.get("description", ""),
                    verification = arguments.get("verification", "Task completed successfully"),
                    callback_url = arguments.get("callback_url"),
                    source       = arguments.get("source", "unknown"),
                )
                if VISUALS_AVAILABLE:
                    print(create_success_message(f"Task created: {task_id}"), file=sys.stderr)
                return [TextContent(type="text", text=json.dumps({
                    "success": True,
                    "task_id": task_id,
                    "status":  "pending",
                    "message": "Task queued for Villager TaskNode execution",
                }, ensure_ascii=False, indent=2))]

            elif name == "get_task_status":
                result = villager.get_task_status(arguments.get("task_id", ""))
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

            elif name == "list_tasks":
                result = villager.list_tasks(
                    source=arguments.get("source"),
                    status=arguments.get("status"),
                )
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

            # ── Agent ─────────────────────────────────────────────────────────
            elif name == "schedule_agent":
                response = villager.schedule_agent(
                    arguments.get("agent_name", ""),
                    arguments.get("task_input", ""),
                )
                return [TextContent(type="text", text=json.dumps({
                    "success": True,
                    "agent_name": arguments.get("agent_name"),
                    "response": response,
                }, ensure_ascii=False, indent=2))]

            # ── Tool execution ────────────────────────────────────────────────
            elif name == "execute_tool":
                result = villager.execute_tool(
                    arguments.get("tool_name", ""),
                    arguments.get("parameters", {}),
                )
                return [TextContent(type="text", text=json.dumps(
                    {"result": result}, ensure_ascii=False, indent=2
                ))]

            elif name == "list_available_tools":
                return [TextContent(type="text", text=json.dumps(
                    villager.list_available_tools(), ensure_ascii=False, indent=2
                ))]

            # ── System ────────────────────────────────────────────────────────
            elif name == "get_system_status":
                return [TextContent(type="text", text=json.dumps(
                    villager.get_system_status(), ensure_ascii=False, indent=2
                ))]

            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as exc:
            logger.exception(f"Tool error in '{name}'")
            return [TextContent(type="text", text=f"Error: {exc}")]

    return server


# ─────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ─────────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Villager MCP Server — Hexclaw integration build")
    p.add_argument("--debug", action="store_true", help="Enable DEBUG logging")
    return p.parse_args()


async def run() -> None:
    args = parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    print("""
╔══════════════════════════════════════════════════════════════╗
║       🏘️  VILLAGER MCP — HEXCLAW INTEGRATION BUILD  🏘️      ║
║                                                              ║
║  ✅ TaskNode LLM execution (fire-and-forget)                ║
║  ✅ HexStrike tool context injected into every task         ║
║  ✅ SQLite persistent task store                             ║
║  ✅ Webhook callbacks for Hexclaw                            ║
║  ✅ create_mission() — high-level Hexclaw entry point        ║
║  ✅ list_tasks(source='hexclaw') — Hexclaw task history      ║
╚══════════════════════════════════════════════════════════════╝
""", file=sys.stderr)
    logger.info(f"Villager available : {VILLAGER_AVAILABLE}")
    logger.info(f"Task store         : {'SQLite' if TASK_STORE_AVAILABLE else 'in-memory'}")
    logger.info(f"HexStrike URL      : {HEXSTRIKE_MCP_URL}")

    server = build_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(run())
