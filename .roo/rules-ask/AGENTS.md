# AGENTS.md - Ask Mode

This file provides guidance to agents when answering questions about this repository.

## Architecture Context

**Counterintuitive Organization:**
- `src/villager_ai/` contains the main application code (not just AI logic)
- `src/villager_ai/services/` contains all 4 microservices (not just helper utilities)
- `src/villager_ai/mcp/` contains MCP server implementation (not just client code)
- Tests are in `tests/` directory, not `src/tests/`

**Service Architecture (4 independent services):**
1. **Villager Server** (port 37695) - Main task management API
2. **MCP Client** (port 25989) - Bridges to external tools, handles streaming
3. **Kali Driver** (port 1611) - Executes security tools via subprocess
4. **Browser Service** (port 8080) - Browser automation

**Data Flow:**
```
Cursor MCP → Villager MCP Server → Villager Server → MCP Client → Kali Driver/Browser
```

**Key Configuration Files:**
- `.env` - Environment variables (copy from `.env.example`)
- `src/villager_ai/config.py` - LLM provider config, Master/MCP classes
- `src/villager_ai/services/README.md` - Service architecture documentation

**Documentation Location:**
- `docs/SETUP_GUIDE.md` - Complete setup instructions
- `docs/AI_ASSISTANT_GUIDE.md` - How AI should use Villager vs HexStrike
- `docs/TROUBLESHOOTING.md` - Common issues and solutions
- `docs/KALI_CONTAINER_SETUP.md` - Kali container setup (legacy, not used in current version)

## Misleading Names/Patterns

**"Villager MCP" is not a client:**
- Villager operates as an MCP SERVER (exposes tools to Cursor)
- MCP Client service (port 25989) is a separate microservice
- This is confusing but intentional - Villager provides tools via MCP protocol

**"Kali Driver" doesn't use Kali containers:**
- Executes commands directly on local system (WSL/Linux)
- Security tools (msfvenom, nmap, etc.) must be installed locally
- Originally designed for Docker containers, refactored for native execution

**Virtual environment:**
- No longer required - using system Python3
- Dependencies installed via `pip3 install --user`

## Important Context

**LLM Provider Setup:**
- Primary: Z.AI (GLM-4.7/GLM-5) - requires API key from https://z.ai/manage-apikey/apikey-list
- Backup: OpenRouter - requires API key from https://openrouter.ai/keys
- Config.py sets `OPENAI_API_KEY` env var regardless of provider (for LangChain compatibility)

**Security Tools:**
- Tools like msfvenom, nmap, sqlmap must be installed on local system
- `setup.sh` attempts to install some tools via apt
- Metasploit (msfvenom) may need manual installation

**HexStrike Integration:**
- Villager AI and HexStrike are separate tools
- AI assistant chooses which to use based on task complexity
- HexStrike is NOT controlled by Villager - they work in parallel
- See `docs/AI_ASSISTANT_GUIDE.md` for decision logic

**Testing:**
- Tests use `pytest.skip()` when imports fail (graceful degradation)
- `conftest.py` sets `PYTHONPATH` to include `src/` directory
- Run tests from project root: `pytest tests/ -v`

**Environment Variables:**
- `.env` file is not in git (see `.gitignore`)
- Copy `.env.example` to `.env` and configure
- Required: `ZAI_API_KEY` or `OPENROUTER_API_KEY`
- Optional: `GITHUB_TOKEN`, `VILLAGER_WORKSPACE`, `LOG_LEVEL`
