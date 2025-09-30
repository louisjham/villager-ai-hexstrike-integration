#!/bin/bash

# Proper Villager Framework Startup Script
# This script starts Villager using its true architecture as shown in the diagram

echo "🏘️  Starting Proper Villager Framework"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "villager-venv-new" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating Villager virtual environment..."
source villager-venv-new/bin/activate

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

# Use Villager's built-in serve command
python -m interfaces.boot serve --host 0.0.0.0 --port 37695
