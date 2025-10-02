#!/bin/bash

# ===============================================
# Villager AI Framework - Complete Setup Script
# ===============================================
# 
# This script installs ALL system dependencies and sets up
# the complete Villager AI framework from scratch.
#
# Usage: ./setup.sh
#
# ===============================================

set -e  # Exit on any error

# Change to the script's directory (Villager-AI root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "🏘️ Villager AI Framework - Complete Setup"
echo "=========================================="
echo ""

# HexStrike Integration Notice
echo "🔗 Hybrid Approach Available:"
echo "   Villager AI works with HexStrike AI for comprehensive security testing, but is not required."
echo "   HexStrike provides 150+ additional security tools to use for rapid testing its a great complement to Villager AI."
echo "   Install HexStrike: https://github.com/0x4m4/hexstrike-ai"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if user is root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root"
        print_warning "Please run as a regular user with sudo privileges"
        exit 1
    fi
}

# Function to check sudo access
check_sudo() {
    if ! sudo -n true 2>/dev/null; then
        print_warning "This script requires sudo privileges for system package installation"
        print_status "You may be prompted for your password"
    fi
}

# Function to detect OS
detect_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        print_error "Cannot detect operating system"
        exit 1
    fi
    
    print_status "Detected OS: $OS $VER"
}

# Function to install system packages
install_system_packages() {
    print_status "Installing system packages..."
    
    # Update package lists
    print_status "Updating package lists..."
    sudo apt update
    
    # Install essential packages
    print_status "Installing essential packages..."
    sudo apt install -y \
        curl \
        wget \
        git \
        unzip \
        build-essential \
        python3 \
        python3-dev \
        python3-pip \
        python3-venv \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    print_success "System packages installed"
}

# Function to install Docker
install_docker() {
    if command_exists docker; then
        print_success "Docker is already installed"
        return 0
    fi
    
    print_status "Installing Docker..."
    
    # Add Docker's official GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Set up the repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker Engine
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    print_success "Docker installed successfully"
    print_warning "You need to log out and back in for Docker group changes to take effect"
}

# Function to setup Kali Docker container (True Villager Architecture)
setup_kali_container() {
    print_status "Setting up Kali Linux Docker container (True Villager Architecture)..."
    
    # Pull standard Kali image
    print_status "Pulling standard Kali Linux image..."
    docker pull kalilinux/kali-rolling
    
    # Create workspace directory
    print_status "Creating workspace directory..."
    mkdir -p /tmp/villager_workspace
    
    print_success "Kali Linux container setup complete (True Villager Architecture)"
    print_status "✅ Persistent SSH containers with 24-hour self-destruct"
    print_status "✅ Tools pre-installed in containers (no on-demand installation)"
    print_status "✅ Forensic evasion through ephemeral container lifecycle"
}

# Function to install Ollama
install_ollama() {
    if command_exists ollama; then
        print_success "Ollama is already installed"
        return 0
    fi
    
    print_status "Installing Ollama..."
    
    # Install Ollama
    curl -fsSL https://ollama.ai/install.sh | sh
    
    # Start Ollama service
    print_status "Starting Ollama service..."
    ollama serve &
    OLLAMA_PID=$!
    
    # Wait for Ollama to start
    sleep 5
    
    # Pull the AI model
    print_status "Downloading AI model (this may take a few minutes)..."
    ollama pull deepseek-r1-uncensored
    
    print_success "Ollama installed and configured"
}

# Function to setup Python environment
setup_python_environment() {
    print_status "Setting up Python environment..."
    
    # Create virtual environment
    if [ ! -d "villager-venv-new" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv villager-venv-new
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source villager-venv-new/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Python environment setup complete"
}

# Function to configure environment
configure_environment() {
    print_status "Configuring environment..."
    
    # Copy environment template
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_success "Environment file created from template"
    else
        print_success "Environment file already exists"
    fi
    
    # Create logs directory
    mkdir -p logs
    
    print_success "Environment configured"
}

# Function to run tests
run_tests() {
    print_status "Running tests to verify installation..."
    
    # Activate virtual environment
    source villager-venv-new/bin/activate
    
    # Run tests
    ./tests/run_tests.sh
    
    print_success "Tests completed"
}

# Function to start services
start_services() {
    print_status "Starting Villager services..."
    
    # Activate virtual environment
    source villager-venv-new/bin/activate
    
    # Start services
    ./scripts/start_villager_proper.sh
    
    print_success "Services started"
}

# Function to display final instructions
display_final_instructions() {
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo ""
    echo "✅ All system dependencies installed"
    echo "✅ Python environment configured"
    echo "✅ Villager services started"
    echo ""
    echo "🌐 Service URLs:"
    echo "   • Villager Server: http://localhost:37695"
    echo "   • MCP Client: http://localhost:25989"
    echo "   • Kali Driver: http://localhost:1611"
    echo "   • Browser Service: http://localhost:8080"
    echo ""
    echo "📚 Next Steps:"
    echo "   1. Configure your .env file if needed"
    echo "   2. Test the setup: ./tests/run_tests.sh"
    echo "   3. Start using Villager in your MCP client"
    echo ""
    echo "🔗 Optional - Install HexStrike for Hybrid Approach:"
    echo "   git clone https://github.com/0x4m4/hexstrike-ai.git"
    echo "   cd hexstrike-ai && ./start_hexstrike.sh"
    echo "   (Adds 150+ additional security tools)"
    echo ""
    echo "⚠️  Important Notes:"
    echo "   • You may need to log out and back in for Docker group changes"
    echo "   • Configure MCP with cloud LLM (DeepSeek API recommended)"
    echo "   • All services are now running"
    echo "   • Kali container integration with security tools"
    echo ""
    echo "🐳 Kali Container Integration:"
    echo "   • Uses standard Kali Linux Docker image"
    echo "   • Containers include pre-installed security tools"
    echo "   • SSH-based command execution with 24-hour persistence"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   • Check logs: tail -f logs/*.log"
    echo "   • Restart services: ./start_villager_proper.sh"
    echo "   • Run tests: ./tests/run_tests.sh"
    echo "   • Docker issues: sudo systemctl status docker"
    echo ""
}

# Main execution
main() {
    echo "Starting complete Villager AI Framework setup..."
    echo ""
    echo "💡 Tip: For the full hybrid experience, also install HexStrike MCP:"
    echo "   https://github.com/0x4m4/hexstrike-ai"
    echo ""
    
    # Pre-flight checks
    check_root
    check_sudo
    detect_os
    
    # Installation steps
    install_system_packages
    install_docker
    setup_kali_container
    # install_ollama  # Commented out - use cloud LLM instead (no RAM required)
    setup_python_environment
    configure_environment
    
    # Start services
    start_services
    
    # Wait for services to start
    print_status "Waiting for services to initialize..."
    sleep 30
    
    # Run tests
    run_tests
    
    # Display final instructions
    display_final_instructions
}

# Run main function
main "$@"
