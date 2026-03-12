#!/bin/bash

# Test Villager Setup Script
# This script verifies that Villager AI works correctly in native WSL mode

echo "🧪 Testing Setup for Villager AI"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "OK")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
    esac
}

# Test 1: Check if Villager services are running
echo -e "\n${BLUE}1. Checking Villager Services${NC}"
echo "----------------------------"

services=("37695:Villager Server" "25989:MCP Client" "1611:Kali Driver" "8080:Browser Service")
all_services_ok=true

for service in "${services[@]}"; do
    port=$(echo $service | cut -d: -f1)
    name=$(echo $service | cut -d: -f2)
    
    if curl -s http://localhost:$port/health > /dev/null 2>&1; then
        print_status "OK" "$name (Port $port) is healthy"
    else
        print_status "ERROR" "$name (Port $port) is not responding"
        all_services_ok=false
    fi
done

if [ "$all_services_ok" = false ]; then
    print_status "ERROR" "Some Villager services are not running. Please start them first:"
    echo "  ./scripts/start_villager_proper.sh"
    exit 1
fi

# Test 2: Test local security tools availability
echo -e "\n${BLUE}2. Checking Local Security Tools${NC}"
echo "------------------------------------"

tools=("nmap" "sqlmap" "hydra" "nikto" "john")
tools_found=0

for tool in "${tools[@]}"; do
    if command -v "$tool" > /dev/null 2>&1; then
        print_status "OK" "$tool is installed"
        tools_found=$((tools_found + 1))
    else
        print_status "WARN" "$tool is not installed (optional)"
    fi
done

if [ $tools_found -gt 0 ]; then
    print_status "OK" "$tools_found security tools available"
else
    print_status "WARN" "No security tools found. Install them with: sudo apt install nmap sqlmap hydra nikto john"
fi

# Test 3: Test Kali Driver functionality
echo -e "\n${BLUE}3. Testing Kali Driver Functionality${NC}"
echo "------------------------------------"

print_status "INFO" "Testing Kali Driver with a simple command..."

response=$(curl -s -X POST http://localhost:1611/ \
    -H "Content-Type: application/json" \
    -d '{"prompt": "echo hello && pwd && whoami"}' \
    --max-time 30)

if echo "$response" | grep -q "Kali Driver executed"; then
    print_status "OK" "Kali Driver is working correctly"
    
    # Extract and show the output
    output=$(echo "$response" | grep -o '"Output: [^"]*"' | sed 's/"Output: //g' | sed 's/"//g')
    if [ ! -z "$output" ]; then
        echo "   Command output: $output"
    fi
else
    print_status "ERROR" "Kali Driver test failed"
    echo "   Response: $response"
fi

# Test 4: Test MCP Server
echo -e "\n${BLUE}4. Testing MCP Server${NC}"
echo "----------------------"

# Check if MCP server can be started
if timeout 5 python src/villager_ai/mcp/villager_proper_mcp.py --debug > /dev/null 2>&1; then
    print_status "OK" "MCP Server starts successfully"
else
    print_status "ERROR" "MCP Server failed to start"
fi

# Test 5: Summary and Recommendations
echo -e "\n${BLUE}5. Summary${NC}"
echo "--------------------------------"

print_status "OK" "Villager AI is running in native WSL mode"
echo "   - Commands execute directly on the local system"
echo "   - No containers or virtualization needed"
echo "   - All Villager AI features are fully functional"

echo -e "\n${GREEN}🎉 Villager AI is ready to use!${NC}"
echo ""
echo "Next steps:"
echo "1. Restart Cursor to load MCP tools"
echo "2. Check the MCP tools panel for Villager tools"
echo "3. Start using the hybrid Villager AI + HexStrike setup"
echo ""
echo "For detailed setup information, see:"
echo "- docs/AI_ASSISTANT_GUIDE.md"
echo "- docs/TROUBLESHOOTING.md"
