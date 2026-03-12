# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Commands

**Setup & Start:**
- `./scripts/setup.sh` - Full setup (creates venv, installs deps, configures env)
- `./scripts/start_villager_proper.sh` - Start all 4 services in correct order with health checks

**Testing:**
- `pytest tests/ -v --tb=short` - Run all tests
- `pytest tests/test_file.py::test_function_name -v` - Run single test
- `./tests/run_tests.sh` - Test runner script (checks for pytest first)

## Architecture

**Multi-service architecture (all must be running):**
- Port 37695: Villager Server (task management endpoints)
- Port 25989: MCP Client (bridges to external tools)
- Port 1611: Kali Driver (security tool execution via subprocess)
- Port 8080: Browser Service (automation)

**Service startup order matters** - start_villager_proper.sh waits for each service's `/health` endpoint before starting next.

## Project-Specific Requirements

**LLM Provider Configuration:**
- Primary: Z.AI (GLM-4.7/GLM-5) - Set `ZAI_API_KEY` in .env
- Backup: OpenRouter - Set `OPENROUTER_API_KEY` in .env
- Config.py sets `OPENAI_API_KEY` and `OPENAI_API_BASE` env vars regardless of provider (for LangChain compatibility)

**Path Handling:**
- Tests use `sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))` to import modules
- MCP server uses `VILLAGER_ROOT` env var or calculates from `__file__`
- Workspace defaults to `/tmp/villager_workspace` (override with `VILLAGER_WORKSPACE` env var)

**Service Communication:**
- All services communicate via HTTP (FastAPI)
- MCP Client escapes JSON responses for Villager compatibility
- Services log to `logs/` directory at project root

## Testing Patterns

- Tests use `pytest.skip()` when imports fail (don't fail the whole suite)
- `conftest.py` sets `PYTHONPATH` to include `src/` directory
- Mock subprocess for testing command execution

## MCP Integration

- MCP server runs via stdio (stdio_server) for Cursor integration
- MCP tools defined in `src/villager_ai/mcp/villager_proper_mcp.py`
- MCP Client service acts as bridge between Villager and external tools

## Security Notes

- Upstream Villager package contains hardcoded proxy credentials (NOT in this repo)
- This repo has been audited and cleaned of malicious endpoints
- Security tools execute as local subprocess calls (not Docker containers)
