#!/bin/bash

# Villager Startup Script
echo "🚀 Starting Villager AI Penetration Testing Framework..."
echo "=" * 60

# Activate the virtual environment
source /home/yenn/Villager-AI/villager-venv-new/bin/activate

# Set environment variables
export VILLAGER_BASE_URL="http://127.0.0.1:37695"
export ALLOW_SHELL="1"
export ALLOW_APT="1"
export ALLOW_WRITE="1"
export ALLOW_BUILD="1"
export PYTHONUNBUFFERED="1"

# Set DeepSeek API key
# API Keys - Set these in your environment or .env file
# export DEEPSEEK_API_KEY="your-api-key-here"
# export OPENAI_API_KEY="your-api-key-here"

# Start the Villager FastAPI server
echo "🌐 Starting Villager FastAPI server on port 37695..."
cd /home/yenn/Villager-AI
python villager_server.py