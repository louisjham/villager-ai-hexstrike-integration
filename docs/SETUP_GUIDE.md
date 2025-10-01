# Villager AI Framework - Setup Guide

This guide provides complete setup instructions for the Villager AI framework with HexStrike integration.

## 🚀 Quick Setup (Recommended)

```bash
# Clone and setup everything automatically
git clone https://github.com/Yenn503/villager-ai-hexstrike-integration.git
cd villager-ai-hexstrike-integration
./scripts/setup.sh

# Start the framework
./scripts/start_villager_proper.sh
```

**That's it!** Both Villager AI and HexStrike ready for your AI model to use.

## 🔧 Manual Setup

### Prerequisites
- **Python 3.8+** (3.13 recommended)
- **Docker** (for containerized security tools)
- **Ollama** (for local AI models)

### Step 1: System Dependencies
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Kali tools
sudo apt install -y kali-linux-everything

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull deepseek-r1-uncensored
ollama serve &
```

### Step 2: Python Setup
```bash
# Create virtual environment
python3 -m venv villager-venv-new
source villager-venv-new/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### Step 3: Start Services
```bash
# Start all services
./scripts/start_villager_proper.sh

# Verify services are running
curl http://localhost:37695/health  # Villager Server
curl http://localhost:25989/health  # MCP Client
curl http://localhost:1611/health   # Kali Driver
curl http://localhost:8080/health   # Browser Service
```

## 🔧 MCP Configuration

Add this to your `mcp_servers.json`:

```json
{
  "mcpServers": {
    "villager-proper": {
      "command": "/path/to/your/Villager-AI/villager-venv-new/bin/python3",
      "args": [
        "/path/to/your/Villager-AI/src/villager_ai/mcp/villager_proper_mcp.py",
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

**Important**: Replace `/path/to/your/Villager-AI` with your actual installation path.

## 🎯 Service Architecture

| Service | Port | Purpose |
|:---:|:---:|:---|
| Villager Server | 37695 | Task management and orchestration |
| MCP Client | 25989 | Service communication and streaming |
| Kali Driver | 1611 | Security tools execution |
| Browser Automation | 8080 | Web automation capabilities |

## 🔧 Configuration Options

### LLM Providers
- **Ollama (Recommended)**: Free, local, uncensored AI
- **DeepSeek API**: Cloud-based AI with API key
- **OpenAI API**: Cloud-based AI with API key

### Environment Variables
```bash
# LLM Configuration (Local Ollama - Recommended)
export LLM_PROVIDER="ollama"
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="deepseek-r1-uncensored"

# Alternative: API-based LLM
export LLM_PROVIDER="deepseek"
export DEEPSEEK_API_KEY="your-api-key-here"

# Optional: GitHub Integration
export GITHUB_TOKEN="your-github-token-here"
```

## 🧪 Testing

```bash
# Run comprehensive test suite
./tests/run_tests.sh
```

The test suite verifies:
- ✅ Environment setup and dependencies
- ✅ Villager core imports and functionality
- ✅ MCP server initialization
- ✅ LLM provider connectivity
- ✅ Tool execution capabilities
- ✅ Security tools availability
- ✅ Docker availability and container access

## 🎉 Success Indicators

✅ All services running on correct ports  
✅ MCP tools available in Cursor  
✅ Test suite passes  
✅ Can create and execute tasks  
✅ Security tools accessible through containers  

---

*For troubleshooting, see the [Troubleshooting Guide](TROUBLESHOOTING.md). For AI integration, see the [AI Assistant Guide](AI_ASSISTANT_GUIDE.md).*
