# 📚 Villager AI Framework Documentation

Welcome to the Villager AI Framework documentation. This directory contains essential guides for setting up, using, and troubleshooting the framework.

## 📖 Documentation Index

### 🚀 Getting Started
- **[Setup Guide](SETUP_GUIDE.md)** - Complete setup guide for the Villager framework
- **[AI Assistant Guide](AI_ASSISTANT_GUIDE.md)** - Complete guide for AI assistants on how to use Villager

### 🔧 Support
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions

## 🎯 Quick Navigation

| Document | Purpose | Audience |
|----------|---------|----------|
| [Setup Guide](SETUP_GUIDE.md) | Complete framework setup | Users, Developers |
| [AI Assistant Guide](AI_ASSISTANT_GUIDE.md) | How to use Villager via MCP | AI Assistants |
| [Troubleshooting Guide](TROUBLESHOOTING.md) | Troubleshooting | Users, Developers |

## 🔗 External Resources

- **Main Repository**: [Villager AI Framework](../README.md)
- **HexStrike Integration**: See AI Assistant Guide for integration details
- **MCP Configuration**: See Setup Guide for MCP client configuration

## 🎯 Framework Overview

Villager is an **AI-driven cybersecurity automation platform** that orchestrates complex security operations through:

- **Task Decomposition**: AI automatically breaks down complex tasks into manageable subtasks
- **Agent Scheduling**: Coordinates multiple AI agents for different security operations
- **Tool Integration**: Manages and orchestrates security tools through MCP protocol
- **Containerized Execution**: All security tools run in isolated Kali Linux environments

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

## 🛠️ Key Features

- **🤖 AI-Driven Operations**: Intelligent task decomposition and agent orchestration
- **🔧 True Architecture**: Implements proper Villager framework with TaskNode execution
- **🐳 Containerized Security**: Isolated Kali Linux environments for safe tool execution
- **🔗 MCP Integration**: Seamless Model Context Protocol integration for tool access
- **🛡️ Uncensored AI**: Local Ollama integration with unrestricted cybersecurity capabilities
- **📊 GitHub Integration**: Repository management and tool discovery capabilities
- **⚡ Real Security Tools**: Access to MSFVenom, Nmap, SQLMap, and thousands of Kali tools

## 🚀 Quick Start

1. **Setup**: Follow the [Setup Guide](SETUP_GUIDE.md)
2. **Configure MCP**: Add Villager to your Cursor MCP configuration
3. **Start Services**: Run `./start_villager_proper.sh`
4. **Test**: Use the MCP tools in Cursor to create tasks

## 📝 Contributing to Documentation

When updating documentation:
1. Keep it clear and concise
2. Use consistent formatting
3. Update this index if adding new documents
4. Test all code examples
5. Ensure links work correctly

---

*For the main framework documentation, see the [root README](../README.md).*