# Villager Configuration - Z.AI Coding Plan (primary) + OpenRouter (backup)
import os
import uuid

# Generate a unique server UUID
SERVER_UUID = str(uuid.uuid4())

# Villager operates as MCP SERVER (not client)
# Villager will be called by Cursor via MCP protocol

# ──────────────────────────────────────────────────────────────
# LLM Provider Configuration
# Primary: Z.AI Coding Plan  (GLM-4.7 / GLM-5)
# Backup:  OpenRouter         (any model)
# ──────────────────────────────────────────────────────────────

LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'zai')  # Options: 'zai', 'openrouter'

# Z.AI Coding Plan Configuration (Primary)
ZAI_API_KEY = os.getenv('ZAI_API_KEY', '')
ZAI_BASE_URL = os.getenv('ZAI_BASE_URL', 'https://api.z.ai/api/coding/paas/v4')
ZAI_MODEL = os.getenv('ZAI_MODEL', 'glm-4.7')

# OpenRouter Configuration (Backup)
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'zhipu/glm-5')

# Resolve active provider settings
if LLM_PROVIDER == 'zai':
    os.environ['OPENAI_API_KEY'] = ZAI_API_KEY
    os.environ['OPENAI_API_BASE'] = ZAI_BASE_URL
elif LLM_PROVIDER == 'openrouter':
    os.environ['OPENAI_API_KEY'] = OPENROUTER_API_KEY
    os.environ['OPENAI_API_BASE'] = OPENROUTER_BASE_URL

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
        if LLM_PROVIDER == 'zai':
            self.api_key = ZAI_API_KEY
            self.openai_api_key = ZAI_API_KEY
            self.base_url = ZAI_BASE_URL
            self.model = ZAI_MODEL
            self.default_model = ZAI_MODEL
            self.openai_api_endpoint = ZAI_BASE_URL
        elif LLM_PROVIDER == 'openrouter':
            self.api_key = OPENROUTER_API_KEY
            self.openai_api_key = OPENROUTER_API_KEY
            self.base_url = OPENROUTER_BASE_URL
            self.model = OPENROUTER_MODEL
            self.default_model = OPENROUTER_MODEL
            self.openai_api_endpoint = OPENROUTER_BASE_URL

        # Backup provider config (used by failover logic)
        self.backup_api_key = OPENROUTER_API_KEY
        self.backup_base_url = OPENROUTER_BASE_URL
        self.backup_model = OPENROUTER_MODEL
        
        # Common settings
        self.temperature = 0.7
        self.max_tokens = 4000
        self.timeout = 30
        
    def get(self, key):
        """Get configuration value by key."""
        if key == "prefix":
            return "You are a helpful AI assistant with access to shell commands and system tools. "
        elif key == "misc":
            return self.get_misc_config()
        return getattr(self, key, None)
        
    def get_llm_config(self):
        """Get LLM configuration for the active provider."""
        return {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout
        }

    def get_backup_llm_config(self):
        """Get LLM configuration for the backup provider (OpenRouter)."""
        return {
            "api_key": self.backup_api_key,
            "base_url": self.backup_base_url,
            "model": self.backup_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout
        }
    
    def get_misc_config(self):
        """Get miscellaneous configuration for Villager tools."""
        return {
            "shell_encode": "utf-8"
        }

# HexStrike MCP server URL (Villager will advertise these tools to its LLM)
HEXSTRIKE_MCP_URL = os.getenv('HEXSTRIKE_MCP_URL', 'http://localhost:8000')


def validate_config() -> None:
    """
    Validate that required API keys are set for the configured LLM provider.
    Call this lazily (e.g. just before the first LLM call) rather than at
    import time, so tests and Villager-unavailable imports don't break.
    """
    if LLM_PROVIDER == 'zai' and not ZAI_API_KEY:
        raise ValueError(
            "❌ ZAI_API_KEY must be set when using 'zai' provider. "
            "Get one at https://z.ai/manage-apikey/apikey-list"
        )
    if LLM_PROVIDER == 'openrouter' and not OPENROUTER_API_KEY:
        raise ValueError(
            "❌ OPENROUTER_API_KEY must be set when using 'openrouter' provider. "
            "Get one at https://openrouter.ai/keys"
        )

# MCP Configuration (required by Villager)
class MCP:
    """MCP configuration class required by Villager."""
    
    def __init__(self):
        self.client = {
            'base_url': 'http://localhost:25989',  # Villager's MCP Client port
            'timeout': 30,
        }
        self.server = {
            'base_url':   'http://localhost:25989',
            'browser_use': 'http://localhost:8080',
            'timeout':    30,
            # External MCP servers Villager's LLM can call into
            'mcp_servers': {
                'hexstrike':  HEXSTRIKE_MCP_URL,
                'kali_driver': 'http://localhost:1611',
                'browser':    'http://localhost:8080',
            },
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