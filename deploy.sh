#!/bin/bash

# Villager AI Secure Deployment Script
# This script ensures proper security setup before deployment

set -e  # Exit on any error

echo "🔒 Villager AI Secure Deployment Script"
echo "======================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Creating .env file from template..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env file created from .env.example"
        echo "🔑 Please edit .env file and add your API key:"
        echo "   nano .env"
        echo ""
        echo "❌ Deployment aborted. Please configure .env file first."
        exit 1
    else
        echo "❌ .env.example not found. Cannot create .env file."
        exit 1
    fi
fi

# Check if API key is set
if ! grep -q "DEEPSEEK_API_KEY=your-deepseek-api-key-here" .env && ! grep -q "DEEPSEEK_API_KEY=$" .env; then
    echo "✅ API key appears to be configured in .env"
else
    echo "⚠️  API key not configured in .env file!"
    echo "🔑 Please edit .env file and add your actual API key:"
    echo "   nano .env"
    echo ""
    echo "❌ Deployment aborted. Please configure API key first."
    exit 1
fi

# Check for hardcoded API keys in source code (excluding local .env files)
echo "🔍 Checking for hardcoded API keys in source code..."
if grep -r "sk-[a-zA-Z0-9]\{20,\}" . --exclude-dir=villager-venv-new --exclude-dir=.git --exclude="*.log" --exclude=".env" 2>/dev/null; then
    echo "❌ Hardcoded API keys found in source code!"
    echo "🔒 Please remove all hardcoded API keys before deployment."
    exit 1
else
    echo "✅ No hardcoded API keys found in source code"
fi

# Check if .gitignore includes .env
if [ -f ".gitignore" ] && grep -q "\.env" .gitignore; then
    echo "✅ .env files are properly excluded from Git"
else
    echo "⚠️  .env files may not be excluded from Git"
    echo "📝 Adding .env to .gitignore..."
    echo ".env" >> .gitignore
    echo "✅ .env added to .gitignore"
fi

# Check Docker setup
if [ -f "deploy/Dockerfile" ]; then
    echo "✅ Docker configuration found"
    
    # Check if Dockerfile has hardcoded secrets
    if grep -q "sk-[a-zA-Z0-9]\{20,\}" deploy/Dockerfile 2>/dev/null; then
        echo "❌ Hardcoded API keys found in Dockerfile!"
        echo "🔒 Please remove hardcoded API keys from Dockerfile."
        exit 1
    else
        echo "✅ Dockerfile is secure (no hardcoded secrets)"
    fi
else
    echo "⚠️  Docker configuration not found"
fi

# Check Docker Compose setup
if [ -f "deploy/docker-compose.yml" ]; then
    echo "✅ Docker Compose configuration found"
    
    # Check if docker-compose.yml has hardcoded secrets
    if grep -q "sk-[a-zA-Z0-9]\{20,\}" deploy/docker-compose.yml 2>/dev/null; then
        echo "❌ Hardcoded API keys found in docker-compose.yml!"
        echo "🔒 Please remove hardcoded API keys from docker-compose.yml."
        exit 1
    else
        echo "✅ docker-compose.yml is secure (no hardcoded secrets)"
    fi
else
    echo "⚠️  Docker Compose configuration not found"
fi

echo ""
echo "🎉 Security checks passed!"
echo "🚀 Ready for deployment"
echo ""
echo "📋 Next steps:"
echo "1. Review SECURITY.md for additional security guidelines"
echo "2. Test deployment in a safe environment first"
echo "3. Monitor logs and access patterns after deployment"
echo "4. Regularly rotate API keys"
echo ""
echo "🔒 Security is everyone's responsibility!"
