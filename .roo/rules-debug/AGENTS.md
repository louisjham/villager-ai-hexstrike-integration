# AGENTS.md - Debug Mode

This file provides guidance to agents when debugging code in this repository.

## Debugging Services

**Service Health Checks:**
All services expose `/health` endpoint - use these to verify service is running:
```bash
curl http://localhost:37695/health  # Villager Server
curl http://localhost:25989/health  # MCP Client
curl http://localhost:1611/health   # Kali Driver
curl http://localhost:8080/health   # Browser Service
```

**Log Locations:**
Service logs are written to `logs/` directory at project root:
- `logs/villager_server.log` - Villager Server
- `logs/mcp_client.log` - MCP Client
- `logs/kali_driver.log` - Kali Driver
- `logs/browser_automation.log` - Browser Service

**Starting Services Manually for Debugging:**
```bash
# Start each service in separate terminal
python3 src/villager_ai/services/villager_server_simple.py
python3 src/villager_ai/services/mcp_service.py
python3 src/villager_ai/services/kali_driver_service.py
python3 src/villager_ai/services/browser_service.py
```

**Common Debug Issues:**

**Port Already in Use:**
```bash
# Find process using port
netstat -tlnp | grep :PORT

# Kill process (replace PID)
kill PID
```

**Import Errors:**
- Verify `PYTHONPATH` includes `src/` directory
- Run `pip3 install -r requirements.txt --user` to ensure all deps installed

**MCP Connection Issues:**
- Verify MCP Client is running on port 25989
- Check MCP Client log for connection errors
- Ensure `VILLAGER_ROOT` env var is set correctly

**LLM Provider Issues:**
- Check `.env` file exists and has `ZAI_API_KEY` or `OPENROUTER_API_KEY`
- Verify `LLM_PROVIDER` env var is set to 'zai' or 'openrouter'
- Check config.py sets `OPENAI_API_KEY` and `OPENAI_API_BASE` correctly

**Subprocess Execution Failures:**
- Check `VILLAGER_WORKSPACE` env var (defaults to `/tmp/villager_workspace`)
- Verify workspace directory exists and is writable
- Check command timeout (default 300s) - may need increase for long-running tools

**Silent Failures:**
- Services catch exceptions and return error responses instead of crashing
- Check service logs for error messages
- Add `print()` statements for debugging - output goes to log files

**Testing MCP Tools:**
```bash
# Test MCP server directly
python -m mcp.server.stdio src/villager_ai/mcp/villager_proper_mcp.py

# Test service endpoints directly
curl -X POST http://localhost:1611/ -H "Content-Type: application/json" -d '{"prompt": "test"}'
```

**Environment Variables for Debugging:**
```bash
# Set verbose logging
export LOG_LEVEL=DEBUG

# Enable all security flags
export ALLOW_SHELL=1
export ALLOW_APT=1
export ALLOW_WRITE=1
export ALLOW_BUILD=1

# Set workspace
export VILLAGER_WORKSPACE=/tmp/villager_workspace
```
