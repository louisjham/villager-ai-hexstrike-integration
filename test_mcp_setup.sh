#!/bin/bash

# Villager MCP Setup Test Script
# This script tests the complete MCP setup and provides diagnostic information

echo "🏘️ Villager MCP Setup Test"
echo "=========================="

# Check if we're in the right direc
if [ ! -f "src/villager_ai/mcp/villager_proper_mcp.py" ]; then
    echo "❌ Error: Please run this script from the Villager-AI directory"
    exit 1
fi

echo "✅ Running from correct directory"

# Check Python version
echo "🐍 Python version:"
python3 --version

# Check dependencies
echo "📦 Checking dependencies:"
python3 -c "
import sys
print(f'Python version: {sys.version}')

# Test core dependencies
try:
    import typer
    print('✅ typer imported successfully')
except ImportError as e:
    print(f'❌ typer import failed: {e}')

try:
    import click
    print('✅ click imported successfully')
except ImportError as e:
    print(f'❌ click import failed: {e}')

try:
    import mcp
    print('✅ mcp imported successfully')
except ImportError as e:
    print(f'❌ mcp import failed: {e}')

try:
    import fastapi
    print('✅ fastapi imported successfully')
except ImportError as e:
    print(f'❌ fastapi import failed: {e}')
"

# Test Villager imports
echo "🏘️ Testing Villager imports:"

# Get project root dynamically
SCRIPT_DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="\$SCRIPT_DIR"

python3 -c "
import sys
import os
project_root = os.path.abspath('.')
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src', 'villager_ai'))

print('Testing Villager core imports...')
try:
    from scheduler.core.init import global_llm
    print('✅ global_llm imported successfully')
except ImportError as e:
    print(f'❌ global_llm import failed: {e}')

try:
    from scheduler.core.mcp_client.mcp_client import McpClient
    print('✅ McpClient imported successfully')
except ImportError as e:
    print(f'❌ McpClient import failed: {e}')

try:
    from scheduler.core.tasks.task import TaskNode
    print('✅ TaskNode imported successfully')
except ImportError as e:
    print(f'❌ TaskNode import failed: {e}')

try:
    from config import MCP, Master
    print('✅ MCP, Master imported successfully')
except ImportError as e:
    print(f'❌ MCP, Master import failed: {e}')

print('Villager availability test complete!')
"

# Test MCP server startup
echo "🚀 Testing MCP server startup:"

# Get project root dynamically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

export VILLAGER_ROOT="$PROJECT_ROOT"
export PYTHONPATH="$PROJECT_ROOT"
export LLM_PROVIDER="${LLM_PROVIDER:-zai}"

# Security: Never hardcode API keys
if [ -z "$ZAI_API_KEY" ] && [ "$LLM_PROVIDER" = "zai" ]; then
    echo "⚠️  WARNING: ZAI_API_KEY not set. Using test mode."
    echo "   For production: export ZAI_API_KEY='your-key-here'"
    export ZAI_API_KEY="test-mode-placeholder"
fi

echo "Environment variables set:"
echo "  VILLAGER_ROOT: $VILLAGER_ROOT"
echo "  PYTHONPATH: $PYTHONPATH"
echo "  LLM_PROVIDER: $LLM_PROVIDER"
echo "  ZAI_API_KEY: [$([ -n "$ZAI_API_KEY" ] && echo "SET" || echo "NOT SET")]"

echo "Starting MCP server test (5 second timeout)..."
timeout 5 python src/villager_ai/mcp/villager_proper_mcp.py --debug 2>&1 | head -20

echo ""
echo "🎯 MCP Configuration for Cursor:"
echo "================================"
echo "Add this to your mcp_servers.json:"
echo ""
cat << EOF
{
  "mcpServers": {
    "villager-proper": {
      "command": "/usr/bin/python3",
      "args": [
        "$PROJECT_ROOT/src/villager_ai/mcp/villager_proper_mcp.py",
        "--debug"
      ],
      "description": "Villager AI Framework - AI-Driven Cybersecurity Automation",
      "timeout": 300,
      "alwaysAllow": [],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "VILLAGER_ROOT": "$PROJECT_ROOT",
        "PYTHONPATH": "$PROJECT_ROOT",
        "LLM_PROVIDER": "zai",
        "ZAI_API_KEY": "your-zai-api-key-here",
        "OPENROUTER_API_KEY": "your-openrouter-api-key-here"
      }
    }
  }
}
EOF

echo ""
echo "✅ Setup test complete!"
echo "If you see 'Villager Available: True' above, the MCP server is working correctly."
echo "Make sure to replace the API key placeholders with your actual Z.AI and OpenRouter API keys."
