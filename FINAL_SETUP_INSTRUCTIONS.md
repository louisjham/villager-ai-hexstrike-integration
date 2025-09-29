# 🚨 FINAL SETUP INSTRUCTIONS - Villager MCP Tool Loading Fix

## Prerequisites
Before starting, make sure you have:
- Villager-AI installed (cloned from this repository)
- HexStrike-AI installed and configured
- Both virtual environments set up and activated

**Find Your Installation Paths:**
- Villager-AI path: Where you cloned this repository (e.g., `/home/username/Villager-AI`)
- HexStrike-AI path: Where you installed HexStrike (e.g., `/home/username/hexstrike-ai`)
- Replace `/path/to/your/` in the examples below with your actual paths

## The Problem
HexStrike has 69+ tools which overwhelms Cursor's MCP loading capacity, preventing Villager tools from appearing. You can see this in the available tools list - only HexStrike tools are visible.

## The Solution
1. **Put Villager FIRST** in MCP config
2. **Set proper PYTHONPATH**
3. **Start Villager MCP server**
4. **Restart Cursor**

## Step-by-Step Fix

### 1. Update Your MCP Configuration

Copy this to `~/.cursor/mcp.json` (replace the paths with your actual installation paths):

```json
{
  "mcpServers": {
    "villager": {
      "command": "/path/to/your/Villager-AI/villager-venv-new/bin/python3",
      "args": [
        "/path/to/your/Villager-AI/mcp/villager_http_mcp.py",
        "--server",
        "http://127.0.0.1:37695"
      ],
      "description": "Villager AI Framework - Autonomous Penetration Testing with Agent Management",
      "timeout": 300,
      "alwaysAllow": [],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "PYTHONPATH": "/path/to/your/Villager-AI"
      }
    },
    "hexstrike-ai": {
      "command": "/path/to/your/hexstrike-ai/hexstrike-env/bin/python3",
      "args": [
        "/path/to/your/hexstrike-ai/hexstrike_mcp.py",
        "--server",
        "http://localhost:8000",
        "--debug"
      ],
      "description": "HexStrike AI v6.0 - Advanced Cybersecurity Automation Platform. Turn off alwaysAllow if you dont want autonomous execution!",
      "timeout": 300,
      "alwaysAllow": []
    }
  }
}
```

**Key Points**:
- `villager` comes BEFORE `hexstrike-ai`
- `PYTHONPATH` points to Villager repo root
- HexStrike server port is 8000 (not 8888)

### 2. Start Both Servers

**Terminal 1 - HexStrike Server**:
```bash
cd /path/to/your/hexstrike-ai
source hexstrike-env/bin/activate
python hexstrike_server.py --port 8000 --debug
```

**Terminal 2 - Villager Server**:
```bash
cd /path/to/your/Villager-AI
source villager-venv-new/bin/activate
python villager_server.py
```

### 3. Restart Cursor

1. Close Cursor completely
2. Reopen Cursor
3. Wait for MCP servers to initialize

### 4. Test the Fix

After restart, you should see Villager tools in the available tools list:

- `mcp_villager_get_status`
- `mcp_villager_create_agent`
- `mcp_villager_list_agents`
- `mcp_villager_execute_shell`
- `mcp_villager_execute_python`
- etc.

### 5. Create Your First Agent

```python
mcp_villager_create_agent(
    name="Bug_Bounty_Agent",
    task="Perform comprehensive bug bounty assessment on target.com. Include: 1) Subdomain enumeration, 2) Port scanning, 3) Web application testing, 4) API security assessment, 5) Generate detailed report with findings and recommendations."
)
```

## Why This Works

1. **Tool Loading Order**: Cursor loads MCP servers in order. By putting Villager first, it gets loaded before hitting the tool limit.

2. **PYTHONPATH**: Villager needs this to find its modules properly.

3. **Server Ports**: HexStrike runs on 8000, Villager on 37695.

## Troubleshooting

If Villager tools still don't appear:

1. **Check MCP config syntax**: Validate JSON at jsonlint.com
2. **Verify server status**: Both servers should be running
3. **Check logs**: Look for MCP connection errors in Cursor
4. **Try minimal config**: Start with just Villager, then add HexStrike

## Alternative: Use HexStrike to Talk to Villager

If MCP loading still fails, you can use HexStrike's `execute_python_script` to communicate with Villager:

```python
mcp_hexstrike-ai_execute_python_script(
    script="""
import requests
import json

# Create a Villager agent
response = requests.post('http://127.0.0.1:37695/api/agents/create', 
    json={'name': 'Test_Agent', 'task': 'Test task'})
print(response.json())
"""
)
```

This hybrid approach gives you access to both tool sets even if MCP loading is problematic.

## Success Indicators

✅ You should see Villager tools in the available tools list  
✅ `mcp_villager_get_status()` works  
✅ `mcp_villager_create_agent()` works  
✅ Both HexStrike and Villager tools are available  

The key insight from the user's message is that **tool loading order matters** - Villager must come first to be visible in Cursor's MCP interface.
