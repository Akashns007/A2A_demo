from agents.mcp import MCPServerStdio
import asyncio
from services.weather_agent import run_agent


async def agent_run(query: str):   
    try:
        async with MCPServerStdio(
            name="Weather MCP Server",
            params={
                "command": "uv",
                "args": [
                    "--directory",
                    "c:/Users/hp/OneDrive/Desktop/assignments/A2A/weather_mcp/src/weather_mcp",
                    "run", 
                    "weather_tool.py"
                ]
            }, 
        ) as server:
            print(f"Starting MCP Server for query: {query}")
            response = await run_agent(server, query)
            return response
    except Exception as e:
        print(f"Error in agent_run: {e}")
        return f"Sorry, I encountered an error while processing your weather request: {str(e)}"


if __name__ == "__main__":
    asyncio.run(agent_run('how is the weather on september 10th to sep 14th of 2025?'))

