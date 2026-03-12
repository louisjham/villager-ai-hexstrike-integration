#!/bin/bash

# Villager AI Setup Validation Script
# This script validates your Villager AI setup and provides specific fixes

echo "🏘️ Villager AI Setup Validation"
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track validation results
PASSED=0
FAILED=0

# Function to check and report
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ $2${NC}"
        ((FAILED++))
    fi
}

# Check 1: Python version
echo "🐍 Checking Python version..."
python3 --version | grep -q "Python 3\.[8-9]\|Python 3\.1[0-9]"
check_status $? "Python 3.8+ installed"

# Check 2: Security tools (optional, informational)
echo "🔧 Checking security tools..."
tools_found=0
for tool in nmap sqlmap hydra nikto john; do
    if command -v "$tool" > /dev/null 2>&1; then
        tools_found=$((tools_found + 1))
    fi
done
if [ $tools_found -gt 0 ]; then
    echo -e "${GREEN}✅ $tools_found security tools available${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  No security tools found (optional — install with apt)${NC}"
fi

# Check 3: Dependencies
echo "🔍 Checking dependencies..."
python3 -c "import typer, click, mcp, fastapi" > /dev/null 2>&1
check_status $? "Core dependencies installed"

# Check 4: Villager imports
echo "🏘️ Checking Villager imports..."
python3 -c "
import sys
sys.path.append('.')
sys.path.append('src/villager_ai')
from scheduler.core.init import global_llm
from scheduler.core.mcp_client.mcp_client import McpClient
from config import MCP, Master
" > /dev/null 2>&1
check_status $? "Villager modules importable"

# Check 5: MCP server startup
echo "🚀 Testing MCP server startup..."
export PYTHONPATH="$(pwd)"
export LLM_PROVIDER="zai"
export ZAI_API_KEY="test-key"

timeout 5 python3 src/villager_ai/mcp/villager_proper_mcp.py --debug 2>&1 | grep -q "Villager Available: True"
check_status $? "MCP server starts correctly"

# Check 7: Services (optional - only check if running)
echo "🌐 Checking services (optional)..."
curl -s http://localhost:37695/health > /dev/null 2>&1
villager_server=$?

curl -s http://localhost:25989/health > /dev/null 2>&1
mcp_client=$?

curl -s http://localhost:1611/health > /dev/null 2>&1
kali_driver=$?

curl -s http://localhost:8080/health > /dev/null 2>&1
browser_service=$?

if [ $villager_server -eq 0 ] && [ $mcp_client -eq 0 ] && [ $kali_driver -eq 0 ] && [ $browser_service -eq 0 ]; then
    echo -e "${GREEN}✅ All services running${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  Services not running (optional - run ./scripts/start_villager_proper.sh)${NC}"
    # Don't count this as a failure since it's optional
fi

# Summary
echo ""
echo "📊 Validation Summary"
echo "===================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed! Your Villager AI setup is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Configure MCP in Cursor with the provided mcp_servers.json"
    echo "2. Start services: ./scripts/start_villager_proper.sh"
    echo "3. Test in Cursor: mcp_villager-proper_get_system_status()"
else
    echo -e "${YELLOW}⚠️  Some checks failed. See fixes below:${NC}"
    echo ""
    
    # Provide specific fixes
    if ! python3 --version | grep -q "Python 3\.[8-9]\|Python 3\.1[0-9]"; then
        echo "🔧 Fix Python version:"
        echo "   Install Python 3.8+ from python.org or your package manager"
    fi
    
    if ! python3 -c "import typer, click, mcp, fastapi" > /dev/null 2>&1; then
        echo "🔧 Fix Python dependencies:"
        echo "   pip3 install -r requirements.txt --user"
    fi
    
    echo ""
    echo "📚 For detailed troubleshooting, see: docs/TROUBLESHOOTING.md"
fi

echo ""
echo "🔗 MCP Configuration for Cursor:"
echo "================================"
echo "Add this to your mcp_servers.json:"
echo ""
cat << 'EOF'
{
  "mcpServers": {
    "villager-proper": {
      "command": "/usr/bin/python3",
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
        "LLM_PROVIDER": "zai",
        "ZAI_API_KEY": "your-zai-api-key-here",
        "OPENROUTER_API_KEY": "your-openrouter-api-key-here"
      }
    }
  }
}
EOF

echo ""
echo "💡 Remember to replace '/path/to/your/Villager-AI' with your actual path!"
