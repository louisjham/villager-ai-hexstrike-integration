# System Requirements for Villager AI Framework

## 🚨 **Why Tests Fail on First Install**

The test failures your friend is seeing are **expected** on a fresh installation. These tests require system-level dependencies that aren't Python packages.

## 📋 **System Dependencies Required**

### **1. Docker (Required)**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
```

### **2. Kali Linux Tools (Required)**
```bash
# Install Kali Linux tools (Ubuntu/Debian)
sudo apt update
sudo apt install -y kali-linux-everything

# Or install specific tools
sudo apt install -y metasploit-framework nmap gobuster nikto sqlmap hydra john hashcat

# Verify msfvenom
msfvenom --help
```

### **3. Ollama (Required for AI)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the AI model
ollama pull deepseek-r1-uncensored

# Start Ollama
ollama serve &
```

### **4. Python System Dependencies**
```bash
# Install Python build dependencies
sudo apt install -y python3-dev python3-pip python3-venv build-essential

# Install additional system packages
sudo apt install -y git curl wget unzip
```

## 🔧 **Complete Setup Process**

### **Step 1: System Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

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

### **Step 2: Python Setup**
```bash
# Clone repository
git clone https://github.com/Yenn503/villager-ai-hexstrike-integration.git
cd villager-ai-hexstrike-integration

# Create virtual environment
python3 -m venv villager-venv-new
source villager-venv-new/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### **Step 3: Start Services**
```bash
# Start all services
./start_villager_proper.sh

# Wait for services to start (30 seconds)
sleep 30

# Run tests
./tests/run_tests.sh
```

## ✅ **Expected Test Results After Complete Setup**

After installing all system dependencies and starting services:

- ✅ **Environment Setup**: PASSED
- ✅ **Villager Imports**: PASSED  
- ✅ **MCP Server**: PASSED
- ✅ **LLM Provider**: PASSED
- ✅ **Tool Execution**: PASSED
- ✅ **Security Tools**: PASSED (msfvenom available)
- ✅ **GitHub Integration**: PASSED
- ✅ **Docker Availability**: PASSED
- ✅ **New Workflow Services**: PASSED (services running)
- ✅ **Complete Workflow**: PASSED
- ✅ **RAT Payload Generation**: PASSED
- ✅ **MCP Tools Integration**: PASSED

## 🚨 **Common Issues & Solutions**

### **Issue: "Docker not available"**
```bash
# Solution: Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in, then test: docker --version
```

### **Issue: "msfvenom not found"**
```bash
# Solution: Install Kali tools
sudo apt install -y kali-linux-everything
# Or specific: sudo apt install -y metasploit-framework
```

### **Issue: "Services not running"**
```bash
# Solution: Start services first
./start_villager_proper.sh
# Wait 30 seconds, then run tests
```

### **Issue: "Ollama not available"**
```bash
# Solution: Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull deepseek-r1-uncensored
ollama serve &
```

## 📝 **Quick Fix for Your Friend**

Send them this one-command setup:

```bash
# Complete system setup
sudo apt update && sudo apt upgrade -y && \
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && \
sudo usermod -aG docker $USER && \
sudo apt install -y kali-linux-everything python3-dev python3-pip python3-venv build-essential && \
curl -fsSL https://ollama.ai/install.sh | sh && \
ollama pull deepseek-r1-uncensored && \
ollama serve & && \
git clone https://github.com/Yenn503/villager-ai-hexstrike-integration.git && \
cd villager-ai-hexstrike-integration && \
python3 -m venv villager-venv-new && \
source villager-venv-new/bin/activate && \
pip install -r requirements.txt && \
cp .env.example .env && \
./start_villager_proper.sh && \
sleep 30 && \
./tests/run_tests.sh
```

**Note**: They'll need to log out and back in after Docker installation for the docker group to take effect.
