# agent_executor.py


# services/execute_agent.py


# services/agent_discovery.py

# tools/call_agent.py



# services/orchestrator_agent.py

# main.py

# test_advanced_orchestrator.py
import asyncio
from services.execute_agent import orchestrator_run


async def test_advanced_orchestrator():
    """Test function for the advanced orchestrator agent"""
    
    test_queries = [
        # Complex multi-step travel planning
        """
        I want to go from Bangalore to Chennai and stay at Chennai from 15th Sep 2025 to 20th Sep 2025.
        Please help me plan this complete trip with weather check and accommodation.
        """,
        
        # Weather-dependent planning
        """
        I'm planning to visit Mumbai from September 10-15, 2025. First check if the weather 
        will be good, and if so, find me suitable accommodation options.
        """,
        
        # Multi-city planning
        """
        Plan a trip to Delhi from September 5-10, 2025. I need both weather forecast 
        and hotel options. If weather is bad, suggest alternative dates.
        """,
        
        # Complex requirements
        """
        Family trip to Goa from September 20-25, 2025. Check weather conditions first, 
        then find family-friendly accommodation for 4 people (2 adults, 2 kids).
        """,
        
        # Discovery test
        "What agents are available to help me plan my travel?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"Test Query {i}:")
        print(query.strip())
        print(f"{'='*80}")
        
        try:
            response = await orchestrator_run(query)
            print(f"Response:\n{response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"{'='*80}\n")
        
        # Wait between requests
        await asyncio.sleep(3)


if __name__ == "__main__":
    print("Testing Advanced Orchestrator Agent...")
    print("Make sure Weather Agent (port 7001) and Airbnb Agent (port 7002) are running!")
    print("The orchestrator will automatically discover available agents...\n")
    asyncio.run(test_advanced_orchestrator())



# requirements.txt
"""
fastapi
uvicorn
starlette
pydantic
python-dotenv
httpx
aiohttp
asyncio
uuid
agents  # Your agents library
a2a.client  # Your A2A client library
a2a.server  # Your A2A server library
a2a.types   # Your A2A types library
"""