# System Requirements

## Quick Setup

```bash
# One-command installation
sudo apt update && sudo apt upgrade -y && \
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && \
sudo usermod -aG docker $USER && \
sudo apt install -y kali-linux-everything python3-dev python3-pip python3-venv build-essential && \
curl -fsSL https://ollama.ai/install.sh | sh && \
ollama pull deepseek-r1-uncensored && \
ollama serve & && \
git clone https://github.com/YOUR_USERNAME/villager-ai.git && \
cd villager-ai && \
python3 -m venv villager-venv-new && \
source villager-venv-new/bin/activate && \
pip install -r requirements.txt && \
cp .env.example .env && \
./scripts/setup.sh && \
./scripts/start_villager_proper.sh && \
sleep 30 && \
./tests/run_tests.sh
```

**Note**: Log out and back in after Docker installation.

## Requirements

### System Dependencies
- **Docker** - For containerized security tools
- **Kali Linux tools** - msfvenom, nmap, sqlmap, etc.
- **Ollama** - For local AI models
- **Python 3.8+** - (3.13 recommended)

### Installation Commands
```bash
# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Kali tools
sudo apt install -y kali-linux-everything

# Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull deepseek-r1-uncensored
ollama serve &

# Python dependencies
sudo apt install -y python3-dev python3-pip python3-venv build-essential
```

## Manual Setup

If the quick setup fails:

1. **Install system dependencies** (Docker, Kali tools, Ollama)
2. **Clone repository**: `git clone https://github.com/YOUR_USERNAME/villager-ai.git`
3. **Setup Python**: `python3 -m venv villager-venv-new && source villager-venv-new/bin/activate`
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Configure**: `cp .env.example .env`
6. **Start services**: `./scripts/start_villager_proper.sh`
7. **Test**: `./tests/run_tests.sh`

## Architecture

**4 Core Services:**
- Villager Server (37695) - Task management
- MCP Client (25989) - Service communication  
- Kali Driver (1611) - Security tools
- Browser Automation (8080) - Web automation

**Key Features:**
- AI-driven task decomposition
- Containerized security tools (MSFVenom, Nmap, SQLMap, etc.)
- 24-hour self-destruct containers
- MCP integration for tool access

## Troubleshooting

**Docker not available:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in
```

**msfvenom not found:**
```bash
sudo apt install -y kali-linux-everything
```

**Services not running:**
```bash
./scripts/start_villager_proper.sh
# Wait 30 seconds, then test
```

**Ollama not available:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull deepseek-r1-uncensored
ollama serve &
```

## Expected Results

After setup, all tests should pass:
- ✅ Environment Setup
- ✅ Villager Imports  
- ✅ MCP Server
- ✅ Security Tools (msfvenom available)
- ✅ Docker Availability
- ✅ Complete Workflow
