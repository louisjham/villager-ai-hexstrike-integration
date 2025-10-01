#!/bin/bash

# Test runner script for Villager AI Framework
echo "🧪 Running Villager AI Tests"
echo "============================="

# Check if we're in the right directory
if [ ! -f "tests/test_villager_ai.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo "❌ Error: pytest is not installed"
    echo "Install it with: pip install pytest pytest-cov"
    exit 1
fi

# Run the tests
echo "Running tests..."
pytest tests/ -v --tb=short

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed"
    exit 1
fi
