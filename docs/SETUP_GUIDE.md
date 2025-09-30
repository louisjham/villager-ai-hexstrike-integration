# Villager AI Framework - Setup Guide

This guide provides complete setup instructions for the Villager AI framework.

## 🚀 Quick Setup (Recommended)

### One-Command Installation
```bash
# Clone and setup everything automatically
git clone https://github.com/Yenn503/villager-ai-hexstrike-integration.git
cd villager-ai-hexstrike-integration
./setup.sh
```

The setup script automatically:
- Installs Docker and Kali tools
- Sets up Ollama with DeepSeek R1 uncensored model
- Installs Python dependencies
- Configures the virtual environment
- Starts all services

## 🔧 Manual Setup

### Prerequisites
- **Python 3.8+**
- **Docker** (for persistent SSH containers)
- **Ollama** (for local AI model)

### Step 1: Environment Setup
```bash
# Create virtual environment
python -m venv villager-venv-new
source villager-venv-new/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the uncensored AI model
ollama pull deepseek-r1-uncensored

# Start Ollama server
ollama serve &
```

### Step 3: Configure Environment
```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your preferred settings
# The file includes detailed instructions for each option
```

### Step 4: Start Villager
```bash
# Start all services
./start_villager_proper.sh
```

## 🔧 MCP Configuration

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

## ✅ Verification

After setup, verify everything is working:

### Check Services
```bash
# Check if all services are running
lsof -i -P -n | grep LISTEN | grep -E "(25989|1611|37695|8080)"
```

### Run Tests
```bash
# Run comprehensive test suite
./tests/run_tests.sh
```

### Test MCP Connection
```python
# In Cursor, test the MCP connection
mcp_villager-proper_get_system_status()
```

## 🎯 Service Architecture

| Service | Port | Purpose |
|---------|------|---------|
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
# LLM Configuration
export LLM_PROVIDER="ollama"
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="deepseek-r1-uncensored"

# Alternative: API-based LLM
export LLM_PROVIDER="deepseek"
export DEEPSEEK_API_KEY="your-api-key-here"

# Optional: GitHub Integration
export GITHUB_TOKEN="your-github-token-here"
```

## 🐳 Docker Configuration

Villager uses Docker for containerized security tool execution:

### Cyberspike Integration
- **Primary Image**: `gitlab.cyberspike.top:5050/aszl/diamond-shovel/al-1s/kali-image:main`
- **Fallback Image**: `kalilinux/kali-rolling`
- **Features**: Pre-installed security tools, 24-hour self-destruct

### Container Management
- **Persistence**: Containers run for 24 hours then auto-destroy
- **SSH Access**: Commands executed via SSH on randomized ports
- **Forensic Evasion**: Ephemeral containers with automatic cleanup

## 🚨 Troubleshooting

### Common Issues

1. **Services not starting**:
   ```bash
   # Check Docker status
   sudo systemctl status docker
   
   # Restart all services
   pkill -f "python.*services"
   ./start_villager_proper.sh
   ```

2. **MCP tools not available**:
   - Ensure Villager comes FIRST in MCP config
   - Check PYTHONPATH is set correctly
   - Restart Cursor after config changes

3. **Container creation fails**:
   ```bash
   # Check Docker daemon
   sudo systemctl start docker
   
   # Check available images
   docker images
   ```

4. **Ollama not responding**:
   ```bash
   # Start Ollama server
   ollama serve &
   
   # Check model availability
   ollama list
   ```

### Debug Commands
```bash
# Check service logs
tail -f logs/villager_server.log
tail -f logs/mcp_client.log
tail -f logs/kali_driver.log

# Test individual services
curl http://localhost:37695/health
curl http://localhost:25989/health
curl http://localhost:1611/health
```

## 🎉 Success Indicators

✅ All services running on correct ports  
✅ MCP tools available in Cursor  
✅ Test suite passes  
✅ Can create and execute tasks  
✅ Security tools accessible through containers  

---

*For additional help, see the [Troubleshooting Guide](TROUBLESHOOTING.md) or [AI Assistant Guide](AI_ASSISTANT_GUIDE.md).*
