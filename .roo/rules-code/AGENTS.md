# AGENTS.md - Code Mode

This file provides guidance to agents when writing code in this repository.

## Critical Coding Rules

**Service Startup Order:**
When adding new services to `start_villager_proper.sh`, you must:
1. Check if port is in use with `check_port()` function
2. Start service in background with `> logs/service_name.log 2>&1 &`
3. Capture PID for display
4. Wait for `/health` endpoint to respond (curl loop with timeout)
5. Only then proceed to next service

**Path Handling:**
- Always use relative paths from project root, not absolute paths
- For imports from tests: `sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))`
- For workspace: `WORKSPACE_DIR = os.getenv("VILLAGER_WORKSPACE", "/tmp/villager_workspace")`

**LLM Provider Integration:**
- Config.py sets `OPENAI_API_KEY` and `OPENAI_API_BASE` env vars for LangChain compatibility
- Don't use `os.environ['OPENAI_API_KEY']` directly - use `Master.api_key` from config
- Always check `LLM_PROVIDER` env var before using provider-specific settings

**MCP Tool Registration:**
- Tools must be registered with `ToolsManager().register_func(func_name)`
- MCP tools are defined in `src/villager_ai/mcp/villager_proper_mcp.py`
- Tool functions must return proper MCP response format with `TextContent`

**FastAPI Service Pattern:**
All services follow this pattern:
```python
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Service Name")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/")
async def handle_request(request: dict):
    # Process request
    return {"content": "response", "new_msg": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
```

**Subprocess Execution:**
- Use `execute_local()` from `kali_driver_service.py` for command execution
- Commands run in `WORKSPACE_DIR` with configurable timeout (default 300s)
- Returns dict with `success`, `stdout`, `stderr`, `returncode` keys

**Error Handling:**
- Services should catch exceptions and return error responses, not crash
- Use `try/except` blocks around external service calls
- Log errors to service-specific log file in `logs/` directory

**Environment Variables:**
- Load from `.env` file using `python-dotenv`
- All env vars should have defaults in config.py
- Security flags: `ALLOW_SHELL`, `ALLOW_APT`, `ALLOW_WRITE`, `ALLOW_BUILD` (default to '1')
