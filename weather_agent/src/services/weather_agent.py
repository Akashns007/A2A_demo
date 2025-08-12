from agents import Agent, Runner
from agents.mcp import MCPServer    
from dotenv import load_dotenv

load_dotenv()

llm = "litellm/gemini/gemini-2.0-flash"

async def run_agent(mcp_server: MCPServer, query: str):
    try:
        agent = Agent(
            name="WeatherAgent",
            instructions="""You are a weather agent that provides weather information based on user queries.
            You can answer questions only about the month of September 2025.
            If the query is outside this range, respond with "I can only provide weather information for September 2025.".
            Make sure to use the **RESOURCES** and **TOOLS** available by the MCP server to fetch the weather data.
            If the query is not related to weather, respond with "I can only answer questions about the weather.".
            Do not provide any other information or context outside of the weather data.
            The start_day and end_day should be in the format of **DD**.
            Always provide clear, concise weather information based on the available data.
            """,
            mcp_servers=[mcp_server],
            model=llm,
        )
        print(f"Running weather agent with query: {query}")

        response = await Runner.run(agent, query)
        return response
    except Exception as e:
        print(f"Error in run_agent: {e}")
        return f"Error processing weather request: {str(e)}"

