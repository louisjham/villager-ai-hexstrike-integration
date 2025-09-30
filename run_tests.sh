#!/bin/bash

# Villager AI Framework - Test Runner
# ===================================
# This script runs the comprehensive test suite to verify
# that all components are properly connected and working.

echo "🏘️ Villager AI Framework - Test Runner"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "test_villager_framework.py" ]; then
    echo "❌ Error: test_villager_framework.py not found"
    echo "   Please run this script from the Villager-AI directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "villager-venv-new" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "   Please run setup first: python -m venv villager-venv-new"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source villager-venv-new/bin/activate

# Load environment variables
if [ -f ".env" ]; then
    echo "🔧 Loading environment variables..."
    source .env
else
    echo "⚠️  Warning: .env file not found"
    echo "   Using default environment variables"
fi

# Run the test suite
echo "🧪 Running comprehensive test suite..."
echo ""
python3 test_villager_framework.py

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 All tests passed! Framework is ready to use."
    echo ""
    echo "Next steps:"
    echo "  • Start Villager: ./start_villager_proper.sh"
    echo "  • Or run MCP server: python3 mcp/villager_proper_mcp.py --debug"
    echo "  • Check documentation: docs/README.md"
else
    echo ""
    echo "❌ Some tests failed. Please check the output above."
    echo ""
    echo "Troubleshooting:"
    echo "  • Check setup instructions: docs/PROPER_VILLAGER_SETUP.md"
    echo "  • Check debug guide: docs/VILLAGER_DEBUG_AND_ORCHESTRATION_GUIDE.md"
    echo "  • Ensure Ollama is running: ollama serve"
fi
