#!/usr/bin/env python3
"""
Simple MCP Service for Villager
This service acts as the MCP Client that Villager expects to be running on port 25989
"""

import json
import asyncio
import uvicorn
import io
import re
import requests
import sys
import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# Force UTF-8 for standard output on Windows to avoid print crashes
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = FastAPI(title="Villager MCP Service")

@app.post("/")
async def mcp_request(request: Request):
    """Handle MCP requests from Villager with proper streaming response format"""
    try:
        try:
            body = await request.json()
        except Exception as je:
            print(f"JSON Parse Error: {je}")
            # Try to get raw body if JSON fails
            raw_body = await request.body()
            print(f"Raw body snippet: {raw_body[:200]}")
            body = {"prompt": str(raw_body)}
            
        prompt = body.get("prompt", "")
        mcp_servers = body.get("mcp_servers")
        if not isinstance(mcp_servers, dict):
            mcp_servers = {}
        
        # Safely print for debugging
        print("--- New MCP Request ---")
        try:
            print(f"Prompt (start): {prompt[:100]}")
        except:
            print("Prompt contains unprintable characters")
        
        # Extract actual command if it's in the "Execute tool 'X' on input: Y" format
        # This regex is robust against the Chinese wrapping and extra context
        cmd_match = re.search(r"Execute tool '([^']+)' on input: ([^\s!?,]+)", prompt)
        if cmd_match:
            tool_name = cmd_match.group(1).lower()
            target = cmd_match.group(2)
            print(f"Detected Tool: {tool_name}, Target: {target}")
            
            # Extract extra params if present (before tool-specific blocks)
            params_match = re.search(r"Extra params: ({.+})", prompt)
            params = {}
            if params_match:
                try:
                    params = json.loads(params_match.group(1))
                except: pass
            
            # Simple translation for common tools
            if tool_name == "amass":
                mode = params.get("mode", "passive")
                resolvers = params.get("resolvers")
                max_time = params.get("max_time")
                
                cmd_parts = ["amass enum"]
                if mode == "passive":
                    cmd_parts.append("-passive")
                cmd_parts.append(f"-d {target}")
                if resolvers:
                    cmd_parts.append(f"-rf {resolvers}")
                if max_time:
                    cmd_parts.append(f"-max-time {max_time}")
                prompt = " ".join(cmd_parts)
            elif tool_name == "nmap":
                scan_type = params.get("scan_type", "-sV")
                ports = params.get("ports")
                cmd_parts = ["nmap", scan_type]
                if ports:
                    cmd_parts.append(f"-p {ports}")
                cmd_parts.append(target)
                prompt = " ".join(cmd_parts)
            elif tool_name == "subfinder":
                recursive = params.get("recursive", False)
                cmd_parts = ["subfinder", "-d", target]
                if recursive:
                    cmd_parts.append("-recursive")
                prompt = " ".join(cmd_parts)
            elif tool_name == "rustscan":
                ports = params.get("ports")
                cmd_parts = ["rustscan_fast_scan"]
                if ports:
                    cmd_parts.append(f"-p {ports}")
                cmd_parts.append(target)
                prompt = " ".join(cmd_parts)
            elif tool_name == "gobuster":
                wordlist = params.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
                threads = params.get("threads", 50)
                prompt = f"gobuster_scan {target} -w {wordlist} -t {threads}"
            
            print(f"Translated command: {prompt}")

        def generate_response():
            try:
                # Decide routing
                lower_prompt = prompt.lower()
                is_security_tool = any(k in lower_prompt for k in ["msfvenom", "payload", "kali", "amass", "nmap", "scan", "recon", "subfinder", "rustscan", "gobuster"])
                is_browser = any(k in lower_prompt for k in ["browser", "web", "scrape", "search"])
                
                if is_security_tool:
                    kali_url = mcp_servers.get("kali_driver", "http://127.0.0.1:1611")
                    try:
                        # Increased timeout to 300s for heavy tools
                        resp = requests.post(f"{kali_url}/", json={"prompt": prompt}, timeout=300)
                        resp.raise_for_status()
                        result = resp.json()
                        content = result.get("content", str(result))
                        
                        # Correct sequence for scheduler's McpClient:
                        # 1. Start message (clear buffer)
                        yield f'{{"new_msg": true}}\n'
                        # 2. Yield content
                        yield f'{{"content": {json.dumps(content)}}}\n'
                        # 3. Mark as done
                        yield f'{{"done": true}}\n'
                    except Exception as e:
                        print(f"Kali Driver error: {e}")
                        yield f'{{"new_msg": true}}\n'
                        yield f'{{"content": {json.dumps(f"Kali Driver error: {str(e)}")}}}\n'
                        yield f'{{"done": true}}\n'
                
                elif is_browser:
                    browser_url = mcp_servers.get("browser_use", "http://127.0.0.1:8080")
                    try:
                        resp = requests.post(f"{browser_url}/", json={"prompt": prompt}, timeout=120)
                        resp.raise_for_status()
                        result = resp.json()
                        content = result.get("content", str(result))
                        
                        yield f'{{"new_msg": true}}\n'
                        yield f'{{"content": {json.dumps(content)}}}\n'
                        yield f'{{"done": true}}\n'
                    except Exception as e:
                        print(f"Browser service error: {e}")
                        yield f'{{"new_msg": true}}\n'
                        yield f'{{"content": {json.dumps(f"Browser service error: {str(e)}")}}}\n'
                        yield f'{{"done": true}}\n'
                
                else:
                    if "Execute task:" in prompt or len(prompt) > 500:
                        yield f'{{"new_msg": true}}\n'
                        yield f'{{"content": "Acknowledge task: {json.dumps(prompt[:50])}..."}}\n'
                        yield f'{{"done": true}}\n'
                    else:
                        # Fallback to local subprocess
                        try:
                            import subprocess
                            proc = subprocess.run(prompt, shell=True, capture_output=True, text=True, timeout=60)
                            out = f"STDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
                            yield f'{{"new_msg": true}}\n'
                            yield f'{{"content": {json.dumps(out)}}}\n'
                            yield f'{{"done": true}}\n'
                        except Exception as e:
                            yield f'{{"new_msg": true}}\n'
                            yield f'{{"content": {json.dumps(f"Local exec error: {str(e)}")}}}\n'
                            yield f'{{"done": true}}\n'
            except Exception as inner_e:
                yield f'{{"content": {json.dumps(f"Generator Error: {str(inner_e)}")}, "new_msg": true}}\n'
                yield f'{{"done": true}}\n'

        return StreamingResponse(generate_response(), media_type="text/plain")
        
    except Exception as e:
        print(f"Top-level mcp_request Error: {e}")
        # Return a 200 with an error object instead of 500 to let Villager handle it
        async def err_stream():
            yield f'{{"content": {json.dumps(f"Service Error: {str(e)}")}, "new_msg": true}}\n'
            yield f'{{"done": true}}\n'
        return StreamingResponse(err_stream(), media_type="text/plain")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mcp_client"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=25989)
