class AirbnbConfig:
    """Configuration settings for the Airbnb agent"""
    
    # Server settings
    HOST = "0.0.0.0"
    PORT = 7002
    
    # Agent settings
    AGENT_NAME = "AirbnbAgent"
    AGENT_VERSION = "1.0.0"
    
    # MCP Server settings
    MCP_COMMAND = "npx"
    MCP_PACKAGE = "@openbnb/mcp-server-airbnb"
    MCP_FLAGS = ["--ignore-robots-txt"]
    
    # LLM settings
    LLM_MODEL = "litellm/gemini/gemini-2.0-flash"
    
    @classmethod
    def get_mcp_args(cls):
        return [
            "-y",
            cls.MCP_PACKAGE,
            *cls.MCP_FLAGS
        ]

