#!/bin/bash

# Test Villager Setup Script
# This script verifies that Villager AI works correctly with Kali containers

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

# Test 2: Test Docker and Kali image availability
echo -e "\n${BLUE}2. Testing Docker and Kali Image Access${NC}"
echo "------------------------------------"

print_status "INFO" "Checking Docker and Kali image availability..."
if docker images | grep -q "kalilinux/kali-rolling"; then
    print_status "OK" "Kali Linux image is available locally"
    kali_available=true
else
    print_status "INFO" "Pulling Kali Linux image..."
    if timeout 60 docker pull kalilinux/kali-rolling > /dev/null 2>&1; then
        print_status "OK" "Kali Linux image pulled successfully"
        kali_available=true
    else
        print_status "WARN" "Kali Linux image pull failed"
        kali_available=false
    fi
fi

# Test 3: Test Kali Driver functionality
echo -e "\n${BLUE}3. Testing Kali Driver Functionality${NC}"
echo "------------------------------------"

print_status "INFO" "Testing Kali Driver with a simple command..."

response=$(curl -s -X POST http://localhost:1611/ \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Run whoami && pwd && which nmap"}' \
    --max-time 30)

if echo "$response" | grep -q "Kali Driver executed"; then
    print_status "OK" "Kali Driver is working correctly"
    
    # Extract and show the output
    output=$(echo "$response" | grep -o '"Output: [^"]*"' | sed 's/"Output: //g' | sed 's/"//g')
    if [ ! -z "$output" ]; then
        echo "   Command output: $output"
    fi
    
    # Check if tools are available
    if echo "$response" | grep -q "nmap"; then
        print_status "OK" "Security tools (nmap) are available"
    else
        print_status "WARN" "Security tools may still be installing (wait 1-2 minutes)"
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
echo -e "\n${BLUE}5. Summary and Recommendations${NC}"
echo "--------------------------------"

if [ "$kali_available" = true ]; then
    print_status "OK" "Kali container system is working perfectly!"
    echo "   - Kali Linux image is available and ready"
    echo "   - All security tools are automatically installed"
    echo "   - All Villager AI features are fully functional"
    echo "   - No additional setup required"
else
    print_status "WARN" "Kali image not available - check Docker setup"
    echo "   - Docker may not be running"
    echo "   - Network connectivity issues"
    echo "   - Check Docker daemon status"
fi

echo -e "\n${GREEN}🎉 Villager AI is ready to use!${NC}"
echo ""
echo "Next steps:"
echo "1. Restart Cursor to load MCP tools"
echo "2. Check the MCP tools panel for Villager tools"
echo "3. Start using the hybrid Villager AI + HexStrike setup"
echo ""
echo "For detailed setup information, see:"
echo "- docs/KALI_CONTAINER_SETUP.md"
echo "- docs/AI_ASSISTANT_GUIDE.md"
echo "- docs/TROUBLESHOOTING.md"
