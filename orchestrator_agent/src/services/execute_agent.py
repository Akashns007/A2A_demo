import asyncio
from services.orchestrator_agent import run_main_agent
from services.agent_discovery import AgentDiscoveryService


async def orchestrator_run(query: str):   
    try:
        print(f"Starting advanced orchestrator for query: {query}")
        
        discovery_service = AgentDiscoveryService()
        agent_cards = await discovery_service.discover_agents()
        
        if not agent_cards:
            return "No agents are currently available. Please ensure the weather and accommodation agents are running."

        response = await run_main_agent(query, agent_cards)
        return response
        
    except Exception as e:
        print(f"Error in orchestrator_run: {e}")
        return f"Sorry, I encountered an error while processing your request: {str(e)}"


if __name__ == "__main__":
    test_query = """
    I want to go from Bangalore to Chennai and stay at Chennai from 10th Sep 2025 to 14th Sep 2025.
    Please help me plan this trip. there will be 2 kids and 2 adults. the prize should be mid range not too costly.
    """
    asyncio.run(orchestrator_run(test_query))
