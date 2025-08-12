from agents import Agent, Runner 
from dotenv import load_dotenv
from services.tools import call_agent
from services.agent_discovery import AgentDiscoveryService

load_dotenv()

llm = "litellm/gemini/gemini-2.0-flash"

async def run_main_agent(query: str, agent_cards):
    try:
        # Format agent cards for the prompt
        discovery_service = AgentDiscoveryService()
        discovery_service.discovered_agents = agent_cards
        formatted_agent_info = discovery_service.format_agent_cards_for_prompt()
        
        agent = Agent(
            name="TravelOrchestratorAgent",
            instructions=f"""You are a helpful travel planning orchestrator agent. Your primary role is to analyze a user's request
            and determine the most suitable agent(s) to handle it. The user's queries will primarily focus on weather and hotel availability.

            Your task is to route the user's request to the correct specialized agent(s) and coordinate their responses.
            
            Here are the agents you can call and their capabilities:
            {formatted_agent_info}

            To route requests, you must use the `call_agent` tool with the following parameters:
            - agent_name: The name of the agent to call (e.g., "WeatherAgent", "AirbnbAgent")
            - message: The specific message/query to send to that agent

            IMPORTANT WORKFLOW EXAMPLE:
            For a query like "I want to go from Bangalore to Chennai and stay at Chennai from 15th Sep 2025 to 20th Sep 2025":
            
            Step 1: Use WeatherAgent first to check weather in Chennai for those dates
            - call_agent("WeatherAgent", "What's the weather like in Chennai from September 15-20, 2025?")
            
            Step 2: Analyze the weather results to see if conditions are suitable for travel
            - If weather is good: proceed to accommodation search
            - If weather is poor: inform user and ask if they still want accommodation options
            
            Step 3: If weather is acceptable, search for accommodations
            - call_agent("AirbnbAgent", "Find accommodation in Chennai from September 15-20, 2025 for [number] people")
            
            You can call agents multiple times and in any sequence needed to provide comprehensive travel planning.
            
            Always:
            1. Consider weather conditions before recommending accommodation
            2. Provide clear reasoning for your recommendations
            3. Summarize information from multiple agents cohesively
            4. Ask clarifying questions if needed (number of travelers, budget, preferences)

            Remember: You're orchestrating a complete travel planning experience!

            **if u face an error specify what the error is**
            """,
            tools=[call_agent],
            model=llm,
        )
        
        print(f"Running travel orchestrator with query: {query}")
        print(f"Available agents: {list(agent_cards.keys())}")

        response = await Runner.run(agent, query)
        return response.final_output
    except Exception as e:
        print(f"Error in run_main_agent: {e}")
        return f"Error processing request: {str(e)}"

