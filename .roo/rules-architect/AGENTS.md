# AGENTS.md - Architect Mode

This file provides guidance to agents when designing/architecting for this repository.

## Architectural Constraints

**Service Dependency Order:**
Services must be started in this specific order (enforced by `start_villager_proper.sh`):
1. MCP Client (port 25989) - First, as it's the bridge
2. Kali Driver (port 1611) - Second, external tool executor
3. Browser Service (port 8080) - Third, automation service
4. Villager Server (port 37695) - Last, depends on MCP Client

**Communication Pattern:**
- All services communicate via HTTP (FastAPI)
- MCP Client is the central bridge - all external tool access goes through it
- Villager Server → MCP Client → Kali Driver/Browser Service
- No direct communication between Kali Driver and Browser Service

**State Management:**
- Services are stateless (except for in-memory task tracking)
- Task state stored in `task_manager` dict in `villager_proper_mcp.py`
- No persistent storage - tasks lost on service restart
- Logs are the only persistent record of activity

**LLM Provider Architecture:**
- Dual-provider system: Z.AI (primary) + OpenRouter (backup)
- Failover logic exists but not fully implemented in current codebase
- Config.py sets `OPENAI_API_KEY` env var for LangChain compatibility
- Provider switching requires environment variable change + service restart

## Hidden Coupling

**Path Dependencies:**
- `VILLAGER_ROOT` env var must be set or calculated from `__file__`
- `sys.path` manipulation required for imports (not standard Python package structure)
- Tests rely on `PYTHONPATH` being set to include `src/`

**Port Hardcoding:**
- All service ports are hardcoded in code (37695, 25989, 1611, 8080)
- Changing ports requires modifying multiple files
- Port conflicts cause silent failures (services just don't start)

**Virtual Environment:**
- No longer required - using system Python3
- Dependencies installed via `pip3 install --user`

## Performance Considerations

**Subprocess Execution:**
- Security tools run via `subprocess.run()` with 300s default timeout
- Long-running tools (full scans, cracking) may timeout
- No async subprocess handling - blocks service during execution
- Consider increasing timeout or implementing async execution for long tasks

**MCP Streaming:**
- MCP Client handles streaming JSON responses
- Responses must be properly escaped for Villager compatibility
- Large responses may cause memory issues (no streaming to disk)

**Service Startup Latency:**
- Each service waits up to 10-15 seconds for `/health` endpoint
- Slow service startup causes entire stack to fail
- No retry logic for failed health checks

## Scalability Limitations

**Single-Instance Design:**
- Only one instance of each service can run (fixed ports)
- No horizontal scaling capability
- No load balancing between multiple instances

**No Service Discovery:**
- Service URLs hardcoded in config and code
- Adding/removing services requires code changes
- No dynamic service registration

**Task Queue:**
- Tasks execute synchronously (no queue)
- Concurrent tasks may cause race conditions
- No task prioritization or throttling

## Security Architecture

**Command Execution:**
- All commands run as the user running the service
- No sandboxing or containerization (refactored away from Docker)
- Security flags (`ALLOW_SHELL`, `ALLOW_APT`, etc.) are boolean checks only
- No audit logging of executed commands

**LLM Provider:**
- API keys stored in `.env` file (plaintext)
- No key rotation mechanism
- No request signing or encryption

**Network Exposure:**
- Services bind to `0.0.0.0` (all interfaces) by default
- No authentication or authorization on service endpoints
- Anyone who can reach the ports can execute commands

## Future Architecture Considerations

**Potential Improvements:**
1. Add service discovery (Consul, etcd)
2. Implement async subprocess execution
3. Add task queue (Celery, Redis)
4. Implement service authentication
5. Add persistent storage for tasks
6. Containerize services for isolation
7. Add health check retry logic
8. Implement proper failover between LLM providers
