# Villager AI Debug & Orchestration Guide

## 🚨 Critical Fix: MCP Tool Loading Order

**Problem**: HexStrike has ~150+ tools which overwhelms Cursor's MCP loading, preventing Villager tools from being visible.

**Solution**: Put Villager FIRST in your MCP config and ensure proper PYTHONPATH.

### Fixed MCP Configuration

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
1. **Villager comes FIRST** - This ensures Cursor loads Villager tools before hitting the tool limit
2. **PYTHONPATH is set** - Points to Villager repo root for proper module resolution
3. **HexStrike port is 8000** - Not 8888 as some configs show

## 🔍 Debugging Villager

### Debug Flags & Environment Variables

```bash
# Villager HTTP MCP Server
export VILLAGER_DEBUG=1
export PYTHONUNBUFFERED=1
export PYTHONPATH=/path/to/your/Villager-AI

# Start with verbose logging
python mcp/villager_http_mcp.py --server http://127.0.0.1:37695
```

### Log Locations

- **Villager MCP Logs**: Check Cursor's MCP output in the developer console
- **Villager Server Logs**: `villager_server.py` outputs to stdout/stderr
- **HexStrike Logs**: `/home/yenn/hexstrike-ai/hexstrike_mcp.log`

### Debug Commands

```python
# Test Villager MCP connection
mcp_villager_get_status()

# Test HexStrike connection via Villager
mcp_villager_execute_python(
    code="import requests; print(requests.get('http://localhost:8000/health').json())"
)

# Check available tools
mcp_villager_list_agents()
```

## 📡 Villager HTTP MCP API Schema

### Available Endpoints

| Endpoint | Method | Description | Payload |
|----------|--------|-------------|---------|
| `/api/status` | GET | Server status | None |
| `/api/agents/create` | POST | Create agent | `{"name": "string", "task": "string"}` |
| `/api/agents` | GET | List agents | None |
| `/api/scans/run` | POST | Run scan | `{"target": "string", "scan_type": "string"}` |
| `/api/scans` | GET | List scans | None |
| `/api/exec/shell` | POST | Execute shell | `{"cmd": "string", "timeout": int, "cwd": "string", "env": {}}` |
| `/api/exec/python` | POST | Execute Python | `{"code": "string", "timeout": int}` |

### Typical Responses

```json
// Agent Creation Response
{
  "success": true,
  "agent_id": "agent_12345",
  "message": "Agent created successfully",
  "status": "pending"
}

// Status Response
{
  "status": "running",
  "agents": 2,
  "scans": 1,
  "server_time": "2024-01-15T10:30:00Z"
}

// Error Response
{
  "success": false,
  "error": "Agent name already exists",
  "code": "AGENT_EXISTS"
}
```

## ⏱️ Timeouts & Rate Limits

### Recommended Timeouts

```json
{
  "mcp_timeout": 300,        // 5 minutes for MCP operations
  "agent_timeout": 3600,     // 1 hour for agent tasks
  "scan_timeout": 1800,      // 30 minutes for scans
  "exec_timeout": 120        // 2 minutes for shell/Python execution
}
```

### Rate Limiting Best Practices

1. **Agent Creation**: Max 5 concurrent agents
2. **Scan Execution**: Max 3 concurrent scans
3. **Shell Commands**: 10 requests/minute per agent
4. **Python Execution**: 20 requests/minute per agent

### Monitoring Agent Lifecycle

```python
# Check agent status
mcp_villager_list_agents()

# Monitor specific agent
mcp_villager_execute_python(
    code="""
import requests
response = requests.get('http://127.0.0.1:37695/api/agents')
agents = response.json()
for agent in agents.get('agents', []):
    print(f"Agent {agent['name']}: {agent['status']}")
"""
)
```

## 🎯 Tool Orchestration Strategy

### Recommended Split

| Tool Category | Use Case | Tool Set |
|---------------|----------|----------|
| **Fast Reconnaissance** | Quick scans, port discovery | HexStrike tools |
| **Complex Analysis** | Multi-step penetration testing | Villager agents |
| **One-off Commands** | Single tool execution | HexStrike tools |
| **Long-running Tasks** | Comprehensive assessments | Villager agents |

### Orchestration Patterns

#### Pattern 1: HexStrike → Villager Pipeline
```python
# 1. Quick recon with HexStrike
mcp_hexstrike-ai_nmap_scan(target="192.168.1.1")

# 2. Create Villager agent for deep analysis
mcp_villager_create_agent(
    name="Deep_Analysis_Agent",
    task="Based on nmap results, perform comprehensive penetration testing including vulnerability assessment, exploitation attempts, and detailed reporting."
)
```

#### Pattern 2: Villager Agent Orchestration
```python
# Create specialized agents for different phases
mcp_villager_create_agent(
    name="Recon_Agent",
    task="Perform initial reconnaissance: subdomain enumeration, port scanning, service detection"
)

mcp_villager_create_agent(
    name="Vuln_Agent", 
    task="Analyze discovered services for vulnerabilities and create exploitation plan"
)

mcp_villager_create_agent(
    name="Report_Agent",
    task="Compile findings from all agents into comprehensive penetration test report"
)
```

#### Pattern 3: Hybrid Approach
```python
# Use HexStrike for immediate results
mcp_hexstrike-ai_httpx_probe(target="https://target.com")

# Use Villager for complex workflows
mcp_villager_create_agent(
    name="Web_App_Agent",
    task="Perform comprehensive web application security assessment including OWASP Top 10 testing, authentication bypass attempts, and business logic testing"
)
```

## 🚀 Quick Start Workflow

1. **Start Servers**:
   ```bash
   # Terminal 1: HexStrike
   cd /path/to/your/hexstrike-ai
   source hexstrike-env/bin/activate
   python hexstrike_server.py --port 8000 --debug
   
   # Terminal 2: Villager
   cd /path/to/your/Villager-AI
   source villager-venv-new/bin/activate
   python villager_server.py
   ```

2. **Update MCP Config**: Copy the fixed config above to `~/.cursor/mcp.json`

3. **Restart Cursor**: Reload window to pick up new MCP configuration

4. **Test Connection**:
   ```python
   mcp_villager_get_status()
   mcp_hexstrike-ai_execute_python_script(script="print('HexStrike connected')")
   ```

5. **Create Your First Agent**:
   ```python
   mcp_villager_create_agent(
       name="Bug_Bounty_Agent",
       task="Perform comprehensive bug bounty assessment on target.com. Include: 1) Subdomain enumeration, 2) Port scanning, 3) Web application testing, 4) API security assessment, 5) Generate detailed report with findings and recommendations."
   )
   ```

## 🎥 For Content Creators

### Screen Recording Tips

1. **Show the MCP config first** - Demonstrate the tool order fix
2. **Test both tool sets** - Show Villager and HexStrike working together
3. **Create a real agent** - Use a live target (with permission)
4. **Show monitoring** - Demonstrate agent status checking
5. **Highlight the hybrid approach** - Fast tools + autonomous agents

### Key Points to Emphasize

- **Tool loading order matters** - Villager must come first
- **PYTHONPATH is critical** - Without it, Villager tools fail
- **Hybrid approach is powerful** - Fast scans + autonomous analysis
- **Real-world applicability** - This isn't just a demo, it's production-ready

## 🔧 Troubleshooting

### Common Issues

1. **"Tool not found" errors**: Check MCP config order and restart Cursor
2. **"Not connected" errors**: Verify server ports (8000 for HexStrike, 37695 for Villager)
3. **Python import errors**: Ensure PYTHONPATH is set correctly
4. **Agent creation fails**: Check Villager server is running and accessible

### Debug Commands

```python
# Check server status
mcp_villager_get_status()

# Test Python execution
mcp_villager_execute_python(code="import sys; print(sys.path)")

# List available agents
mcp_villager_list_agents()
```

This setup provides a powerful, scalable framework for automated security testing with both immediate tool access and autonomous agent capabilities.
