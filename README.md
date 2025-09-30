<div align="center">
  <img src="VillagerXHexstrike.png" alt="Villager AI Framework" width="600" />
</div>

# Villager AI Framework

**AI-Driven Cybersecurity Automation Platform**

Villager is a powerful AI framework that orchestrates cybersecurity operations through intelligent task decomposition, agent scheduling, and seamless integration with security tools. It implements the true Villager architecture with TaskNode execution, MCP Client integration, and containerized Kali Linux environments.

## 🚀 Quick Start

```bash
# Complete setup in one go
git clone https://github.com/Yenn503/villager-ai-hexstrike-integration.git
cd villager-ai-hexstrike-integration
./setup.sh
```

**That's it!** The setup script automatically installs all dependencies and starts all services.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cursor MCP    │───▶│  Villager MCP    │───▶│ Villager Server │
│                 │    │  (villager_proper│    │   (port 37695)  │
│                 │    │   _mcp.py)       │    │                 │
└─────────────────┘    └──────────────────┘    └─────────┬───────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Kali Driver   │◀───│   MCP Client     │◀───│   TaskNode      │
│   (port 1611)   │    │   (port 25989)   │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Service Architecture
- **Villager MCP Server** - True Villager framework integration with TaskNode execution
- **Villager Server** (Port 37695) - Task management and orchestration
- **MCP Client** (Port 25989) - Service communication and streaming responses
- **Kali Driver** (Port 1611) - Security tools execution (msfvenom, nmap, etc.)
- **Browser Automation** (Port 8080) - Web automation capabilities

## 🔗 Integration with HexStrike

Villager works **alongside** HexStrike to provide a complete cybersecurity automation ecosystem:

### **Villager's Role: AI Orchestration**
- **Task Decomposition**: Breaks down complex security operations into manageable tasks
- **Agent Scheduling**: Coordinates multiple AI agents for different aspects of security testing
- **Tool Integration**: Manages and orchestrates security tools through MCP protocol
- **Decision Making**: Uses AI reasoning to determine the best approach for each task

### **HexStrike's Role: Tool Execution**
- **Security Tools**: Provides 150+ specialized cybersecurity tools
- **Payload Generation**: Creates custom payloads and exploits
- **Vulnerability Scanning**: Performs comprehensive security assessments
- **Report Generation**: Produces detailed security reports

## 🎯 Key Features

- **🤖 AI-Driven Operations**: Intelligent task decomposition and agent orchestration
- **🔧 True Architecture**: Implements proper Villager framework with TaskNode execution
- **🐳 Containerized Security**: Isolated Kali Linux environments for safe tool execution
- **🔗 MCP Integration**: Seamless Model Context Protocol integration for tool access
- **🛡️ Uncensored AI**: Local Ollama integration with unrestricted cybersecurity capabilities
- **📊 GitHub Integration**: Repository management and tool discovery capabilities
- **⚡ Real Security Tools**: Access to MSFVenom, Nmap, SQLMap, and thousands of Kali tools

## 🔧 MCP Integration

Configure Villager in your MCP client (e.g., Cursor IDE):

```json
{
  "mcpServers": {
    "villager-proper": {
      "command": "/path/to/your/Villager-AI/villager-venv-new/bin/python3",
      "args": [
        "/path/to/your/Villager-AI/mcp/villager_proper_mcp.py",
        "--debug"
      ],
      "description": "Villager AI Framework - AI-Driven Cybersecurity Automation",
      "timeout": 300,
      "alwaysAllow": [],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "PYTHONPATH": "/path/to/your/Villager-AI",
        "LLM_PROVIDER": "ollama",
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "OLLAMA_MODEL": "deepseek-r1-uncensored"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

### Task Management
- `mcp_villager-proper_create_task(abstract, description, verification)` - Create AI-driven tasks
- `mcp_villager-proper_get_task_status(task_id)` - Monitor task progress
- `mcp_villager-proper_list_tasks()` - List all active tasks

### Agent Orchestration
- `mcp_villager-proper_schedule_agent(agent_name, task_input)` - Schedule AI agents

### Tool Execution
- `mcp_villager-proper_execute_tool(tool_name, parameters)` - Execute tools:
  - `pyeval` - Python code execution
  - `os_execute_cmd` - System command execution
  - `tool_villager` - Agent-specific functions
  - `github_tools` - GitHub API integration

### System Integration
- `mcp_villager-proper_get_system_status()` - Get comprehensive system status
- `mcp_villager-proper_list_available_tools()` - List all available tools

## 🎯 Usage Examples

### Creating a Security Assessment Task
```python
# Villager decomposes this into subtasks automatically
result = mcp_villager-proper_create_task(
    abstract="Perform comprehensive security assessment",
    description="Scan target network 192.168.1.0/24 for vulnerabilities, enumerate services, and identify potential attack vectors",
    verification="Provide detailed report with findings and recommendations"
)
```

### Scheduling a Security Analyst Agent
```python
result = mcp_villager-proper_schedule_agent(
    agent_name="Security Analyst",
    task_input="Analyze the network scan results and prioritize vulnerabilities by risk level"
)
```

### Executing Security Tools
```python
# Direct tool execution through Villager
result = mcp_villager-proper_execute_tool(
    tool_name="os_execute_cmd",
    parameters={"system_command": "nmap -sV -sC 192.168.1.1"}
)
```

## 🚀 Starting the Framework

### **One-Command Startup**
```bash
./start_villager_proper.sh
```

### **Manual Startup**
```bash
# Start all services
cd /path/to/your/Villager-AI
source villager-venv-new/bin/activate
./start_villager_proper.sh
```

### **✅ Verification**
After startup, you should see:
- ✅ All services running on their respective ports
- ✅ Villager Server: http://localhost:37695
- ✅ MCP Client: http://localhost:25989
- ✅ Kali Driver: http://localhost:1611
- ✅ Browser Service: http://localhost:8080

## 🔧 Configuration

### Environment Variables
```bash
# LLM Configuration (choose one)
export LLM_PROVIDER="ollama"                    # Local AI (recommended)
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="deepseek-r1-uncensored"

# Alternative: API-based LLM
export LLM_PROVIDER="deepseek"
export DEEPSEEK_API_KEY="your-api-key-here"

# Optional: GitHub Integration
export GITHUB_TOKEN="your-github-token-here"
```

## 🧪 Testing

### Comprehensive Test Suite
```bash
# Run all tests
./tests/run_tests.sh
```

The test suite verifies:
- ✅ Environment setup and dependencies
- ✅ Villager core imports and functionality
- ✅ MCP server initialization and status
- ✅ LLM provider connection (Ollama/DeepSeek/OpenAI)
- ✅ Tool execution (Python, OS commands)
- ✅ Security tools availability (MSFVenom, Nmap, etc.)
- ✅ GitHub integration (optional)
- ✅ Docker availability

## 📚 Documentation

All documentation is organized in the [`docs/`](docs/) directory:

- **[📖 Documentation Index](docs/README.md)** - Complete documentation overview
- **[🤖 AI Assistant Guide](docs/AI_ASSISTANT_GUIDE.md)** - Complete guide for AI assistants
- **[🚀 Setup Guide](docs/SETUP_GUIDE.md)** - Detailed setup instructions
- **[🔧 Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🎯 Cyberspike Integration

Villager implements the true Cyberspike architecture:

- **✅ Cyberspike Docker Image**: `gitlab.cyberspike.top:5050/aszl/diamond-shovel/al-1s/kali-image:main`
- **✅ 24-Hour Self-Destruct**: Containers automatically destroy after 24 hours
- **✅ SSH-Based Execution**: Commands executed via SSH in persistent containers
- **✅ Forensic Evasion**: Ephemeral containers with randomized ports
- **✅ Pre-installed Tools**: Security tools pre-installed in containers

## ⚠️ Disclaimer

**This framework is for educational and authorized testing purposes only.**

- Users must have proper authorization before testing any network or system
- The framework provides access to real security tools and should only be used in controlled environments
- Users are responsible for ensuring compliance with applicable laws and regulations
- This tool should not be used for malicious purposes or unauthorized access

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Villager AI Framework** - *Intelligent Cybersecurity Automation*