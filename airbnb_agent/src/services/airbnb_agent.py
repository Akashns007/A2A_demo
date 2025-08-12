from agents import Agent, Runner
from agents.mcp import MCPServer
from dotenv import load_dotenv

load_dotenv()

llm = "litellm/gemini/gemini-2.0-flash"

async def run_agent(mcp_server: MCPServer, query: str):
    try:
        agent = Agent(
            name="AirbnbAgent",
            instructions="""You are an Airbnb assistant that helps users find accommodation.
            You can search for hotels, rooms, and vacation rentals on Airbnb.
            Make sure to use the **RESOURCES** and **TOOLS** available by the MCP server to fetch accommodation data.
            Always provide detailed information about available properties including:
            - Property name and type
            - Price per night
            - Total cost for the stay
            - Number of bedrooms and bathrooms
            - Amenities available
            - Host information
            - Location details
            
            If the query is not related to accommodation or travel, respond with "I can only help you find accommodation on Airbnb.".
            Always include the time when you retrieved the information in your response.
            Be helpful and provide comprehensive summaries of available options.
            Format your responses clearly with bullet points or structured information when appropriate.
            """,
            mcp_servers=[mcp_server],
            model=llm,
        )
        
        print(f"Running Airbnb agent with query: {query}")
        
        response = await Runner.run(agent, query)
        print(f"Airbnb agent response received: {len(str(response)) if response else 0} characters")
        return response
        
    except Exception as e:
        print(f"Error in run_agent: {e}")
        return f"Error processing Airbnb request: {str(e)}"

