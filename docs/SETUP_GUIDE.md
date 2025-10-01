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

## 🔧 MCP Configuration (Required)

**Important**: Configure MCP before starting services to ensure tools are available in Cursor.

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
        "LLM_PROVIDER": "deepseek",
        "DEEPSEEK_API_KEY": "your-api-key-here"
      }
    },
    "hexstrike-ai": {
      "command": "/path/to/your/hexstrike-ai/hexstrike-env/bin/python3",
      "args": [
        "/path/to/your/hexstrike-ai/hexstrike_mcp.py",
        "--server",
        "http://localhost:8000",
        "--debug"
      ],
      "description": "HexStrike AI - Advanced Cybersecurity Tools",
      "timeout": 300,
      "alwaysAllow": []
    }
  }
}
```

**Key Points**:
1. **Villager comes FIRST** - Ensures Cursor loads Villager tools before hitting tool limits
2. **Replace paths** - Use actual paths to your installations
3. **Cloud LLM** - Uses DeepSeek API by default but has the ability to use other models too 

## 🔧 Manual Setup

### Prerequisites
- **Python 3.8+** (3.13 recommended)
- **Docker** (for containerized security tools)
- **API Key** (for cloud AI models - recommended)
- **Ollama** (optional - for local AI models)

### Step 1: System Dependencies
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Kali tools
sudo apt install -y kali-linux-everything

# Optional: Install Ollama for local AI models
# curl -fsSL https://ollama.ai/install.sh | sh
# search on https://huggingface.co/ to find a model of your liking for example:
# ollama pull (model of choice)
# ollama serve &
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

## 🔧 LLM Configuration

### Option 1: Cloud LLM (Recommended - No RAM Required)

```bash
# Set environment variables for cloud AI
export LLM_PROVIDER="deepseek"
export DEEPSEEK_API_KEY="your-api-key-here"

# Alternative: OpenAI
# export LLM_PROVIDER="openai"
# export OPENAI_API_KEY="your-api-key-here"
```

### Option 2: Local Ollama (High RAM Required)

```bash
# Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull deepseek-r1-uncensored
ollama serve &

# Set environment variables
export LLM_PROVIDER="ollama"
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="deepseek-r1-uncensored"
```

## 🎯 Service Architecture

| Service | Port | Purpose |
|:---:|:---:|:---|
| Villager Server | 37695 | Task management and orchestration |
| MCP Client | 25989 | Service communication and streaming |
| Kali Driver | 1611 | Security tools execution |
| Browser Automation | 8080 | Web automation capabilities |

## 🔧 Additional Configuration

### Environment Variables
```bash
# Cloud LLM Configuration (Recommended)
export LLM_PROVIDER="deepseek"
export DEEPSEEK_API_KEY="your-api-key-here"

# Alternative: OpenAI
# export LLM_PROVIDER="openai"
# export OPENAI_API_KEY="your-api-key-here"

# Local Ollama (High RAM Required)
# export LLM_PROVIDER="ollama"
# export OLLAMA_BASE_URL="http://localhost:11434"
# export OLLAMA_MODEL="deepseek-r1-uncensored"

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
