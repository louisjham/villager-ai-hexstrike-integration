<div align="center">

# 🏘️ Villager AI Framework

<img src="VillagerXHexstrike.png" alt="Villager AI Framework" width="600" />

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-green.svg)](https://github.com/Yenn503/villager-ai-hexstrike-integration)

**🤖 AI-Driven Cybersecurity Automation Platform**

</div>

---

## 🌟 About Villager AI + HexStrike

**Villager AI** and **HexStrike** are both powerful cybersecurity tools that work under the control of your AI model (like Cursor). Your AI can intelligently choose between them based on task complexity: **HexStrike** for fast, direct tool execution (quick tests, single commands, immediate results) and **Villager AI** for complex, orchestrated operations using its own framework and uncensored models like DeepSeek. This gives you the flexibility to use HexStrike's 150+ tools for rapid testing or Villager's advanced AI orchestration for sophisticated multi-step security assessments.

**Key Features:**
- 🤖 **AI Model Control** - Both tools controlled by your AI (Cursor, etc.)
- ⚡ **Fast Execution** - HexStrike for quick tests and direct tool access
- 🧠 **Advanced Orchestration** - Villager for complex, multi-step operations
- 🛡️ **150+ Security Tools** - Complete HexStrike arsenal available
- 🔗 **MCP Integration** - Seamless integration with any MCP-compatible client
- 🧠 **Uncensored AI** - Local DeepSeek and other models for unrestricted reasoning

---

## 🚀 Quick Setup

```bash
# Clone and setup in one command
git clone https://github.com/Yenn503/villager-ai-hexstrike-integration.git
cd villager-ai-hexstrike-integration
./scripts/setup.sh

# Start the framework
./scripts/start_villager_proper.sh

# Test the setup (optional but recommended)
./scripts/test_cyberspike_setup.sh
```

**That's it!** Both Villager AI and HexStrike ready for your AI model to use.

---

## 🔧 MCP Integration

Configure your MCP client to use Villager AI. See the [Setup Guide](docs/SETUP_GUIDE.md) for detailed MCP configuration instructions.

---



## 📚 Documentation

| Guide | Purpose |
|:---:|:---|
| **[Setup Guide](docs/SETUP_GUIDE.md)** | Complete setup instructions and configuration |
| **[AI Assistant Guide](docs/AI_ASSISTANT_GUIDE.md)** | How AI assistants should use both tools intelligently |
| **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** | Common issues and solutions |
| **[System Requirements](SYSTEM_REQUIREMENTS.md)** | System dependencies and requirements |

## 💡 Usage Examples

### Quick Tests with HexStrike
```python
# Your AI chooses HexStrike for fast, direct execution
result = mcp_hexstrike-ai_nmap_scan(
    target="192.168.1.1",
    scan_type="-sV",
    ports="22,80,443"
)

# Direct tool execution for immediate results
result = mcp_hexstrike-ai_msfvenom_generate(
    payload="windows/meterpreter/reverse_tcp",
    format_type="exe",
    output_file="payload.exe"
)
```

### Complex Operations with Villager AI
```python
# Your AI chooses Villager for sophisticated orchestration
result = mcp_villager-proper_create_task(
    abstract="Comprehensive Security Assessment",
    description="Multi-phase assessment with AI-driven decision making",
    verification="Detailed report with AI analysis and recommendations"
)

# Villager uses its own framework and uncensored models
# for complex task decomposition and execution
```

---

## ⚠️ Disclaimer

> **This framework is for educational and authorized testing purposes only.**

- Users must have explicit permission before testing any system
- Use only in controlled, isolated environments
- Comply with all applicable laws and regulations

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Villager AI Framework** - *AI-Driven Cybersecurity Automation with HexStrike Integration*

[![GitHub stars](https://img.shields.io/github/stars/Yenn503/villager-ai-hexstrike-integration?style=social)](https://github.com/Yenn503/villager-ai-hexstrike-integration)

</div>