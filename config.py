# Villager Configuration - Fixed for MCP SERVER setup
import os
import uuid

# Generate a unique server UUID
SERVER_UUID = str(uuid.uuid4())

# Villager operates as MCP SERVER (not client)
# Remove the MCP client configuration entirely
# Villager will be called by Cursor via MCP protocol

# DeepSeek AI Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')

# Set OpenAI API key for compatibility (Villager uses OpenAI client for DeepSeek)
os.environ['OPENAI_API_KEY'] = DEEPSEEK_API_KEY

# Server Configuration
HOST = os.getenv('VILLAGER_HOST', '0.0.0.0')
PORT = int(os.getenv('VILLAGER_PORT', '37695'))

# Security Configuration - FULL ACCESS for red team operations
ALLOW_SHELL = os.getenv('ALLOW_SHELL', '1') == '1'
ALLOW_APT = os.getenv('ALLOW_APT', '1') == '1'
ALLOW_WRITE = os.getenv('ALLOW_WRITE', '1') == '1'
ALLOW_BUILD = os.getenv('ALLOW_BUILD', '1') == '1'

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'villager.log')

# Master Configuration (required by Villager)
class Master:
    """Master configuration class required by Villager."""
    
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.base_url = DEEPSEEK_BASE_URL
        self.model = "deepseek-chat"
        self.temperature = 0.7
        self.max_tokens = 4000
        self.timeout = 30
        self.default_model = "deepseek-chat"
        
    def get(self, key):
        """Get configuration value by key."""
        if key == "prefix":
            return "You are a helpful AI assistant with access to shell commands and system tools. "
        return getattr(self, key, None)
        
    def get_llm_config(self):
        """Get LLM configuration for DeepSeek AI."""
        return {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout
        }

# Security validation
if DEEPSEEK_API_KEY == "":
    print("⚠️  WARNING: DEEPSEEK_API_KEY not set.")

# MCP Configuration (required by Villager)
class MCP:
    """MCP configuration class required by Villager."""
    
    def __init__(self):
        self.client = {
            'base_url': 'http://localhost:37695',
            'timeout': 30
        }
        self.server = {
            'base_url': 'http://localhost:37695',
            'timeout': 30
        }
        self.enabled = True
        
    def __getitem__(self, key):
        """Make MCP subscriptable."""
        return getattr(self, key, None)
        
    def get(self, key):
        """Get configuration value by key."""
        return getattr(self, key, None)

# Create instances
Master = Master()
MCP = MCP()