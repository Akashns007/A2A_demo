from agents.mcp import MCPServerStdio
import asyncio
from services.airbnb_agent import run_agent


async def agent_run(query: str):   
    try:
        async with MCPServerStdio(
            name="Airbnb MCP Server",
            params={
                "command": "npx",
                "args": [
                    "-y",
                    "@openbnb/mcp-server-airbnb", 
                    "--ignore-robots-txt"
                ]
            }, 
        ) as server:
            print(f"Starting Airbnb MCP Server for query: {query}")
            response = await run_agent(server, query)
            return response
    except Exception as e:
        print(f"Error in agent_run: {e}")
        return f"Sorry, I encountered an error while processing your Airbnb request: {str(e)}"


if __name__ == "__main__":
    test_query = """
    Please get the hotel rooms from Airbnb for the following dates:
    2025-08-10 to 2025-08-14. London, UK.
    Return the summary as well as the time you got the content.
    For 5 people: 2 are kids and 3 adults, no pets.
    Provide me a summary of the available rooms and their prices.
    """
    asyncio.run(agent_run(test_query))

