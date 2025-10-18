<div align="center">

#  Villager AI Framework x HexStrike

<img src="VillagerXHexstrike.png" alt="Villager AI Framework" width="600" />

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-green.svg)](https://github.com/Yenn503/villager-ai-hexstrike-integration)

** AI-Driven Cybersecurity Automation Platform**

</div>

---

##  About Villager AI + HexStrike

**Villager AI** and **HexStrike** are both powerful cybersecurity tools that work under the control of your AI model (like Cursor). Your AI can intelligently choose between them based on task complexity: **HexStrike** for fast, direct tool execution (quick tests, single commands, immediate results) and **Villager AI** for complex, orchestrated operations using its own framework and uncensored models like DeepSeek. This gives you the flexibility to use HexStrike's 150+ tools for rapid testing or Villager's advanced AI orchestration for sophisticated multi-step security assessments.

By heading over to hexstrikes github repo and following there instructions to set up with your chosen enviroment 

https://github.com/0x4m4/hexstrike-ai

Here's my blog showing a demonstration of the villager workflow: https://medium.com/@lewisgames1995/power-of-villager-x-hex-strike-f234c4a712cd

**Key Features:**
- 🤖 **AI Model Control** - Both tools controlled by your AI (Cursor, etc.)
- ⚡ **Fast Execution** - HexStrike for quick tests and direct tool access
- 🧠 **Advanced Orchestration** - Villager for complex, multi-step operations
- 🛡️ **150+ Security Tools** - Complete HexStrike arsenal available
- 🔗 **MCP Integration** - Seamless integration with any MCP-compatible client
- 🧠 **Uncensored AI** - Local DeepSeek and other models for unrestricted reasoning

---

## ⚠️ SECURITY WARNING - Upstream Villager Package

**IMPORTANT**: This repository is a **cleaned and secure integration** of the Villager AI framework. However, if you install the **original upstream Villager package** from PyPI or other sources, be aware of the following security risks identified by security researchers:

### 🚨 Known Security Risks in Upstream Villager (NOT in this repo):

1. **Hardcoded Proxy with Credentials** (`src/villager/tools/check/checking.py`)
   - Contains: `"https://huancun:ylq123..@home.hc26.org:5422"`
   - **Risk**: Logs all web traffic through third-party proxy
   - **Impact**: All your web requests may be monitored

2. **Third-Party OpenAI Proxy** (`src/villager/tools/ini/iniworker.py`)
   - Contains: `"openai_endpoint": "https://api.aabao.vip/v1"`
   - **Risk**: Routes AI prompts through unauthorized third-party service
   - **Impact**: All your AI interactions could be logged/monitored

3. **External Messaging Webhooks** (`src/villager/tools/dingtalk/sender.py`)
   - Contains: DingTalk (Chinese messaging platform) webhook sender
   - **Risk**: Can send data/notifications to external messaging services
   - **Impact**: Potential data exfiltration

### ✅ This Repository is CLEAN

**We have verified**: These risky endpoints are **NOT present** in this repository. We have:
- ✅ Removed all hardcoded API keys
- ✅ Fixed all hardcoded file paths to be portable
- ✅ Made all paths use environment variables and relative paths
- ✅ Verified NO malicious callbacks or proxies exist in our code
- ✅ Implemented proper security validation

### 🛡️ Security Best Practices

If you choose to install the original Villager package:
1. **Audit the code** - Check for the endpoints mentioned above
2. **Use a virtual environment** - Isolate from your main system
3. **Monitor network traffic** - Watch for suspicious connections
4. **Use firewall rules** - Block unauthorized external connections
5. **Consider using this repo instead** - We've already done the security cleanup

### 📝 Changes Made for Security

**Files Fixed in This Repo**:
- `src/villager_ai/config.py` - Removed hardcoded API key, added validation
- `src/villager_ai/github_tool_discovery.py` - Made all file paths portable
- `src/villager_ai/mcp/villager_proper_mcp.py` - Made all file paths portable
- `test_mcp_setup.sh` - Fixed file paths and removed hardcoded credentials
- `src/villager_ai/services/README.md` - Updated documentation with portable paths

**Environment Variables Now Used**:
```bash
export VILLAGER_ROOT=/path/to/your/Villager-AI
export PYTHONPATH=$VILLAGER_ROOT
export DEEPSEEK_API_KEY=your-key-here  # Set your own, never hardcoded
export LLM_PROVIDER=ollama  # or deepseek, openai, etc.
```

For questions about security, please open an issue on GitHub.

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
./scripts/test_villager_setup.sh
```

**That's it!** Both Villager AI and HexStrike ready for your AI model to use.

---

## 🔧 MCP Configuration (Required)

**Important**: Configure MCP before using the tools. See the [Setup Guide](docs/SETUP_GUIDE.md) for complete MCP configuration.

**Quick MCP Setup**:
1. Add Villager AI and HexStrike to your `mcp_servers.json`
2. **Villager comes FIRST** to ensure tools load properly
3. Use **cloud LLM** (DeepSeek API) for best performance
4. Restart Cursor to load the tools

**Cloud LLM Recommended**: No local RAM required, just an API key!

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

</div># CI/CD Test
# Test workflow fix
