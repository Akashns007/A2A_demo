class Config:
    """Configuration settings for the weather agent"""
    
    # Server settings
    HOST = "0.0.0.0"
    PORT = 7001
    
    # Agent settings
    AGENT_NAME = "WeatherAgent"
    AGENT_VERSION = "1.0.0"
    
    # MCP Server settings
    MCP_COMMAND = "uv"
    MCP_DIRECTORY = "c:/Users/hp/OneDrive/Desktop/assignments/A2A/weather_mcp/src/weather_mcp"
    MCP_SCRIPT = "weather_tool.py"
    
    # LLM settings
    LLM_MODEL = "litellm/gemini/gemini-2.0-flash"
    
    @classmethod
    def get_mcp_args(cls):
        return [
            "--directory",
            cls.MCP_DIRECTORY,
            "run", 
            cls.MCP_SCRIPT
        ]

