# 🛡️ **Villager AI + HexStrike Integration - Complete Guide**

## 🎯 **What This Is**

This is a **comprehensive AI-powered security framework** that combines:
- **Villager AI**: Autonomous penetration testing with 10 specialized AI agents
- **HexStrike AI**: 150+ security tools arsenal with AI-assisted execution
- **GitHub Integration**: Tool discovery and repository management
- **MCP Bridge**: Seamless chat-based access to everything

**Result**: A self-evolving security platform that can discover, install, and use new tools from GitHub while performing autonomous security operations.

---

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HexStrike AI  │    │   Villager AI   │    │   GitHub API    │
│   150+ Tools    │◄──►│   10 Agents     │◄──►│   Tool Discovery│
│   Port: 8000    │    │   Port: 37695   │    │   Repository    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   MCP Bridge    │
                    │   (Cursor AI)   │
                    └─────────────────┘
```

---

## 🤖 **The 10 Specialized Security Agents**

### **1. Reconnaissance_Agent**
**Purpose**: Information gathering and target discovery
**Tools**: Nmap, Amass, Subfinder, Masscan, Rustscan
**What it does**:
- Subdomain enumeration
- Port scanning and service detection
- OS fingerprinting
- Network range discovery
- IP address collection

### **2. Vulnerability_Assessment_Agent**
**Purpose**: Comprehensive vulnerability scanning
**Tools**: Nuclei, Trivy, Checkov, custom scanners
**What it does**:
- Known vulnerability scanning
- Container security assessment
- Infrastructure as Code security
- CVE database cross-referencing
- Vulnerability prioritization

### **3. Web_Application_Testing_Agent**
**Purpose**: Web application security testing
**Tools**: OWASP ZAP, Burp Suite, SQLMap, Nikto, Gobuster
**What it does**:
- Comprehensive web app scanning
- SQL injection testing
- XSS and CSRF testing
- Directory enumeration
- Server vulnerability checks

### **4. Exploitation_Agent**
**Purpose**: Vulnerability exploitation and initial access
**Tools**: Metasploit, SQLMap, Hydra, custom exploits
**What it does**:
- Exploit execution
- SQL injection exploitation
- Brute force attacks
- Access establishment
- Exploit documentation

### **5. Post_Exploitation_Agent**
**Purpose**: Lateral movement and persistence
**Tools**: Mimikatz, BloodHound, lateral movement tools
**What it does**:
- Credential extraction
- Active Directory analysis
- Lateral movement techniques
- Persistence establishment
- Privilege escalation

### **6. Forensics_Agent**
**Purpose**: Attack analysis and evidence collection
**Tools**: Volatility, Binwalk, Radare2, reverse engineering
**What it does**:
- Memory forensics analysis
- Firmware and file analysis
- Reverse engineering
- System artifact analysis
- Evidence collection

### **7. Monitoring_Agent**
**Purpose**: Continuous security monitoring
**Tools**: Custom monitoring scripts, Nuclei, network monitoring
**What it does**:
- Continuous network monitoring
- Ongoing vulnerability scanning
- CVE and threat monitoring
- Suspicious activity alerts
- System change tracking

### **8. Reporting_Agent**
**Purpose**: Comprehensive report generation
**Tools**: Custom reporting tools, GitHub integration, visualization
**What it does**:
- Data aggregation from all agents
- Executive summary generation
- Technical report creation
- GitHub report storage
- Data visualization

### **9. Workflow_Coordinator_Agent**
**Purpose**: Master orchestration and workflow management
**Tools**: GitHub integration, workflow management tools
**What it does**:
- Multi-stage operation coordination
- Agent execution sequencing
- Shared state management
- Data flow coordination
- Error handling and retry logic

### **10. GitHub_Tool_Discovery_Agent**
**Purpose**: Discover, install, and integrate new security tools
**Tools**: GitHub API, tool discovery system
**What it does**:
- Search GitHub for security tools
- Analyze tool types and installation methods
- Install tools automatically
- Test installed tools
- Integrate new tools into workflows

---

## 🚀 **How to Use the System**

### **Step 1: Start the Servers**

```bash
# Start Villager AI (Port 37695)
cd /home/yenn/Villager-AI
./start_villager.sh

# Start HexStrike AI (Port 8000) - if not already running
cd /home/yenn/hexstrike-ai
./start_hexstrike.sh
```

### **Step 2: Create Specialized Agents**

```python
# Create a reconnaissance agent
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

# Create reconnaissance agent
agent = {
    "name": "Recon_Agent",
    "task": "Perform comprehensive reconnaissance on target.com. Use Nmap for port scanning, Amass for subdomain enumeration, and gather all available information about the target."
}

result = subprocess.run([
    'curl', '-X', 'POST', 'http://127.0.0.1:37695/api/agents/create',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(agent)
], capture_output=True, text=True)

print("Agent created:", result.stdout)
""")
```

### **Step 3: Monitor Agent Progress**

```python
# Check all agents
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

result = subprocess.run(['curl', '-s', 'http://127.0.0.1:37695/api/agents'], capture_output=True, text=True)
agents = json.loads(result.stdout)

print(f"Total agents: {len(agents['agents'])}")
for agent in agents['agents']:
    print(f"• {agent['name']} - {agent['status']} ({agent['progress']}%)")
""")
```

### **Step 4: Use GitHub Tool Discovery**

```python
# Discover and install new tools
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

# Create tool discovery agent
agent = {
    "name": "Tool_Discovery_Agent",
    "task": "Search GitHub for Python-based network scanning tools, analyze the top 3 results, and install the best one. Test the installed tool to ensure it works correctly."
}

result = subprocess.run([
    'curl', '-X', 'POST', 'http://127.0.0.1:37695/api/agents/create',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(agent)
], capture_output=True, text=True)

print("Tool discovery agent created:", result.stdout)
""")
```

---

## 🔄 **Workflow Examples**

### **Example 1: Complete Penetration Test**

```python
# Create a coordinated penetration test
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

# Create workflow coordinator
coordinator = {
    "name": "Pentest_Coordinator",
    "task": "Coordinate a complete penetration test of target.com. Execute the following workflow: 1) Reconnaissance to gather information, 2) Vulnerability assessment to find weaknesses, 3) Exploitation attempts on found vulnerabilities, 4) Post-exploitation if access is gained, 5) Generate comprehensive report. Coordinate with other agents and ensure proper data flow between stages."
}

result = subprocess.run([
    'curl', '-X', 'POST', 'http://127.0.0.1:37695/api/agents/create',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(coordinator)
], capture_output=True, text=True)

print("Penetration test coordinator created:", result.stdout)
""")
```

### **Example 2: Continuous Security Monitoring**

```python
# Create monitoring system
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

# Create monitoring agent
monitor = {
    "name": "Security_Monitor",
    "task": "Set up continuous security monitoring for the network. Monitor for new vulnerabilities, scan for changes, and alert on suspicious activities. Coordinate with vulnerability assessment agents when issues are found."
}

result = subprocess.run([
    'curl', '-X', 'POST', 'http://127.0.0.1:37695/api/agents/create',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(monitor)
], capture_output=True, text=True)

print("Security monitor created:", result.stdout)
""")
```

### **Example 3: GitHub Tool Discovery and Integration**

```python
# Discover and integrate new tools
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

# Create tool discovery agent
discovery = {
    "name": "Tool_Discovery_Agent",
    "task": "Search GitHub for the latest security tools in these categories: 1) Web application security testing, 2) Network scanning, 3) Vulnerability assessment. For each category, find the top 2 tools, analyze their capabilities, install them, and integrate them into the appropriate agent workflows."
}

result = subprocess.run([
    'curl', '-X', 'POST', 'http://127.0.0.1:37695/api/agents/create',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(discovery)
], capture_output=True, text=True)

print("Tool discovery agent created:", result.stdout)
""")
```

---

## 🛠️ **Available Tools and Capabilities**

### **HexStrike Tools (150+)**
- **Network Scanning**: Nmap, Masscan, Rustscan, Gobuster, Dirb
- **Web Application Testing**: OWASP ZAP, Burp Suite, Nikto, SQLMap, XSSer
- **Vulnerability Scanning**: Nuclei, Trivy, Checkov, Clair
- **Exploitation**: Metasploit, Hydra, John the Ripper, Hashcat
- **Forensics**: Volatility, Binwalk, GDB, Radare2, Ghidra
- **Cloud Security**: Prowler, Scout Suite, CloudMapper
- **Container Security**: Docker Bench, Falco, Kube-hunter
- **And 100+ more specialized tools**

### **GitHub Integration**
- **Repository Management**: Create, fork, delete repositories
- **Issue Tracking**: Create, update, comment on issues
- **Pull Request Management**: Create, review, merge PRs
- **Code Analysis**: File operations, branch management
- **Tool Discovery**: Search, analyze, install security tools
- **Collaboration**: Share reports and findings

### **Villager Agent Capabilities**
- **Autonomous Task Planning**: Break complex tasks into subtasks
- **Tool Selection**: Intelligently choose appropriate tools
- **Multi-Agent Coordination**: Work together on complex operations
- **Error Recovery**: Retry failed operations with different approaches
- **Progress Tracking**: Real-time status updates
- **Self-Evolution**: Discover and integrate new tools

---

## 🔧 **Configuration and Setup**

### **Environment Variables**
```bash
# Required
DEEPSEEK_API_KEY=your-deepseek-api-key-here
GITHUB_TOKEN=your-github-token-here

# Optional
VILLAGER_HOST=0.0.0.0
VILLAGER_PORT=37695
ALLOW_SHELL=1
ALLOW_APT=1
ALLOW_WRITE=1
ALLOW_BUILD=1
```

### **GitHub Token Setup**
1. Go to GitHub: Settings → Developer settings → Personal access tokens
2. Generate new token with these scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Access workflow runs)
   - `gist` (Create gists)
3. Set environment variable: `export GITHUB_TOKEN="your-token"`

### **MCP Configuration**
The system is already configured in your Cursor MCP settings. No additional setup needed.

---

## 📊 **Monitoring and Management**

### **Check System Status**
```python
# Check Villager server status
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

result = subprocess.run(['curl', '-s', 'http://127.0.0.1:37695/api/status'], capture_output=True, text=True)
status = json.loads(result.stdout)
print("Villager Status:", status)
""")
```

### **List All Agents**
```python
# List all active agents
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

result = subprocess.run(['curl', '-s', 'http://127.0.0.1:37695/api/agents'], capture_output=True, text=True)
agents = json.loads(result.stdout)

print(f"Active Agents: {len(agents['agents'])}")
for agent in agents['agents']:
    print(f"• {agent['name']} - {agent['status']} ({agent['progress']}%)")
""")
```

### **Check Agent Details**
```python
# Get specific agent details
mcp_hexstrike-ai_execute_python_script(script="""
import subprocess
import json

# Replace with actual agent ID
agent_id = "your-agent-id-here"
result = subprocess.run(['curl', '-s', f'http://127.0.0.1:37695/api/agents/{agent_id}'], capture_output=True, text=True)
agent = json.loads(result.stdout)
print("Agent Details:", agent)
""")
```

---

## 🎯 **Best Practices**

### **Agent Creation**
- **Be Specific**: Give agents clear, detailed tasks
- **Use Specialized Agents**: Choose the right agent type for your task
- **Coordinate Workflows**: Use the Workflow Coordinator for complex operations
- **Monitor Progress**: Check agent status regularly

### **Tool Discovery**
- **Search Strategically**: Use specific keywords for tool discovery
- **Test Thoroughly**: Always test new tools before integration
- **Document Usage**: Keep track of tool capabilities and usage
- **Update Regularly**: Keep tools updated for latest features

### **Security Operations**
- **Start with Reconnaissance**: Always gather information first
- **Follow the Workflow**: Use the established penetration testing workflow
- **Document Everything**: Generate comprehensive reports
- **Coordinate Agents**: Let agents work together on complex tasks

### **GitHub Integration**
- **Use Repositories**: Store reports and findings in GitHub
- **Collaborate**: Share findings with team members
- **Version Control**: Track changes and improvements
- **Automate**: Use GitHub Actions for automated workflows

---

## 🚨 **Troubleshooting**

### **Common Issues**

**Agents Not Starting**
```bash
# Check server status
curl http://127.0.0.1:37695/api/status

# Restart Villager server
cd /home/yenn/Villager-AI
./start_villager.sh
```

**GitHub Integration Not Working**
```bash
# Check GitHub token
echo $GITHUB_TOKEN

# Test GitHub connection
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

**Tools Not Found**
```bash
# Check HexStrike server
curl http://127.0.0.1:8000/status

# Restart HexStrike server
cd /home/yenn/hexstrike-ai
./start_hexstrike.sh
```

### **Performance Optimization**
- **Limit Concurrent Agents**: Don't run too many agents simultaneously
- **Monitor Resource Usage**: Check CPU and memory usage
- **Clean Up**: Remove completed agents regularly
- **Update Tools**: Keep all tools updated

---

## 🎉 **What Makes This Special**

### **Self-Evolving Framework**
- **Tool Discovery**: Automatically find and install new security tools
- **Continuous Learning**: Agents learn from their experiences
- **Adaptive Workflows**: Workflows adapt based on results
- **Community Integration**: Leverage the entire GitHub security community

### **Comprehensive Coverage**
- **Full Security Lifecycle**: From reconnaissance to reporting
- **Multiple Attack Vectors**: Web, network, cloud, container security
- **Automated Coordination**: Agents work together seamlessly
- **Real-time Monitoring**: Continuous security assessment

### **Easy to Use**
- **Chat-Based Interface**: No complex command-line operations
- **Intelligent Agents**: Just describe what you want, agents figure out how
- **Progress Tracking**: Real-time status updates
- **Comprehensive Reports**: Detailed findings and recommendations

---

## 🚀 **Getting Started Right Now**

1. **Start the servers** (if not already running)
2. **Create your first agent**:
   ```python
   mcp_hexstrike-ai_execute_python_script(script="""
   import subprocess
   import json
   
   agent = {
       "name": "My_First_Agent",
       "task": "Analyze the current system and provide a security assessment. Check running processes, network connections, and system vulnerabilities."
   }
   
   result = subprocess.run([
       'curl', '-X', 'POST', 'http://127.0.0.1:37695/api/agents/create',
       '-H', 'Content-Type: application/json',
       '-d', json.dumps(agent)
   ], capture_output=True, text=True)
   
   print("Agent created:", result.stdout)
   """)
   ```
3. **Monitor the agent's progress**
4. **Explore the results**
5. **Create more specialized agents as needed**

---

**This is the most comprehensive and advanced AI-powered security framework available. You now have access to autonomous agents that can discover new tools, coordinate complex security operations, and provide detailed analysis - all through simple chat commands. Welcome to the future of cybersecurity!** 🛡️🤖
