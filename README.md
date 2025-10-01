<div align="center">
<img src="VillagerXHexstrike.png" alt="Villager AI Framework" width="600" />
</div>

<h1 align="center">Villager AI Framework</h1>

<p align="center">
<strong>An AI-driven framework for orchestrating and automating cybersecurity operations.</strong>
<br />
<br />
<a href="#-quick-start">Quick Start</a> •
<a href="#-architecture">Architecture</a> •
<a href="#-key-features">Features</a> •
<a href="#-usage-examples">Usage</a> •
<a href="#-configuration">Configuration</a> •
<a href="#-documentation">Docs</a>
</p>

<p align="center">
<img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
<img src="https://img.shields.io/badge/python-3.9+-informational.svg" alt="Python Version">
<img src="https://img.shields.io/badge/status-active-success.svg" alt="Status">
</p>

Villager is a powerful AI framework that orchestrates cybersecurity operations through intelligent task decomposition, agent scheduling, and seamless integration with security tools. It implements the true Villager architecture with TaskNode execution, MCP Client integration, and containerized Kali Linux environments for secure and robust testing.

🚀 Quick Start

Get the entire framework up and running with a single script.
Bash

# Clone the repository and run the setup script
git clone https://github.com/Yenn503/villager-ai-hexstrike-integration.git
cd villager-ai-hexstrike-integration
./setup.sh

    That's it! The setup script automatically installs all dependencies, builds the necessary containers, and starts all services.

🏗️ Architecture

Villager operates on a distributed, service-oriented architecture, ensuring modularity and scalability.

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cursor MCP    │───▶│  Villager MCP    │───▶│ Villager Server │
│ (User Interface)│    │  (villager_proper│    │   (port 37695)  │
└─────────────────┘    │   _mcp.py)       │    │                 │
                       └──────────────────┘    └─────────┬───────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Kali Driver   │◀───│   MCP Client     │◀───│   TaskNode      │
│   (port 1611)   │    │   (port 25989)   │    │  (Execution)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘

Core Services

    Villager MCP Server: The central brain, integrating the true Villager framework with TaskNode execution.

    Villager Server (Port 37695): Manages and orchestrates high-level tasks and AI agents.

    MCP Client (Port 25989): Facilitates communication between services and streams responses.

    Kali Driver (Port 1611): Executes security tools (msfvenom, nmap, etc.) within a secure container.

    Browser Automation (Port 8080): Provides web automation and scraping capabilities.

A Symbiotic Ecosystem: Villager & HexStrike

Villager and HexStrike work in tandem, each with a distinct role, to create a comprehensive cybersecurity automation platform.
Framework	Role & Responsibilities
🤖 Villager	AI Orchestration & Strategy • Task Decomposition: Breaks down high-level goals into executable steps. • Agent Scheduling: Coordinates AI agents for analysis and decision-making. • Tool Integration: Manages security tools via the MCP protocol. • AI-Driven Logic: Determines the optimal approach for each task.
🛡️ HexStrike	Tool Execution & Exploitation • Tool Arsenal: Provides 150+ specialized cybersecurity tools. • Payload Generation: Creates custom payloads and exploits. • Vulnerability Scanning: Performs deep security assessments. • Report Generation: Produces detailed findings and reports.

🎯 Key Features

    AI-Driven Operations: Leverages LLMs for intelligent task decomposition and agent orchestration.

    True Villager Architecture: Implements the proper framework with TaskNode execution for robust performance.

    Containerized Security: Utilizes isolated Kali Linux environments for safe and clean tool execution.

    Seamless MCP Integration: Integrates flawlessly with any Model Context Protocol (MCP) client like Cursor.

    Uncensored Local AI: Natively supports Ollama for unrestricted, private, and powerful cybersecurity reasoning.

    Real Security Tools: Provides programmatic access to thousands of industry-standard Kali tools, including MSFVenom, Nmap, and SQLMap.

⚙️ Connecting with MCP

Integrate Villager into your MCP client (e.g., Cursor IDE) by adding the following to your configuration file (mcp_servers.json).

    Note: Remember to replace /path/to/your/Villager-AI with the absolute path to the project directory.

JSON

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

🛠️ Core Commands (MCP Tools)

Interact with the framework using these MCP functions from your connected client.

Task Management

    mcp_villager-proper_create_task(abstract, description, verification): Creates a new high-level task for the AI to decompose and execute.

    mcp_villager-proper_get_task_status(task_id): Monitors the progress and status of a specific task.

    mcp_villager-proper_list_tasks(): Lists all currently active tasks.

Tool & System Execution

    mcp_villager-proper_execute_tool(tool_name, parameters): Directly executes a specific tool.

        pyeval: Python code execution.

        os_execute_cmd: System command execution within the Kali container.

        github_tools: GitHub API integration.

    mcp_villager-proper_list_available_tools(): Lists all tools registered with the framework.

    mcp_villager-proper_get_system_status(): Retrieves a comprehensive status of all Villager services.

💡 Usage Examples

1. Create a Full Security Assessment Task

Let Villager's AI handle the entire workflow from reconnaissance to reporting.
Python

# The AI will decompose this abstract goal into multiple sub-tasks (e.g., nmap scan, service enumeration, vulnerability analysis).
result = mcp_villager-proper_create_task(
    abstract="Perform a comprehensive security assessment on the target network.",
    description="Scan the 192.168.1.0/24 network for vulnerabilities, enumerate all services, and identify potential attack vectors.",
    verification="Produce a detailed report outlining findings, risk levels, and mitigation recommendations."
)

2. Execute a Specific Security Tool

Run a command directly when you know exactly what you need.
Python

# Execute an Nmap scan for service versions and common scripts.
result = mcp_villager-proper_execute_tool(
    tool_name="os_execute_cmd",
    parameters={"system_command": "nmap -sV -sC 192.168.1.1"}
)

🔌 Framework Management

Starting the Framework

    One-Command Startup:
    Bash

./start_villager_proper.sh

Manual Startup:
Bash

    # Activate the virtual environment
    source villager-venv-new/bin/activate
    # Run the startup script
    ./start_villager_proper.sh

Verification

After startup, ensure all services are running correctly:

    ✅ Villager Server: http://localhost:37695

    ✅ MCP Client: http://localhost:25989

    ✅ Kali Driver: http://localhost:1611

    ✅ Browser Service: http://localhost:8080

🔧 Configuration

Configure the framework using environment variables.
Bash

# LLM Configuration (Ollama is recommended for uncensored, local operation)
export LLM_PROVIDER="ollama"
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="deepseek-r1-uncensored" # Or another model of your choice

# Alternative: API-based LLM (e.g., DeepSeek)
# export LLM_PROVIDER="deepseek"
# export DEEPSEEK_API_KEY="your-api-key-here"

# Optional: GitHub Integration for repository tools
export GITHUB_TOKEN="your-github-token-here"

🧪 Testing

A comprehensive test suite is included to validate your setup and ensure all components are functional.
Bash

# Run the entire test suite
./tests/run_tests.sh

The suite verifies:

    Environment setup and dependencies

    Core Villager imports and functionality

    MCP server initialization

    LLM provider connectivity (Ollama/DeepSeek)

    Tool execution (Python, OS commands)

    Security tool availability (msfvenom, nmap)

    GitHub integration (if configured)

    Docker availability and container access

📚 Documentation

Detailed documentation for setup, usage, and troubleshooting can be found in the docs/ directory.

    📖 Main Index: Overview of all documentation.

    🤖 AI Assistant Guide: In-depth guide for interacting with the AI.

    🚀 Setup Guide: Step-by-step installation instructions.

    🔧 Troubleshooting: Solutions for common issues.

⚠️ Disclaimer

    For Educational & Authorized Use Only

    This framework provides access to powerful security tools and is intended strictly for educational purposes and authorized security testing.

        Users must have explicit permission from the target system's owner before conducting any security assessment.

        Usage of this framework should be confined to controlled, isolated environments.

        The developers are not responsible for any misuse or damage caused by this tool. Users are solely responsible for their actions and for complying with all applicable laws.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

Villager AI Framework — Intelligent Cybersecurity Automation