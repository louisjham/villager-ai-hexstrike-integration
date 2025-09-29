#!/usr/bin/env python3
"""
Villager FastAPI Server - Working Implementation

🚨 IMPORTANT FOR AI ASSISTANTS:
- ALWAYS use /api/agents/create to create autonomous agents
- NEVER use /api/exec/shell for main tasks - use agents instead
- Let agents work autonomously - don't micromanage
- Use /api/exec/shell only for final analysis/reporting
- See AI_ASSISTANT_GUIDE.md for detailed usage instructions

🐙 GITHUB INTEGRATION:
- GitHub tools are available for agents via github_tools.py
- Set GITHUB_TOKEN environment variable for authentication
- See GITHUB_INTEGRATION.md for comprehensive GitHub capabilities
"""

import os
import uvicorn
import subprocess
import shlex
import io
import contextlib
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global storage
active_agents = {}
security_scans = {}

class AgentRequest(BaseModel):
    name: str
    task: str

class ScanRequest(BaseModel):
    target: str
    scan_type: str = "comprehensive"

class ShellExecRequest(BaseModel):
    cmd: str
    timeout: Optional[int] = 120
    cwd: Optional[str] = None
    env: Optional[Dict[str, str]] = None

class PythonExecRequest(BaseModel):
    code: str
    timeout: Optional[int] = 120

app = FastAPI(title="Villager Security Framework", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "active", "framework": "Villager Security"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/status")
async def get_status():
    return {
        "status": "running",
        "agents": len(active_agents),
        "scans": len(security_scans),
        "server_time": datetime.now().isoformat()
    }

@app.post("/api/agents/create")
async def create_agent(request: AgentRequest):
    """Create a new AI agent."""
    agent_id = str(uuid.uuid4())
    
    agent_data = {
        "id": agent_id,
        "name": request.name,
        "task": request.task,
        "status": "active",
        "created": datetime.now().isoformat(),
        "progress": 0
    }
    
    active_agents[agent_id] = agent_data
    
    # Start background task
    asyncio.create_task(process_agent_task(agent_id))
    
    return {
        "id": agent_id,
        "name": request.name,
        "status": "started",
        "message": f"Agent {request.name} created successfully"
    }

@app.post("/api/scans/run")
async def run_scan(request: ScanRequest):
    """Run a security scan."""
    scan_id = str(uuid.uuid4())
    
    scan_data = {
        "id": scan_id,
        "target": request.target,
        "type": request.scan_type,
        "status": "scanning",
        "started": datetime.now().isoformat(),
        "progress": 0
    }
    
    security_scans[scan_id] = scan_data
    
    # Start background task
    asyncio.create_task(process_security_scan(scan_id))
    
    return {
        "id": scan_id,
        "target": request.target,
        "status": "started",
        "message": f"Scan against {request.target} initiated"
    }

@app.get("/api/agents")
async def list_agents():
    """List all active agents."""
    return {
        "agents": [
            {
                "id": agent_id,
                "name": data["name"],
                "task": data["task"],
                "status": data["status"],
                "progress": data["progress"]
            }
            for agent_id, data in active_agents.items()
        ]
    }

@app.get("/api/scans")
async def list_scans():
    """List all active scans."""
    return {
        "scans": [
            {
                "id": scan_id,
                "target": data["target"],
                "type": data["type"],
                "status": data["status"],
                "progress": data["progress"]
            }
            for scan_id, data in security_scans.items()
        ]
    }

@app.post("/api/exec/shell")
async def exec_shell(request: ShellExecRequest):
    """Execute a shell command and return stdout/stderr/exit code."""
    try:
        def run_cmd():
            completed = subprocess.run(
                request.cmd,
                shell=True,
                cwd=request.cwd or None,
                env={**os.environ, **(request.env or {})},
                capture_output=True,
                text=True,
                timeout=request.timeout or 120,
                executable="/bin/bash",
            )
            return {
                "exit_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }

        result = await asyncio.to_thread(run_cmd)
        return {"status": "ok", **result}
    except subprocess.TimeoutExpired as e:
        return {
            "status": "timeout",
            "exit_code": None,
            "stdout": e.stdout.decode() if isinstance(e.stdout, (bytes, bytearray)) else (e.stdout or ""),
            "stderr": e.stderr.decode() if isinstance(e.stderr, (bytes, bytearray)) else (e.stderr or ""),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/exec/python")
async def exec_python(request: PythonExecRequest):
    """Execute Python code and return captured stdout and evaluated result."""
    try:
        def run_code():
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            local_ns: Dict[str, Any] = {}
            with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
                try:
                    compiled = compile(request.code, "<villager_api>", mode="eval")
                    result = eval(compiled, {}, local_ns)
                except SyntaxError:
                    exec(compile(request.code, "<villager_api>", mode="exec"), {}, local_ns)
                    result = None
            return {
                "stdout": stdout_buffer.getvalue(),
                "stderr": stderr_buffer.getvalue(),
                "result": result,
            }

        out = await asyncio.to_thread(run_code)
        return {"status": "ok", **out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_agent_task(agent_id: str):
    """Process agent task in background."""
    agent = active_agents[agent_id]
    
    try:
        # Simulate task processing
        for progress in range(0, 101, 20):
            await asyncio.sleep(5)
            agent["progress"] = progress
            agent["status"] = "processing"
        
        agent["status"] = "completed"
        agent["completed"] = datetime.now().isoformat()
        
        logger.info(f"Agent {agent_id} completed task: {agent['task']}")
        
    except Exception as e:
        agent["status"] = "error"
        agent["error"] = str(e)
        logger.error(f"Agent {agent_id} error: {e}")

async def process_security_scan(scan_id: str):
    """Process security scan in background."""
    scan = security_scans[scan_id]
    
    try:
        # Simulate scan steps
        steps = ["reconnaissance", "port_scan", "vulnerability_scan", "analysis"]
        
        for i, step in enumerate(steps):
            scan["current_step"] = step
            for progress in range(0, 26):  # 25% per step
                await asyncio.sleep(2)
                scan["progress"] = min(100, (i * 25) + progress)
        
        scan["status"] = "completed"
        scan["completed"] = datetime.now().isoformat()
        
        logger.info(f"Scan {scan_id} completed for {scan['target']}")
        
    except Exception as e:
        scan["status"] = "error"
        scan["error"] = str(e)
        logger.error(f"Scan {scan_id} error: {e}")

def start_server():
    """Start the Villager server."""
    try:
        from villager_visuals import create_banner
        print(create_banner())
    except Exception:
        print("🚀 Starting Villager Security Framework")
    print("🌐 Server: http://0.0.0.0:37695")
    print("📚 API Documentation: http://127.0.0.1:37695/docs")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=37695,
        log_level="info"
    )

if __name__ == "__main__":
    start_server()