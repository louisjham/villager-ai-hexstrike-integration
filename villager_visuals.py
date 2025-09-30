#!/usr/bin/env python3
"""
Villager AI Visual Components
Fancy blue-themed banner and visual elements for Villager AI
"""

# ANSI Color Codes
BLUE = '\033[94m'
CYAN = '\033[96m'
LIGHT_BLUE = '\033[94m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'
BLUE_BG = '\033[44m'
WHITE = '\033[97m'
RED = '\033[91m'
DEEP_RED = '\033[38;5;196m'  # Deep red for VILLAGER
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
ORANGE = '\033[38;5;208m'    # Orange for the hat
PURPLE = '\033[38;5;129m'    # Purple accent

def create_banner():
    """Create a fancy blue-themed ASCII banner for Villager AI."""
    banner = f"""
{BLUE}╔══════════════════════════════════════════════════════════════╗{RESET}
{BLUE}║{RESET}                    {CYAN}🏘️  VILLAGER AI 🏘️{RESET}                      {BLUE}║{RESET}
{BLUE}║{RESET}                                                              {BLUE}║{RESET}
{BLUE}║{RESET}              {BOLD}{CYAN}Autonomous Agent Framework{RESET}                      {BLUE}║{RESET}
{BLUE}║{RESET}              {BOLD}{CYAN}for Security Testing & Research{RESET}                 {BLUE}║{RESET}
{BLUE}║{RESET}                                                              {BLUE}║{RESET}
{BLUE}║{RESET}  {LIGHT_BLUE}🤖 Create custom agents for any security task{RESET}              {BLUE}║{RESET}
{BLUE}║{RESET}  {LIGHT_BLUE}🔧 GitHub Tool Discovery & Integration{RESET}                     {BLUE}║{RESET}
{BLUE}║{RESET}  {LIGHT_BLUE}🚀 Flexible framework for autonomous operations{RESET}            {BLUE}║{RESET}
{BLUE}╚══════════════════════════════════════════════════════════════╝{RESET}
    """
    return banner

def create_ascii_hat():
    """ASCII art hat with orange color."""
    return f"""
{ORANGE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⠀⠀⠀⠴⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⣠⣴⣷⣦⣤⣈⡉⠉⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⣠⣄⡉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀{RESET}
{ORANGE}⢀⣤⣾⣿⣿⣿⣷⣶⣤⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀{RESET}
{ORANGE}⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿{RESET}
{ORANGE}⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁{RESET}
{ORANGE}⠀⠀⠀⠀⠘⣿⡛⠛⠛⠿⠿⠿⢿⣿⣿⣿⣿⡿⠿⠿⠿⠛⠛⢛⣿⠃⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⠙⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠋⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⠀⠈⠻⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣶⣤⣤⣤⣤⣤⣤⣶⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⡿⢿⣅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{ORANGE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠀⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
"""

def create_ascii_font():
    """ASCII art font for VILLAGER with deep red color."""
    return f"""
{DEEP_RED}██▒   █▓ ██▓ ██▓     ██▓    ▄▄▄        ▄████ ▓█████  ██▀███        {RESET}
{DEEP_RED}▓██░   █▒▓██▒▓██▒    ▓██▒   ▒████▄     ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒      {RESET}
{DEEP_RED} ▓██  █▒░▒██▒▒██░    ▒██░   ▒██  ▀█▄  ▒██░▄▄▄░▒███   ▓██ ░▄█ ▒      {RESET}
{DEEP_RED}  ▒██ █░░░██░▒██░    ▒██░   ░██▄▄▄▄██ ░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄        {RESET}
{DEEP_RED}   ▒▀█░  ░██░░██████▒░██████▒▓█   ▓██▒░▒▓███▀▒░▒████▒░██▓ ▒██▒      {RESET}
{DEEP_RED}   ░ ▐░  ░▓  ░ ▒░▓  ░░ ▒░▓  ░▒▒   ▓▒█░ ░▒   ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░      {RESET}
{DEEP_RED}   ░ ░░   ▒ ░░ ░ ▒  ░░ ░ ▒  ░ ▒   ▒▒ ░  ░   ░  ░ ░  ░  ░▒ ░ ▒░      {RESET}
{DEEP_RED}     ░░   ▒ ░  ░ ░     ░ ░    ░   ▒   ░ ░   ░    ░     ░░   ░       {RESET}
{DEEP_RED}      ░   ░      ░  ░    ░  ░     ░  ░      ░    ░  ░   ░           {RESET}
{DEEP_RED}     ░                                                               {RESET}
"""

def create_integrated_banner():
    """Create an integrated banner with hat and VILLAGER text."""
    hat = create_ascii_hat()
    villager_text = create_ascii_font()
    banner = create_banner()
    
    # Combine them with proper spacing
    return f"{hat}\n{villager_text}\n{banner}"

def create_logo():
    """Create a fancy blue-themed text logo."""
    return f"{CYAN}🏘️ {BOLD}VILLAGER AI{RESET}"

def create_startup_message():
    """Create a fancy startup message with blue theme."""
    return f"""
{CYAN}🚀 Villager AI - Autonomous Agent Framework Core{RESET}
{GREEN}⚡ Custom Agents | GitHub Integration | Security Operations{RESET}
{YELLOW}🎯 Bug Bounty | Pentesting | Research | Automation{RESET}
"""

def create_server_info(host="0.0.0.0", port=37695):
    """Create fancy server information display."""
    return f"""
{CYAN}🌐 Server: {BOLD}http://{host}:{port}{RESET}
{CYAN}📚 API Documentation: {BOLD}http://127.0.0.1:{port}/docs{RESET}
{BLUE}{'='*50}{RESET}
"""

def create_success_message(message):
    """Create a green success message."""
    return f"{GREEN}✅ {message}{RESET}"

def create_error_message(message):
    """Create a red error message."""
    return f"{RED}❌ {message}{RESET}"

def create_warning_message(message):
    """Create a yellow warning message."""
    return f"{YELLOW}⚠️  {message}{RESET}"

def create_info_message(message):
    """Create a blue info message."""
    return f"{BLUE}ℹ️  {message}{RESET}"

def create_agent_message(message):
    """Create a magenta agent message."""
    return f"{MAGENTA}🤖 {message}{RESET}"

def create_scan_message(message):
    """Create a yellow scan message."""
    return f"{YELLOW}🔍 {message}{RESET}"

def create_github_message(message):
    """Create a cyan GitHub message."""
    return f"{CYAN}🐙 {message}{RESET}"

def create_security_message(message):
    """Create a red security message."""
    return f"{RED}🔒 {message}{RESET}"

if __name__ == "__main__":
    print(create_integrated_banner())
    print(create_startup_message())
    print(create_server_info())
