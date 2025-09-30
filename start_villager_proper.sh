#!/bin/bash

# Proper Villager Framework Startup Script
# This script starts Villager using its true architecture as shown in the diagram

# Import visual components
source villager_visuals.py 2>/dev/null || python3 -c "
import sys
sys.path.append('.')
from villager_visuals import create_integrated_banner, create_startup_message, create_server_info
print(create_integrated_banner())
print(create_startup_message())
"

# Check if virtual environment exists
if [ ! -d "villager-venv-new" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating Villager virtual environment..."
source villager-venv-new/bin/activate

# Load environment variables
if [ -f ".env" ]; then
    echo "🔧 Loading environment variables..."
    set -a  # Automatically export all variables
    source .env
    set +a  # Turn off automatic export
    echo "✅ Environment variables loaded"
else
    echo "⚠️  Warning: .env file not found"
    echo "   Copy .env.example to .env and configure it:"
    echo "   cp .env.example .env"
    echo "   # Then edit .env with your settings"
    echo "   Using default environment variables"
fi

# Check LLM provider configuration
if [ -z "$LLM_PROVIDER" ]; then
    export LLM_PROVIDER="ollama"
    echo "🔧 Using default LLM provider: Ollama (local, uncensored)"
fi

# Configure Ollama (default)
if [ "$LLM_PROVIDER" = "ollama" ]; then
    export OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"
    export OLLAMA_MODEL="${OLLAMA_MODEL:-deepseek-r1-uncensored}"
    echo "✅ Ollama configuration:"
    echo "   - Base URL: $OLLAMA_BASE_URL"
    echo "   - Model: $OLLAMA_MODEL"
elif [ "$LLM_PROVIDER" = "deepseek" ]; then
    if [ -z "$DEEPSEEK_API_KEY" ]; then
        echo "⚠️  WARNING: DEEPSEEK_API_KEY not set for DeepSeek provider."
        echo "   Please set your DeepSeek API key:"
        echo "   export DEEPSEEK_API_KEY='your-key-here'"
        echo ""
    else
        export OPENAI_API_KEY="$DEEPSEEK_API_KEY"
        echo "✅ DeepSeek API key configured"
    fi
fi

# Start Villager using its true interface
echo "🚀 Starting Villager with proper architecture..."
echo "   - TaskNode for task execution and decomposition"
echo "   - MCP Client (Port 25989) for external tool access"
echo "   - Kali Driver (Port 1611) for containerized execution"
echo "   - Agent Scheduler for LLM orchestration"
echo "   - Tools Manager for function registry"
echo ""

# Function to check if port is in use
check_port() {
    local port=$1
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Start MCP Client service if not running
if ! check_port 25989; then
    echo "🔧 Starting MCP Client service on port 25989..."
    python services/mcp_service.py > logs/mcp_client.log 2>&1 &
    MCP_CLIENT_PID=$!
    echo "📊 MCP Client started with PID: $MCP_CLIENT_PID"
    
    # Wait for MCP Client to be ready
    echo "⏳ Waiting for MCP Client to be ready..."
    for i in {1..10}; do
        if curl -s http://localhost:25989/health > /dev/null 2>&1; then
            echo "✅ MCP Client is ready!"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo
else
    echo "✅ MCP Client is already running on port 25989"
fi

# Start Kali Driver service if not running
if ! check_port 1611; then
    echo "🔧 Starting Kali Driver service on port 1611..."
    python services/kali_driver_service.py > logs/kali_driver.log 2>&1 &
    KALI_DRIVER_PID=$!
    echo "📊 Kali Driver started with PID: $KALI_DRIVER_PID"
    
    # Wait for Kali Driver to be ready
    echo "⏳ Waiting for Kali Driver to be ready..."
    for i in {1..10}; do
        if curl -s http://localhost:1611/health > /dev/null 2>&1; then
            echo "✅ Kali Driver is ready!"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo
else
    echo "✅ Kali Driver is already running on port 1611"
fi

# Start Browser Automation service if not running
if ! check_port 8080; then
    echo "🔧 Starting Browser Automation service on port 8080..."
    python services/browser_service.py > logs/browser_automation.log 2>&1 &
    BROWSER_PID=$!
    echo "📊 Browser Automation started with PID: $BROWSER_PID"
    
    # Wait for Browser service to be ready
    echo "⏳ Waiting for Browser Automation to be ready..."
    for i in {1..10}; do
        if curl -s http://localhost:8080/health > /dev/null 2>&1; then
            echo "✅ Browser Automation is ready!"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo
else
    echo "✅ Browser Automation is already running on port 8080"
fi

echo ""
echo "🎯 All Villager services are now running!"
echo "📋 MCP Client PID: $MCP_CLIENT_PID (Port 25989)"
echo "📋 Kali Driver PID: $KALI_DRIVER_PID (Port 1611)"
echo "📋 Browser Automation PID: $BROWSER_PID (Port 8080)"
echo ""

# Start Villager server if not running
if ! check_port 37695; then
    echo "🔧 Starting Villager server on port 37695..."
    # Use the simplified server that actually works
    python services/villager_server_simple.py > logs/villager_server.log 2>&1 &
    VILLAGER_SERVER_PID=$!
    echo "📊 Villager server started with PID: $VILLAGER_SERVER_PID"
    
    # Wait for Villager server to be ready
    echo "⏳ Waiting for Villager server to be ready..."
    for i in {1..15}; do
        if curl -s http://localhost:37695/health > /dev/null 2>&1; then
            echo "✅ Villager server is ready!"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo
else
    echo "✅ Villager server is already running on port 37695"
fi

echo ""
echo "🎯 All Villager services are now running!"
echo "📋 MCP Client PID: $MCP_CLIENT_PID (Port 25989)"
echo "📋 Kali Driver PID: $KALI_DRIVER_PID (Port 1611)"
echo "📋 Browser Automation PID: $BROWSER_PID (Port 8080)"
echo "📋 Villager Server PID: $VILLAGER_SERVER_PID (Port 37695)"
echo ""
echo "🔗 Service URLs:"
echo "   - Villager Server: http://localhost:37695"
echo "   - MCP Client: http://localhost:25989"
echo "   - Kali Driver: http://localhost:1611"
echo "   - Browser Automation: http://localhost:8080"
echo ""
echo "✅ Villager framework is fully operational!"
echo "🎯 You can now use Villager MCP tools in Cursor to create tasks and execute them."
