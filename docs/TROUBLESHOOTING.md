# Villager AI Framework - Troubleshooting Guide

This guide helps you resolve common issues with the Villager AI framework.

## 🚨 Critical Fix: MCP Tool Loading Order

**Problem**: HexStrike has ~150+ tools which can overwhelm Cursor's MCP loading, potentially preventing Villager tools from being visible.

**Solution**: Put Villager FIRST in your MCP config and ensure proper PYTHONPATH.

### Fixed MCP Configuration

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
2. **PYTHONPATH is set** - Points to Villager repo root for proper module resolution
3. **Cloud LLM first** - Uses DeepSeek API by default (no local RAM required)
4. **Correct paths** - Use actual paths to your installations

##  Docker Permission Denied Errors 

**ERROR MESSAGE**: `permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock`

### Why this might happen 


1. **User not in docker group** - The Docker socket (`/var/run/docker.sock`) requires special permissions
2. **Fresh install** - Default Docker installation doesn't add users to the docker group automatically
3. **Session not refreshed** - Even after adding to docker group, current shell sessions don't pick up the change
4. **Different Linux distributions** - Some distros (Debian, Ubuntu, Kali) have stricter default permissions

### Complete Fix (Choose ONE method)

#### Method 1: Add User to Docker Group (RECOMMENDED)

This is the permanent solution that most users should use:

```bash
# Step 1: Add your user to the docker group
sudo usermod -aG docker $USER

# Step 2: Apply group changes (choose ONE)
# Option A: Log out and log back in (most reliable)
#   - Close all terminals
#   - Log out of your session
#   - Log back in

# Option B: Use newgrp (for current terminal only)
newgrp docker

# Option C: Reboot (guaranteed to work)
sudo reboot

# Step 3: Verify it worked
groups  # Should show "docker" in the list
docker ps  # Should work without sudo

# Step 4: Test with Villager
./scripts/test_villager_setup.sh
```

#### Method 2: Quick Temporary Fix (NOT RECOMMENDED FOR PRODUCTION)

If you just want to test quickly (not secure for long-term use):

```bash
# Make Docker socket accessible (temporary - resets on reboot)
sudo chmod 666 /var/run/docker.sock

# Test it works
docker ps

# Run setup
./scripts/setup.sh
```

**⚠️ WARNING**: This makes Docker accessible to ALL users on the system. Only use for testing!

#### Method 3: Use sudo (LEAST PREFERRED)

If you can't modify groups, run setup with sudo:

```bash
# Run setup with sudo
sudo ./scripts/setup.sh

# Run services with sudo
sudo ./scripts/start_villager_proper.sh
```

**⚠️ WARNING**: This can cause permission issues with files created by root.

### Verification Steps

After applying the fix, verify everything works:

```bash
# 1. Check Docker access (should work WITHOUT sudo)
docker ps
docker images

# 2. Check group membership
groups | grep docker  # Should show "docker"
id -nG | grep docker  # Alternative check

# 3. Test Docker pull
docker pull hello-world

# 4. Test Kali image
docker pull kalilinux/kali-rolling

# 5. Run Villager test script
./scripts/test_villager_setup.sh
```

### Still Not Working?

If you've tried the above and it's still not working:

```bash
# Check Docker daemon status
sudo systemctl status docker
sudo systemctl start docker

# Check socket permissions
ls -l /var/run/docker.sock
# Should show: srw-rw---- 1 root docker

# Fix socket ownership if needed
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

# Restart Docker daemon
sudo systemctl restart docker

# Check Docker service logs
journalctl -u docker --no-pager | tail -50

# Verify Docker info
docker info
```

### Why Some Users Get This Error and Others Don't

1. **Fresh vs Configured Systems**:
   - Fresh Linux install = Needs docker group setup
   - Pre-configured systems (some cloud VMs) = Docker group already set up

2. **Installation Method**:
   - Package manager (apt/yum) = Requires manual group setup
   - Docker Desktop = Handles permissions automatically
   - Snap installation = May have different permission model

3. **Distribution Differences**:
   - **Ubuntu/Debian**: Requires `usermod -aG docker $USER`
   - **Fedora/RHEL**: Same requirement
   - **Arch**: Explicitly requires group addition
   - **Kali Linux**: Default user often needs docker group added

4. **User Account Type**:
   - **Sudo/Admin users**: Can add themselves to docker group
   - **Limited users**: May need admin help
   - **Root user**: No permission issues (but not recommended)

### For Community Project Maintainers

To help users avoid this issue, consider:

1. **Setup Script Enhancement**: Add automatic docker group check/addition to `setup.sh`
2. **Clear Documentation**: Put Docker permissions at the top of setup guides
3. **Error Messages**: Detect permission errors and show the fix automatically
4. **Pre-flight Checks**: Test Docker access before starting installation

## 🔍 Common Issues and Solutions

### 1. Villager Tools Not Available in Cursor

**Symptoms**: Villager MCP tools don't appear in available tools list

**Solutions**:
```bash
# 1. Check MCP config order
# Ensure Villager comes before HexStrike in mcp_servers.json

# 2. Verify PYTHONPATH
export PYTHONPATH="/path/to/your/Villager-AI"

# 3. Restart Cursor completely
# Close Cursor, reopen, wait for MCP servers to initialize

# 4. Test MCP server directly
python /path/to/your/Villager-AI/src/villager_ai/mcp/villager_proper_mcp.py --debug
```

### 2. Services Not Starting

**Symptoms**: Services fail to start or show connection errors

**Solutions**:
```bash
# Check if ports are already in use
lsof -i -P -n | grep LISTEN | grep -E "(25989|1611|37695|8080)"

# Kill existing processes
pkill -f "python.*services"

# Restart all services
./scripts/start_villager_proper.sh

# Check service logs
tail -f logs/villager_server.log
tail -f logs/mcp_client.log
tail -f logs/kali_driver.log
```

### 3. Docker Image Pull Issues

**Symptoms**: Timeout errors when pulling Docker images

**Common Causes**:
- Network connectivity issues or slow connection
- DNS resolution problems
- Docker daemon issues
- Geographic restrictions or firewall blocking

**Solutions**:
```bash
# 1. Check Docker daemon status
sudo systemctl status docker
sudo systemctl start docker

# 2. Test Docker connectivity
docker pull hello-world

# 3. Pull standard Kali image
docker pull kalilinux/kali-rolling

# 4. Configure Docker for better performance
sudo systemctl edit docker
# Add: [Service] ExecStart= ExecStart=/usr/bin/dockerd --max-concurrent-downloads=1
sudo systemctl restart docker
```

**Note**: Villager uses the standard `kalilinux/kali-rolling` image which provides all necessary security tools.

### 4. Docker Container Issues

**Symptoms**: Container creation fails or commands don't execute

**Solutions**:
```bash
# Check Docker daemon status
sudo systemctl status docker
sudo systemctl start docker

# Check Docker group membership
sudo usermod -aG docker $USER
# Log out and back in

# Check available images
docker images

# Test Docker access
docker run hello-world

# Pull standard Kali image
docker pull kalilinux/kali-rolling
```

### 4. Ollama/AI Model Issues

**Symptoms**: AI tasks fail or LLM not responding

**Solutions**:
```bash
# Check Ollama status
ollama list
ollama serve &

# Test model availability
ollama run deepseek-r1-uncensored

# Check environment variables
echo $LLM_PROVIDER
echo $OLLAMA_BASE_URL
echo $OLLAMA_MODEL

# Restart Ollama
pkill ollama
ollama serve &
```

### 5. Python Import Errors

**Symptoms**: ModuleNotFoundError or import failures

**Solutions**:
```bash
# Check virtual environment
source villager-venv-new/bin/activate
which python

# Check PYTHONPATH
export PYTHONPATH="/path/to/your/Villager-AI"
echo $PYTHONPATH

# Reinstall dependencies
pip install -r requirements.txt

# Test imports
python -c "from scheduler.core.init import global_llm; print('✅ Villager imports working')"
```

## 🔧 Debug Commands

### Service Health Checks
```bash
# Check all services
curl http://localhost:37695/health  # Villager Server
curl http://localhost:25989/health  # MCP Client
curl http://localhost:1611/health   # Kali Driver
curl http://localhost:8080/health   # Browser Service

# Check service processes
ps aux | grep -E "(villager|mcp|kali)" | grep -v grep

# Check port usage
netstat -tlnp | grep -E "(25989|1611|37695|8080)"
```

### MCP Testing
```python
# Test MCP connection in Cursor
mcp_villager-proper_get_system_status()

# Test task creation
mcp_villager-proper_create_task(
    abstract="Test Task",
    description="Simple test task",
    verification="Task completed"
)

# Test tool execution
mcp_villager-proper_execute_tool(
    tool_name="pyeval",
    parameters={"python_codeblock": "print('Hello from Villager!')"}
)
```

## 🚨 Emergency Recovery

### Complete Reset
```bash
# Stop all services
pkill -f "python.*services"
pkill ollama

# Clean up containers
docker stop $(docker ps -q) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null

# Restart Docker
sudo systemctl restart docker

# Restart Ollama
ollama serve &

# Restart Villager
./scripts/start_villager_proper.sh
```

### Log Analysis
```bash
# Check recent errors
grep -i error logs/*.log

# Monitor real-time logs
tail -f logs/villager_server.log | grep -i error

# Check system logs
journalctl -u docker
```

## 📊 Performance Optimization

### Memory Usage
```bash
# Monitor memory usage
htop
free -h

# Check Docker memory usage
docker stats

# Limit container memory if needed
docker run -m 2g kalilinux/kali-rolling
```

## 📞 Getting Help

### Diagnostic Information
When reporting issues, include:

```bash
# System information
uname -a
docker --version
python --version

# Service status
./tests/run_tests.sh

# Configuration
cat mcp_servers.json

# Recent logs
tail -50 logs/villager_server.log
```

### Common Solutions Summary

| Issue | Quick Fix |
|-------|-----------|
| Tools not visible | Put Villager first in MCP config, restart Cursor |
| Services not starting | Check ports, restart Docker, run startup script |
| Container failures | Check Docker daemon, verify image availability |
| AI not responding | Restart Ollama, check model availability |
| Import errors | Check PYTHONPATH, reinstall dependencies |
| Task failures | Check service connectivity, review logs |

---

*For setup instructions, see the [Setup Guide](SETUP_GUIDE.md). For AI integration, see the [AI Assistant Guide](AI_ASSISTANT_GUIDE.md).*
