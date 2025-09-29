# AI Assistant Guide: How to Use Villager-AI Framework

## 🚨 CRITICAL: Use Villager MCP Tools (Now Available!)

**IMPORTANT**: When working with Villager-AI, AI assistants should use:
1. **Villager MCP tools** - `mcp_villager_create_agent`, `mcp_villager_list_agents`, etc. (NOW AVAILABLE!)
2. **Fallback**: HexStrike MCP tools - `mcp_hexstrike-ai_execute_python_script` for HTTP API calls
3. **NEVER** use direct terminal commands like `curl`, `python`, or shell scripts

**✅ UPDATE**: Villager MCP tools are now working after tool optimization! You can use:
- `mcp_villager_create_agent(name, task)` - Create custom autonomous agents
- `mcp_villager_list_agents()` - List all active agents
- `mcp_villager_get_status()` - Get server status
- And other Villager MCP tools

**Framework Approach**: Villager-AI is a flexible agent framework. You create custom agents by defining their name and detailed task description - no predefined agent types!

## 🔧 REQUIRED SETUP (Start These Servers First)

Before using Villager, you MUST start these servers:

### 1. Start Villager Server
```bash
cd /home/yenn/Villager-AI
source villager-venv-new/bin/activate
python villager_server.py &
```

### 2. Start HexStrike Server
```bash
cd /home/yenn/hexstrike-ai
source hexstrike-env/bin/activate
python hexstrike_server.py --port 8000 --debug &
```

### 3. Start HexStrike MCP Client (CRITICAL)
```bash
cd /home/yenn/hexstrike-ai
source hexstrike-env/bin/activate
python hexstrike_mcp.py --server http://localhost:8000 --debug &
```

**The HexStrike MCP client is ESSENTIAL** - without it, the `mcp_hexstrike-ai_execute_python_script` tool won't work.

## 🚀 NEW: Direct Villager MCP Tools (Recommended)

**✅ Villager MCP tools are now working!** Use these directly instead of the HexStrike workaround:

### Create Custom Agents
```python
# Direct Villager MCP tool (RECOMMENDED)
mcp_villager_create_agent(
    name="Custom_Pentest_Agent",
    task="Perform comprehensive penetration test on target.com. Include: 1) Reconnaissance (subdomain enumeration, port scanning), 2) Vulnerability assessment (Nuclei, SQLMap), 3) Exploitation attempts, 4) Generate detailed report with findings and recommendations."
)
```

### List Active Agents
```python
# Direct Villager MCP tool
mcp_villager_list_agents()
```

### Get Server Status
```python
# Direct Villager MCP tool
mcp_villager_get_status()
```

### Agent Creation Philosophy
- **Custom Agents**: Create agents for any security task you need
- **Detailed Tasks**: Provide comprehensive task descriptions with analysis steps, execution methods, expected outcomes, and reporting requirements
- **No Predefined Types**: Villager is a framework - you define the agent's purpose and capabilities

## 🛠️ Fallback: HexStrike MCP Tools for Villager-AI

### 1. **Agent Management Tools**

#### Create Autonomous Agents
```python
# Use mcp_hexstrike-ai_execute_python_script to create agents
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

# Create an agent
agent_data = {
    "name": "Your_Agent_Name",
    "task": "Detailed task description with analysis steps, execution methods, expected outcomes, and reporting requirements"
}

# Convert data to JSON
json_data = json.dumps(agent_data).encode('utf-8')

# Create request
req = urllib.request.Request(
    "http://127.0.0.1:37695/api/agents/create",
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

# Send request
with urllib.request.urlopen(req, timeout=30) as response:
    if response.status == 200:
        result = json.loads(response.read().decode('utf-8'))
        print("✅ Agent created successfully!")
        print(f"Agent ID: {result.get('id')}")
        print(f"Name: {result.get('name')}")
        print(f"Status: {result.get('status')}")
    else:
        print(f"❌ Failed to create agent: {response.status}")
"""
)
```

#### List Active Agents
```python
# Use mcp_hexstrike-ai_execute_python_script to list agents
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

#### Check Agent Status
```python
# Use mcp_hexstrike-ai_execute_python_script to check specific agent
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

with urllib.request.urlopen("http://127.0.0.1:37695/api/agents", timeout=10) as response:
    if response.status == 200:
        data = json.loads(response.read().decode('utf-8'))
        target_agent = "Your_Agent_Name"
        
        for agent in data.get('agents', []):
            if agent['name'] == target_agent:
                print(f"🎯 Agent: {agent['name']}")
                print(f"   Status: {agent['status']}")
                print(f"   Progress: {agent['progress']}%")
                print(f"   Task: {agent['task'][:100]}...")
                break
        else:
            print(f"❌ Agent '{target_agent}' not found")
    else:
        print(f"❌ Failed to check agents: {response.status}")
"""
)
```

### 2. **Security Scan Tools**

#### Run Security Scans
```python
# Use mcp_hexstrike-ai_execute_python_script to run scans
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

scan_data = {
    "target": "target.com",
    "scan_type": "comprehensive"
}

# Convert data to JSON
json_data = json.dumps(scan_data).encode('utf-8')

# Create request
req = urllib.request.Request(
    "http://127.0.0.1:37695/api/scans/run",
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

# Send request
with urllib.request.urlopen(req, timeout=30) as response:
    if response.status == 200:
        result = json.loads(response.read().decode('utf-8'))
        print("🔍 Security scan initiated!")
        print(f"Scan ID: {result.get('id')}")
        print(f"Target: {result.get('target')}")
        print(f"Status: {result.get('status')}")
    else:
        print(f"❌ Failed to start scan: {response.status}")
"""
)
```

#### List Active Scans
```python
# Use mcp_hexstrike-ai_execute_python_script to list scans
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

with urllib.request.urlopen("http://127.0.0.1:37695/api/scans", timeout=10) as response:
    if response.status == 200:
        data = json.loads(response.read().decode('utf-8'))
        print("🔍 Active Scans:")
        for scan in data.get('scans', []):
            print(f"  • {scan['target']} - {scan['type']} - Status: {scan['status']} - Progress: {scan['progress']}%")
    else:
        print(f"❌ Failed to list scans: {response.status}")
"""
)
```

### 3. **Direct Execution Tools**

#### Execute Shell Commands (Use Sparingly)
```python
# Use mcp_hexstrike-ai_execute_python_script for shell commands
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

cmd_data = {
    "cmd": "nmap -sS target.com",
    "timeout": 120
}

# Convert data to JSON
json_data = json.dumps(cmd_data).encode('utf-8')

# Create request
req = urllib.request.Request(
    "http://127.0.0.1:37695/api/exec/shell",
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

# Send request
with urllib.request.urlopen(req, timeout=150) as response:
    if response.status == 200:
        result = json.loads(response.read().decode('utf-8'))
        print(f"✅ Command executed")
        print(f"Exit Code: {result.get('exit_code')}")
        print(f"Output: {result.get('stdout')}")
        if result.get('stderr'):
            print(f"Errors: {result.get('stderr')}")
    else:
        print(f"❌ Command failed: {response.status}")
"""
)
```

#### Execute Python Code
```python
# Use mcp_hexstrike-ai_execute_python_script for Python execution
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

python_data = {
    "code": "print('Hello from Villager!'); import os; print(f'Current dir: {os.getcwd()}')",
    "timeout": 30
}

# Convert data to JSON
json_data = json.dumps(python_data).encode('utf-8')

# Create request
req = urllib.request.Request(
    "http://127.0.0.1:37695/api/exec/python",
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

# Send request
with urllib.request.urlopen(req, timeout=60) as response:
    if response.status == 200:
        result = json.loads(response.read().decode('utf-8'))
        print(f"✅ Python code executed")
        print(f"Output: {result.get('stdout')}")
        print(f"Result: {result.get('result')}")
        if result.get('stderr'):
            print(f"Errors: {result.get('stderr')}")
    else:
        print(f"❌ Python execution failed: {response.status}")
"""
)
```

### 4. **Server Status and Health**

#### Check Villager Server Status
```python
# Use mcp_hexstrike-ai_execute_python_script to check server status
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

with urllib.request.urlopen("http://127.0.0.1:37695/api/status", timeout=10) as response:
    if response.status == 200:
        status = json.loads(response.read().decode('utf-8'))
        print("🚀 Villager Server Status:")
        print(f"   Status: {status.get('status')}")
        print(f"   Active Agents: {status.get('agents')}")
        print(f"   Active Scans: {status.get('scans')}")
        print(f"   Server Time: {status.get('server_time')}")
    else:
        print(f"❌ Server not responding: {response.status}")
"""
)
```

## 🎯 Pre-built Agent Templates

### Bug Bounty Hunter Agent
```python
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

agent_data = {
    "name": "Bug_Bounty_Hunter_Agent",
    "task": \"\"\"Perform comprehensive bug bounty reconnaissance and vulnerability assessment. 

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
- Compliance with responsible disclosure practices

REPORTING REQUIREMENTS:
- Executive summary of findings
- Technical details for each vulnerability
- Risk assessment and business impact
- Remediation steps and timeline
- Proof-of-concept demonstrations\"\"\"
}

# Convert data to JSON
json_data = json.dumps(agent_data).encode('utf-8')

# Create request
req = urllib.request.Request(
    "http://127.0.0.1:37695/api/agents/create",
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

# Send request
with urllib.request.urlopen(req, timeout=30) as response:
    if response.status == 200:
        result = json.loads(response.read().decode('utf-8'))
        print("✅ Bug Bounty Hunter Agent created successfully!")
        print(f"Agent ID: {result.get('id')}")
        print(f"Name: {result.get('name')}")
        print(f"Status: {result.get('status')}")
    else:
        print(f"❌ Failed to create agent: {response.status}")
"""
)
```

### Penetration Testing Agent
```python
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

agent_data = {
    "name": "Penetration_Testing_Agent",
    "task": \"\"\"Perform comprehensive penetration testing with full attack simulation.

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
- Compliance assessment\"\"\"
}

# Convert data to JSON
json_data = json.dumps(agent_data).encode('utf-8')

# Create request
req = urllib.request.Request(
    "http://127.0.0.1:37695/api/agents/create",
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

# Send request
with urllib.request.urlopen(req, timeout=30) as response:
    if response.status == 200:
        result = json.loads(response.read().decode('utf-8'))
        print("✅ Penetration Testing Agent created successfully!")
        print(f"Agent ID: {result.get('id')}")
    else:
        print(f"❌ Failed to create agent: {response.status}")
"""
)
```

### Malware Analysis Agent
```python
mcp_hexstrike-ai_execute_python_script(
    script="""
import urllib.request
import json

agent_data = {
    "name": "Malware_Analysis_Agent",
    "task": \"\"\"Perform comprehensive malware analysis and reverse engineering.

ANALYSIS PHASES:
1. Static Analysis - File structure, strings, imports
2. Dynamic Analysis - Behavioral monitoring and sandbox execution
3. Network Analysis - C2 communication and data exfiltration
4. Code Analysis - Reverse engineering and decompilation
5. Threat Intelligence - IOCs and attribution analysis
6. Mitigation Recommendations - Detection and prevention

TOOLS AND TECHNIQUES:
- Static analysis tools (strings, file, binwalk)
- Dynamic analysis (sandbox execution, API monitoring)
- Reverse engineering (Ghidra, Radare2, IDA Pro)
- Network analysis (Wireshark, tcpdump)
- Memory forensics (Volatility, Rekall)
- YARA rule generation

DELIVERABLES:
- Malware family classification
- Behavioral analysis report
- Network indicators and C2 infrastructure
- YARA detection rules
- Mitigation and prevention recommendations\"\"\"
}

# Convert data to JSON
json_data = json.dumps(agent_data).encode('utf-8')

# Create request
req = urllib.request.Request(
    "http://127.0.0.1:37695/api/agents/create",
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

# Send request
with urllib.request.urlopen(req, timeout=30) as response:
    if response.status == 200:
        result = json.loads(response.read().decode('utf-8'))
        print("✅ Malware Analysis Agent created successfully!")
        print(f"Agent ID: {result.get('id')}")
    else:
        print(f"❌ Failed to create agent: {response.status}")
"""
)
```

## 🔧 Integration with HexStrike Tools

The Villager agents can leverage the full HexStrike toolkit (150+ security tools) through the MCP system:

- **Network Scanning**: Nmap, Masscan, Rustscan
- **Web Testing**: Nuclei, SQLMap, Burp Suite, OWASP ZAP
- **Exploitation**: Metasploit, Hydra, Hashcat
- **Forensics**: Volatility, Ghidra, Radare2
- **Cloud Security**: Prowler, Trivy, Kube-hunter
- **And many more...**

## 🚀 Future Enhancement: Dedicated Villager Tools

The following dedicated Villager tools have been implemented in the HexStrike MCP client and will be available after a Cursor restart:

- `mcp_hexstrike-ai_create_villager_agent(name, task)` - Create autonomous agents
- `mcp_hexstrike-ai_list_villager_agents()` - List all active agents
- `mcp_hexstrike-ai_get_villager_status()` - Get server status
- `mcp_hexstrike-ai_run_villager_scan(target, scan_type)` - Initiate security scans
- `mcp_hexstrike-ai_list_villager_scans()` - List active scans

These tools provide a cleaner API than the current `execute_python_script` approach, but the current method is fully functional and recommended for immediate use.

## 🚨 Important Notes for AI Assistants

1. **Always use HexStrike MCP tools** - Never use direct terminal commands
2. **Use urllib, not requests** - The HexStrike environment doesn't have the requests module
3. **Agent-first approach** - Create agents for complex tasks, not direct execution
4. **Proper error handling** - Always check response status codes
5. **Timeout considerations** - Set appropriate timeouts for long-running operations
6. **Resource management** - Monitor agent status and progress
7. **Security awareness** - Remember this is for authorized testing only

## 🔧 Troubleshooting

### If HexStrike MCP tools return "Not connected":
1. **Check if HexStrike MCP client is running:**
   ```bash
   ps aux | grep hexstrike_mcp | grep -v grep
   ```

2. **Start the HexStrike MCP client:**
   ```bash
   cd /home/yenn/hexstrike-ai
   source hexstrike-env/bin/activate
   python hexstrike_mcp.py --server http://localhost:8000 --debug &
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
mcp_hexstrike-ai_execute_python_script(script="import urllib.request, json; print(json.loads(urllib.request.urlopen('http://127.0.0.1:37695/api/status').read().decode('utf-8')))")

# List agents
mcp_hexstrike-ai_execute_python_script(script="import urllib.request, json; print(json.loads(urllib.request.urlopen('http://127.0.0.1:37695/api/agents').read().decode('utf-8')))")

# List scans
mcp_hexstrike-ai_execute_python_script(script="import urllib.request, json; print(json.loads(urllib.request.urlopen('http://127.0.0.1:37695/api/scans').read().decode('utf-8')))")
```

---

**Remember**: This system is designed for authorized security testing and research purposes only. Always ensure you have proper authorization before conducting any security assessments.
